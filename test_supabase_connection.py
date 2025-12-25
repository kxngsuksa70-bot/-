"""
Test Supabase Connection
ทดสอบการเชื่อมต่อ Supabase ทั้ง Direct และ Pooler
"""

# Fix encoding for Windows
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

# Direct Connection
DIRECT_CONFIG = {
    'host': 'db.hbbqwcesmwqnfgkmdayp.supabase.co',
    'port': '5432',
    'database': 'postgres',
    'user': 'postgres',
    'password': os.environ.get('SUPABASE_PASSWORD', '@aslk099980'),
}

# Pooler Connection
POOLER_CONFIG = {
    'host': 'aws-0-ap-southeast-1.pooler.supabase.com',
    'port': '6543',
    'database': 'postgres',
    'user': 'postgres.hbbqwcesmwqnfgkmdayp',
    'password': os.environ.get('SUPABASE_PASSWORD', '@aslk099980'),
}

def test_connection(config, name):
    """Test database connection"""
    print(f"\n{'='*60}")
    print(f"Testing {name}")
    print(f"{'='*60}")
    print(f"Host: {config['host']}")
    print(f"Port: {config['port']}")
    print(f"User: {config['user']}")
    
    try:
        # Try to connect
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password'],
            connect_timeout=10
        )
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM teachers")
        count = cursor.fetchone()[0]
        
        print(f"✅ SUCCESS! Connected to {name}")
        print(f"✅ Found {count} teachers in database")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {name}")
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🔍 Supabase Connection Test")
    print("="*60)
    
    # Test Direct Connection
    direct_success = test_connection(DIRECT_CONFIG, "Direct Connection (port 5432)")
    
    # Test Pooler Connection
    pooler_success = test_connection(POOLER_CONFIG, "Pooler Connection (port 6543)")
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 Summary")
    print(f"{'='*60}")
    print(f"Direct Connection: {'✅ SUCCESS' if direct_success else '❌ FAILED'}")
    print(f"Pooler Connection: {'✅ SUCCESS' if pooler_success else '❌ FAILED'}")
    
    if pooler_success:
        print("\n💡 Recommendation: Use POOLER connection for Railway")
        print("   SUPABASE_HOST=aws-0-ap-southeast-1.pooler.supabase.com")
        print("   SUPABASE_PORT=6543")
        print("   SUPABASE_USER=postgres.hbbqwcesmwqnfgkmdayp")
    elif direct_success:
        print("\n💡 Recommendation: Use DIRECT connection")
        print("   SUPABASE_HOST=db.hbbqwcesmwqnfgkmdayp.supabase.co")
        print("   SUPABASE_PORT=5432")
        print("   SUPABASE_USER=postgres")
    else:
        print("\n❌ Both connections failed. Please check:")
        print("   1. Supabase password is correct")
        print("   2. Supabase project is running")
        print("   3. Network/firewall settings")
