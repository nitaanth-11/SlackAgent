from dotenv import load_dotenv
load_dotenv()

from backend.database.supabase import supabase

print(supabase)
