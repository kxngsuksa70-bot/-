"""
Database Import Script
วิธีใช้: python import_database.py teachmap_db_backup.sql
"""

import sys
import os
import mysql.connector

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234'
}

def import_database(sql_file):
    """Import database from SQL file"""
    if not os.path.exists(sql_file):
        print(f"❌ File not found: {sql_file}")
        return False
    
    print(f"🔄 Importing database from {sql_file}...")
    
    try:
        # Create database if not exists
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS teachmap_db")
        cursor.close()
        conn.close()
        
        # Import SQL file
        cmd = f'mysql -u {DB_CONFIG["user"]} -p{DB_CONFIG["password"]} teachmap_db < {sql_file}'
        result = os.system(cmd)
        
        if result == 0:
            print("✅ Database imported successfully!")
            return True
        else:
            print("❌ Import failed")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python import_database.py <sql_file>")
        sys.exit(1)
    
    sql_file = sys.argv[1]
    import_database(sql_file)
