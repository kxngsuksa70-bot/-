import database as db

conn = db.get_connection()
cursor = conn.cursor()

# Add course_code
try:
    cursor.execute('ALTER TABLE schedule ADD COLUMN course_code VARCHAR(20) AFTER subject')
    print('Added course_code column')
except Exception as e:
    print(f'course_code: {e}')

# Add classroom  
try:
    cursor.execute('ALTER TABLE schedule ADD COLUMN classroom VARCHAR(50) AFTER course_code')
    print('Added classroom column')
except Exception as e:
    print(f'classroom: {e}')

# Add end_time
try:
    cursor.execute('ALTER TABLE schedule ADD COLUMN end_time VARCHAR(10) AFTER start_time')
    print('Added end_time column')
except Exception as e:
    print(f'end_time: {e}')

conn.commit()
cursor.close()
conn.close()
print('Database schema updated!')
