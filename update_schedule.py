import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='teachmap_db'
)

cursor = conn.cursor()
cursor.execute('UPDATE schedule SET end_time="13:30", duration=5.0 WHERE subject="Database Systems"')
conn.commit()
print(f'✅ Updated {cursor.rowcount} row(s)')
print('Database Systems now: 08:30 - 13:30 (5 hours)')

cursor.close()
conn.close()
