"""
Database Export Script
วิธีใช้: python export_database.py
จะสร้างไฟล์ teachmap_db_backup.sql
"""

import mysql.connector
from datetime import datetime
import subprocess
import sys
import os

# Database config
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'teachmap_db'
}

def export_database():
    """Export database to SQL file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'teachmap_db_backup_{timestamp}.sql'
    
    print(f"🔄 Exporting database to {filename}...")
    
    try:
        # Try to find mysqldump
        mysqldump_paths = [
            'mysqldump',  # In PATH
            r'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe',
            r'C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqldump.exe',
            r'C:\xampp\mysql\bin\mysqldump.exe',
        ]
        
        mysqldump_cmd = None
        for path in mysqldump_paths:
            try:
                result = subprocess.run([path, '--version'], 
                                      capture_output=True, 
                                      timeout=5)
                if result.returncode == 0:
                    mysqldump_cmd = path
                    print(f"✓ Found mysqldump: {path}")
                    break
            except:
                continue
        
        if not mysqldump_cmd:
            print("❌ mysqldump not found!")
            print("\nPlease install MySQL or add mysqldump to PATH")
            print("Or use MySQL Workbench: Server -> Data Export")
            return None
        
        # Export using mysqldump
        with open(filename, 'w', encoding='utf-8') as f:
            result = subprocess.run(
                [mysqldump_cmd, 
                 '-u', DB_CONFIG['user'],
                 f'-p{DB_CONFIG["password"]}',
                 '--databases', DB_CONFIG['database'],
                 '--add-drop-database'],
                stdout=f,
                stderr=subprocess.PIPE,
                text=True
            )
        
        if result.returncode == 0:
            file_size = os.path.getsize(filename)
            if file_size > 0:
                print(f"✅ Database exported successfully!")
                print(f"   File: {os.path.abspath(filename)}")
                print(f"   Size: {file_size:,} bytes")
                print(f"\n📋 To import on new machine:")
                print(f"   mysql -u root -p < {filename}")
                return filename
            else:
                print("❌ Export file is empty")
                return None
        else:
            print(f"❌ Export failed: {result.stderr}")
            return None
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == '__main__':
    export_database()
