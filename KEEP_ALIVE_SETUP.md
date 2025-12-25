# Keep-Alive Automation Setup

## 🎯 วัตถุประสงค์

ป้องกัน Supabase project ถูก pause โดยอัตโนมัติ (Free tier pause หลังไม่มี activity 7 วัน)

---

## ✅ สิ่งที่ตั้งค่าไว้แล้ว

### GitHub Actions Workflow

**ไฟล์**: `.github/workflows/keep-alive.yml`

**ทำงาน**:
- 🕐 รันทุก 4 วัน (เที่ยงคืน UTC)
- 📡 Ping Railway app
- 🔍 Query Supabase database
- ✅ สร้าง activity ป้องกัน pause

---

## 🔧 ขั้นตอนการตั้งค่า (สำคัญ!)

### 1. เพิ่ม GitHub Secret

1. **ไปที่ GitHub Repository**:
   ```
   https://github.com/kxngsuksa70-bot/-/settings/secrets/actions
   ```

2. **คลิก "New repository secret"**

3. **เพิ่ม Secret**:
   - **Name**: `SUPABASE_KEY`
   - **Value**: 
     ```
     eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImhiYnF3Y2VzbXdxbmZna21kYXlwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjY1ODQ0MTYsImV4cCI6MjA4MjE2MDQxNn0.tjznDVl8QELQ4nMmrOohUnC3EBsE5HFd5bv44OoM3bI
     ```
   - **คลิก "Add secret"**

---

## 🚀 การใช้งาน

### รันอัตโนมัติ
- ✅ ระบบจะรันเองทุก 4 วัน
- ✅ ไม่ต้องทำอะไรเพิ่ม

### รันด้วยตนเอง
1. ไปที่: `https://github.com/kxngsuksa70-bot/-/actions`
2. คลิก "Keep-Alive Health Check"
3. คลิก "Run workflow" → "Run workflow"

---

## 📊 ตรวจสอบการทำงาน

### ดู Logs
1. ไปที่: `https://github.com/kxngsuksa70-bot/-/actions`
2. คลิก run ล่าสุด
3. ดู logs:
   ```
   ✅ Pinging Railway app...
   ✅ Querying Supabase to keep it active...
   ✅ Keep-alive completed!
   ```

### ตรวจสอบ Schedule
- GitHub จะแสดงเวลา run ถัดไปในหน้า Actions

---

## ⚙️ ปรับแต่ง Schedule

ถ้าต้องการเปลี่ยนความถี่:

**แก้ไข** `.github/workflows/keep-alive.yml`:

```yaml
schedule:
  - cron: '0 0 */4 * *'  # ทุก 4 วัน
```

**ตัวอย่างอื่นๆ**:
- ทุก 3 วัน: `'0 0 */3 * *'`
- ทุก 5 วัน: `'0 0 */5 * *'`
- ทุกวันจันทร์: `'0 0 * * 1'`

**Cron Format**: `นาที ชั่วโมง วัน เดือน วันในสัปดาห์`

---

## 🎯 ผลลัพธ์

✅ **Supabase จะไม่ pause** เพราะมี activity ทุก 4 วัน (ก่อนครบ 7 วัน)

✅ **Railway app จะถูก ping** เพื่อเช็คว่าทำงานปกติ

✅ **ฟรี!** ใช้ GitHub Actions free tier (2,000 นาที/เดือน)

---

## 🔍 Troubleshooting

### Workflow ไม่รัน

1. **เช็คว่า push ไฟล์แล้ว**:
   ```bash
   git status
   ```

2. **เช็คว่ามี Secret**:
   - ไปที่ Settings → Secrets → Actions
   - ต้องมี `SUPABASE_KEY`

3. **เช็ค Actions permissions**:
   - Settings → Actions → General
   - Allow all actions and reusable workflows

### Query ล้มเหลว

- เช็คว่า `SUPABASE_KEY` ถูกต้อง
- เช็คว่า Supabase project ยังไม่ถูก pause

---

**Status**: ✅ พร้อมใช้งาน - ทุกอย่างตั้งค่าเสร็จแล้ว!
