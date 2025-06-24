from supabase import Client, create_client
import osu
from osu import Scope, GameModeStr
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="sec.env")


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
redirect_url = "http://127.0.0.1:8080"


OSU_CLIENT_ID = os.getenv("OSU_CLIENT_ID")
OSU_CLIENT_SECRET = os.getenv("OSU_CLIENT_SECRET")

osu_auth = osu.AuthHandler(OSU_CLIENT_ID, OSU_CLIENT_SECRET, Scope.identify())
client_updater = osu.Client.from_credentials(OSU_CLIENT_ID, OSU_CLIENT_SECRET, redirect_url, limit_per_minute=50)

def get_pp(osu_username):
    if osu_username:
        user = client_updater.get_user(osu_username, GameModeStr.STANDARD)
        pp = round(user.statistics.pp)
        username = user.username
        global_rank = user.statistics.global_rank
        return username, global_rank, pp
    
def update_pp():
    print(supabase)
    response = supabase.table("discord_osu").select("osu_id").execute()
    if not response.data:
        print("Error fetching users names")
        return
    print("Username successfully gotten")
    users = response.data
    for user in users:
        osu_id = user.get("osu_id")
        username, rank,pp = get_pp(osu_id)
        if pp is not None:
            supabase.table("discord_osu").update({"current_pp": pp, "osu_username": username, "global_rank": rank}).eq("osu_id", osu_id).execute()
            print(f"{username}'s, osu pp: {pp}, rank: {rank} updated.")



def main():
    while True:
        update_pp()

if __name__ == "__main__":
    main()
    
