// Teacher Page JavaScript
const API_BASE = '';

let mySchedule = [];

// Check auth and load data
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Teacher page loaded');

    if (!checkAuth('teacher')) {
        console.log('Auth failed');
        return;
    }

    const user = getCurrentUser();
    if (user) {
        console.log('Teacher:', user.name);
    }

    await loadSchedule();
});

// Load schedule
async function loadSchedule() {
    console.log('Loading schedule...');
    const loading = document.getElementById('loading');
    const scheduleBody = document.getElementById('scheduleBody');

    try {
        loading.classList.remove('hidden');

        console.log('Fetching /api/schedule');
        const response = await fetch(`${API_BASE}/api/schedule`);
        console.log('Status:', response.status);

        const data = await response.json();
        console.log('Data:', data);

        mySchedule = data;
        renderSchedule();

    } catch (error) {
        console.error(error);
        scheduleBody.innerHTML = '<tr><td colspan="6" class="text-center">เกิดข้อผิดพลาด</td></tr>';
    } finally {
        loading.classList.add('hidden');
    }
}

// Render schedule
function renderSchedule() {
    const scheduleBody = document.getElementById('scheduleBody');

    const dayMap = {
        'Mon': 'จันทร์', 'Tue': 'อังคาร', 'Wed': 'พุธ',
        'Thu': 'พฤหัสบดี', 'Fri': 'ศุกร์', 'Sat': 'เสาร์'
    };

    const dayOrder = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const sorted = mySchedule.sort((a, b) => {
        const dd = dayOrder.indexOf(a.day) - dayOrder.indexOf(b.day);
        if (dd) return dd;
        return a.start.localeCompare(b.start);
    });

    if (!sorted.length) {
        scheduleBody.innerHTML = '<tr><td colspan="6" class="text-center">ยังไม่มีตารางสอน คลิก "+ เพิ่มวิชา"</td></tr>';
        return;
    }

    scheduleBody.innerHTML = sorted.map(s => `
        <tr class="schedule-row">
            <td>${dayMap[s.day] || s.day}</td>
            <td>${s.start} - ${s.end} (${s.duration}h)</td>
            <td>${s.subject}</td>
            <td>${s.course_code || '-'}</td>
            <td>${s.classroom || '-'}</td>
            <td>
                <button class="btn btn-secondary" style="padding:6px 12px;margin-right:5px" onclick="editSchedule(${s.id})">แก้ไข</button>
                <button class="btn btn-danger" style="padding:6px 12px" onclick="deleteSchedule(${s.id})">ลบ</button>
            </td>
        </tr>
    `).join('');
}

function openAddDialog() { showScheduleDialog(); }

function editSchedule(id) {
    const s = mySchedule.find(x => x.id === id);
    if (s) showScheduleDialog(s);
}

function showScheduleDialog(existing = null) {
    const dayTh = { 'Mon': 'จันทร์', 'Tue': 'อังคาร', 'Wed': 'พุธ', 'Thu': 'พฤหัสบดี', 'Fri': 'ศุกร์', 'Sat': 'เสาร์' };
    const isEdit = !!existing;
    const title = isEdit ? 'แก้ไข' : 'เพิ่มวิชา';

    const modal = `
    <div id="scheduleModal" style="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.8);display:flex;align-items:center;justify-content:center;z-index:1000;padding:20px">
        <div style="background:var(--card-bg);border-radius:12px;max-width:500px;width:100%;padding:30px;max-height:90vh;overflow-y:auto">
            <h2 style="color:var(--primary);margin-bottom:20px">${title}</h2>
            <form id="sf" style="display:flex;flex-direction:column;gap:15px">
                <div class="form-group"><label>วัน</label>
                    <select id="dayI" style="width:100%;padding:12px;background:var(--input-bg);border:none;border-radius:8px;color:var(--text)">
                        ${Object.keys(dayTh).map(en => `<option value="${en}" ${existing && existing.day === en ? 'selected' : ''}>${dayTh[en]}</option>`).join('')}
                    </select>
                </div>
                <div class="form-group"><label>เวลาเริ่ม</label><input type="time" id="startI" value="${existing ? existing.start : '08:00'}" required></div>
                <div class="form-group"><label>เวลาสิ้นสุด</label><input type="time" id="endI" value="${existing ? existing.end : '10:00'}" required></div>
                <div class="form-group"><label>ระยะเวลา (ชม)</label><input type="number" step="0.5" id="durI" value="${existing ? existing.duration : '2'}" required></div>
                <div class="form-group"><label>ชื่อวิชา</label><input type="text" id="subjI" value="${existing ? existing.subject : ''}" required></div>
                <div class="form-group"><label>รหัสวิชา</label><input type="text" id="codeI" value="${existing ? existing.course_code || '' : ''}"></div>
                <div class="form-group"><label>ห้อง</label><input type="text" id="roomI" value="${existing ? existing.classroom || '' : ''}"></div>
                <div class="form-group"><label>สี</label><input type="color" id="colorI" value="${existing ? existing.color || '#4285F4' : '#4285F4'}"></div>
                <div style="display:flex;gap:10px">
                    <button type="submit" class="btn btn-primary" style="flex:1">บันทึก</button>
                    <button type="button" class="btn btn-secondary" style="flex:1" onclick="closeModal()">ยกเลิก</button>
                </div>
            </form>
        </div>
    </div>`;

    document.body.insertAdjacentHTML('beforeend', modal);

    document.getElementById('sf').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            day: document.getElementById('dayI').value,
            start_time: document.getElementById('startI').value,
            end_time: document.getElementById('endI').value,
            duration: parseFloat(document.getElementById('durI').value),
            subject: document.getElementById('subjI').value,
            course_code: document.getElementById('codeI').value,
            classroom: document.getElementById('roomI').value,
            color: document.getElementById('colorI').value
        };

        try {
            const url = isEdit ? `${API_BASE}/api/schedule/${existing.id}` : `${API_BASE}/api/schedule`;
            const resp = await fetch(url, {
                method: isEdit ? 'PUT' : 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });
            const result = await resp.json();
            if (result.success) {
                closeModal();
                await loadSchedule();
                alert('✅ บันทึกสำเร็จ! ข้อมูลอัปเดตแล้ว');
            } else {
                alert('Error: ' + (result.error || 'Failed'));
            }
        } catch (err) {
            console.error(err);
            alert('Error saving');
        }
    });
}

function closeModal() {
    const m = document.getElementById('scheduleModal');
    if (m) m.remove();
}

async function deleteSchedule(id) {
    if (!confirm('ลบรายการนี้?')) return;

    try {
        const resp = await fetch(`${API_BASE}/api/schedule/${id}`, { method: 'DELETE' });
        const result = await resp.json();
        if (result.success) {
            await loadSchedule();
            alert('✅ ลบสำเร็จ! ข้อมูลอัปเดตแล้ว');
        } else {
            alert('Error: ' + (result.error || 'Failed'));
        }
    } catch (err) {
        console.error(err);
        alert('Error deleting');
    }
}
