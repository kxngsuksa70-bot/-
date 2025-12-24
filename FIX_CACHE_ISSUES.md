# แก้ปัญหา: หน้าเว็บไม่รีเฟรชข้อมูลล่าสุด

## 🐛 สาเหตุ
- **Browser Cache** เก็บข้อความเดิม
- **Service Worker** (PWA) เก็บข้อมูลไว้ offline

---

## ✅ วิธีแก้ชั่วคราว

### วิธีที่ 1: Hard Refresh (แนะนำ)
```
Ctrl + Shift + R  (Windows)
Cmd + Shift + R   (Mac)
```

### วิธีที่ 2: Clear Cache
1. `F12` → **Application** tab
2. **Storage** → **Clear site data**
3. Refresh

### วิธีที่ 3: Unregister Service Worker
1. `F12` → **Application** tab
2. **Service Workers** → **Unregister**
3. Refresh

---

## ✅ แก้ไขถาวร (ทำแล้ว)

ผมแก้ไข `sw.js` ให้:
- ✅ ไม่ cache API responses
- ✅ ใช้ Network-First สำหรับ HTML
- ✅ Cache แค่ไฟล์ static (CSS, images)
- ✅ Auto-update เมื่อมี version ใหม่

**วิธีใช้:**
1. Clear cache ครั้งสุดท้าย (Ctrl+Shift+R)
2. หลังจากนี้จะได้ข้อมูลล่าสุดเสมอ!

---

## 🔄 อัพเดทในอนาคต

ถ้าแก้ code แล้วต้องการให้ผู้ใช้เห็นทันที:

**วิธีที่ 1:** เปลี่ยน Cache Name
```javascript
// ใน sw.js
const CACHE_NAME = 'teachmap-v1.2';  // เพิ่มเลข
```

**วิธีที่ 2:** Hard Refresh
ผู้ใช้กด `Ctrl+Shift+R`

---

## 📝 หมายเหตุ

**ก่อนหน้า:**
- Cache ทุกอย่าง → ไม่เห็นข้อมูลใหม่

**ตอนนี้:**
- ไม่ cache API → เห็นข้อมูลล่าสุดเสมอ
- Cache แค่ static files → โหลดเร็วขึ้น

---

## 🆘 ถ้ายังไม่ได้

ลองทำตามนี้:
```bash
# 1. Clear browser data completely
# Settings → Privacy → Clear browsing data → All time

# 2. หรือใช้ Incognito Mode
Ctrl + Shift + N
```
