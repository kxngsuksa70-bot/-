# Auto-Reload สำหรับ Development

## วิธีที่ 1: ใช้ Flask Debug Mode (มีอยู่แล้ว)

Flask debug mode ทำให้ server restart เมื่อแก้ Python code แต่ **ไม่ reload browser**

## วิธีที่ 2: ใช้ Browser Extension

### Chrome/Edge: Live Server
1. ติดตั้ง extension: "Live Reload" หรือ "Auto Refresh"
2. เปิด extension
3. แก้โค้ด → browser refresh อัตโนมัติ

### Firefox: Auto Refresh
ติดตั้ง "Auto Refresh" addon

---

## วิธีที่ 3: Livereload Package (แนะนำ!)

```bash
pip install flask-livereload
```

แก้ไข `app.py`:

```python
from flask_livereload import LiveReload

app = Flask(__name__)
LiveReload(app)  # เพิ่มบรรทัดนี้

# ... rest of code
```

**ผลลัพธ์:** แก้ HTML/CSS/JS → browser reload อัตโนมัติ!

---

## วิธีที่ 4: ปิด Service Worker ขณะ Dev

เปิด DevTools (F12) → **Application** → **Service Workers** → ติ๊ก "**Bypass for network**"

**ผลลัพธ์:** cache ถูก bypass → เห็นการเปลี่ยนแปลงทันที

---

## วิธีที่ 5: อัปเดต Service Worker Version

แก้ `sw.js` เปลี่ยน version:

```javascript
const CACHE_NAME = 'teachmap-v1.2';  // เพิ่มเลข
```

**ผลลัพธ์:** ผู้ใช้ reload จะได้ไฟล์ใหม่

---

## 🎯 คำแนะนำ

### ขณะ Development:
```
1. ปิด Service Worker (F12 → Application → Bypass)
2. หรือใช้ Incognito Mode
3. หรือติดตั้ง flask-livereload
```

### Production:
```
1. เปลี่ยน CACHE_NAME เมื่อมีการอัปเดต
2. Service Worker จะอัปเดตอัตโนมัติ
3. ผู้ใช้ refresh จะได้เวอร์ชันใหม่
```

---

## ⚠️ สำคัญ

**เว็บทั่วไป** (Gmail, Facebook):
- ไม่มี Service Worker cache แบบ aggressive
- หรือมี sophisticated cache strategy
- Server-side rendering

**PWA** (TeachMap):
- Cache เพื่อทำงาน offline
- Trade-off: ต้อง refresh เพื่อดู update
- เป็นเรื่องปกติของ PWA

---

## 📱 ตอนนี้ในโปรเจกต์

ผมได้แก้ `sw.js` ให้:
- ✅ ไม่ cache API responses
- ✅ Network-first สำหรับ HTML
- ✅ Cache แค่ static files

**แต่ถ้าต้องการ perfect hot reload:**
- ใช้ `flask-livereload` (development)
- หรือปิด Service Worker ขณะพัฒนา
