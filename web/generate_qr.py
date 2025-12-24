#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
QR Code Generator for TeachMap PWA
สร้าง QR Code สำหรับเข้าถึงเว็บไซต์

วิธีใช้:
    python generate_qr.py
    หรือ
    python generate_qr.py <custom-url>
"""

import qrcode
import sys
import os

def generate_qr_code(url, filename="teachmap_qr.png"):
    """
    สร้าง QR Code และบันทึกเป็นไฟล์ PNG
    
    Args:
        url: URL ที่จะใส่ใน QR Code
        filename: ชื่อไฟล์ที่จะบันทึก (default: teachmap_qr.png)
    """
    print(f"[*] กำลังสร้าง QR Code สำหรับ URL: {url}")
    
    # สร้าง QR Code
    qr = qrcode.QRCode(
        version=1,  # ขนาดของ QR Code (1-40)
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # ระดับการแก้ไขข้อผิดพลาดสูงสุด
        box_size=10,  # ขนาดของแต่ละกล่อง
        border=4,  # ความกว้างของขอบ
    )
    
    qr.add_data(url)
    qr.make(fit=True)
    
    # สร้างรูปภาพ
    img = qr.make_image(
        fill_color="black",
        back_color="white"
    )
    
    # บันทึกไฟล์
    output_path = os.path.join(os.path.dirname(__file__), filename)
    img.save(output_path)
    
    print(f"[OK] สร้าง QR Code สำเร็จ!")
    print(f"[FILE] ไฟล์: {output_path}")
    print(f"[SIZE] ขนาด: {img.size[0]}x{img.size[1]} pixels")
    
    return output_path

def main():
    """Main function"""
    print("=" * 60)
    print("  QR Code Generator - TeachMap PWA")
    print("=" * 60)
    print()
    
    # รับ URL จาก command line หรือใช้ default
    if len(sys.argv) > 1:
        url = sys.argv[1]
        custom_url = True
    else:
        # Default URLs
        print("เลือกประเภท QR Code:")
        print("1. Localhost (http://localhost:5000) - สำหรับเครือข่ายเดียวกัน")
        print("2. ใส่ URL เอง")
        print()
        
        choice = input("กรุณาเลือก (1-2): ").strip()
        
        if choice == "1":
            url = "http://localhost:5000"
            custom_url = False
        elif choice == "2":
            url = input("กรุณาใส่ URL: ").strip()
            custom_url = True
        else:
            print("[ERROR] ตัวเลือกไม่ถูกต้อง")
            return
    
    if not url:
        print("[ERROR] กรุณาระบุ URL")
        return
    
    # ตรวจสอบว่า URL มี protocol หรือไม่
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    print()
    
    # สร้างชื่อไฟล์
    if custom_url and 'ngrok' in url:
        filename = "teachmap_qr_ngrok.png"
    elif 'localhost' in url:
        filename = "teachmap_qr_localhost.png"
    else:
        filename = "teachmap_qr_custom.png"
    
    # สร้าง QR Code
    try:
        output_path = generate_qr_code(url, filename)
        print()
        print("=" * 60)
        print("[INFO] วิธีใช้งาน:")
        print("  1. เปิดกล้องมือถือ")
        print("  2. เล็งไปที่ QR Code")
        print("  3. แตะลิงก์ที่ขึ้นบนหน้าจอ")
        print("  4. เข้าสู่ระบบด้วย Username และ Password")
        print("=" * 60)
    except Exception as e:
        print(f"[ERROR] เกิดข้อผิดพลาด: {e}")
        print("[TIP] ตรวจสอบว่าติดตั้ง qrcode แล้วหรือไม่: pip install qrcode[pil]")

if __name__ == "__main__":
    main()
