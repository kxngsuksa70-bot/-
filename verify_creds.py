
import os
from supabase import create_client, Client

# Credentials provided by user
url = "https://hbbqwcesmwqnfgkmdayp.supabase.co"
key = "sb_publishable_Ln1_Vu-1Moho5_l6CsfMIQ_ZwVpPcj6"

def test_connection():
    print(f"Testing connection to {url}")
    print(f"Key: {key[:10]}...")
    
    try:
        supabase: Client = create_client(url, key)
        # Try a simple query
        response = supabase.table('teachers').select("count", count="exact").execute()
        print("✅ Connection Successful!")
        print(f"Check Result: {response}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    test_connection()
