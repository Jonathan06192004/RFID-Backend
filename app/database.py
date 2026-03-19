import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Check if environment variables exist
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials are missing in the .env file")

print("Connected to Supabase:", SUPABASE_URL)

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)