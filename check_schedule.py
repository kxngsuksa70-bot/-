import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='1234',
    database='teachmap_db'
)

cursor = conn.cursor(dictionary=True)
cursor.execute('SELECT id, subject, start_time, end_time, duration FROM schedule WHERE teacher_id=1')
results = cursor.fetchall()

for row in results:
    print(f"Subject: {row['subject']}")
    print(f"  Start: {row['start_time']}")
    print(f"  End: {row['end_time']}")
    print(f"  Duration: {row['duration']}")
    print()

cursor.close()
conn.close()
