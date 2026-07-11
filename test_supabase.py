from dotenv import load_dotenv
load_dotenv()

from backend.ai.services.supabase_service import supabase

print(supabase)
