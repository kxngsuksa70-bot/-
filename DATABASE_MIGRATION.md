# Database Migration Guide

## วิธีย้ายฐานข้อมูลไปเครื่องใหม่

### วิธีที่ 1: ใช้ mysqldump (แนะนำ)

**ในเครื่องเดิม (export):**
```bash
# Export database
mysqldump -u root -p1234 teachmap_db > teachmap_db_backup.sql
```

**ในเครื่องใหม่ (import):**
```bash
# 1. สร้าง database
mysql -u root -p
CREATE DATABASE teachmap_db;
exit

# 2. Import ข้อมูล
mysql -u root -p teachmap_db < teachmap_db_backup.sql
```

### วิธีที่ 2: ใช้ Python scripts

**ในเครื่องเดิม:**
```bash
python export_database.py
# จะได้ไฟล์ teachmap_db_backup_YYYYMMDD_HHMMSS.sql
```

**ในเครื่องใหม่:**
```bash
python import_database.py teachmap_db_backup_YYYYMMDD_HHMMSS.sql
```

### วิธีที่ 3: Copy ไฟล์ MySQL (ถ้า MySQL version เดียวกัน)

1. หยุด MySQL service ทั้ง 2 เครื่อง
2. Copy folder:
   - Windows: `C:\ProgramData\MySQL\MySQL Server X.X\Data\teachmap_db\`
   - Linux/Mac: `/var/lib/mysql/teachmap_db/`
3. เริ่ม MySQL service

## เช็คข้อมูลหลัง import

```bash
# Login MySQL
mysql -u root -p

# เช็คข้อมูล
USE teachmap_db;
SHOW TABLES;
SELECT * FROM teachers;
SELECT * FROM students;
SELECT * FROM schedule;
```

## Troubleshooting

**ถ้า import ไม่ได้:**
```bash
# ลบ database เก่าก่อน
mysql -u root -p
DROP DATABASE teachmap_db;
CREATE DATABASE teachmap_db;
exit

# Import ใหม่
mysql -u root -p teachmap_db < teachmap_db_backup.sql
```

**ถ้า password ไม่ตรง:**
แก้ไขใน `database.py`:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'YOUR_PASSWORD',  # เปลี่ยนตรงนี้
    'database': 'teachmap_db'
}
```
