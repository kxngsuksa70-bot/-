"""
Setup ngrok authtoken
"""
from pyngrok import ngrok

# วาง authtoken ของคุณที่นี่
NGROK_AUTH_TOKEN = "YOUR_AUTHTOKEN_HERE"

# ตั้งค่า authtoken
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

print("✅ ngrok authtoken ตั้งค่าเรียบร้อย!")
print("ตอนนี้สามารถรัน python app.py ได้แล้ว")
