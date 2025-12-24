// Student Dashboard JavaScript
// API_BASE is declared in auth.js

const DAY_NAMES = {
    'Mon': 'จันทร์',
    'Tue': 'อังคาร',
    'Wed': 'พุธ',
    'Thu': 'พฤหัสบดี',
    'Fri': 'ศุกร์',
    'Sat': 'เสาร์'
};

const DAYS_ORDER = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

document.addEventListener('DOMContentLoaded', async () => {
    if (!checkAuth('student')) return;

    // Display student name
    const user = getCurrentUser();
    if (user) {
        document.getElementById('studentName').textContent = user.name;
    }

    await loadAllSchedules();
});

async function loadAllSchedules() {
    const loading = document.getElementById('loading');
    const container = document.getElementById('scheduleByDay');

    try {
        loading.classList.remove('hidden');

        const response = await fetch(`${API_BASE}/api/all-schedules`);
        const allSchedules = await response.json();

        console.log('All schedules:', allSchedules);

        // Group by day
        const scheduleByDay = {};
        DAYS_ORDER.forEach(day => scheduleByDay[day] = []);

        allSchedules.forEach(item => {
            if (item.day && scheduleByDay[item.day]) {
                scheduleByDay[item.day].push(item);
            }
        });

        // Render by day
        let html = '';
        DAYS_ORDER.forEach(day => {
            const classes = scheduleByDay[day];
            if (classes.length > 0) {
                html += `
                    <div style="margin-bottom: 30px;">
                        <div style="background: var(--primary); padding: 12px 20px; border-radius: 8px; margin-bottom: 10px;">
                            <h3 style="margin: 0; color: white;">${DAY_NAMES[day]}</h3>
                        </div>
                        <div class="cards-container">
                            ${classes.sort((a, b) => a.start.localeCompare(b.start)).map(c => createScheduleCard(c)).join('')}
                        </div>
                    </div>
                `;
            }
        });

        if (html === '') {
            container.innerHTML = '<p class="text-center" style="color: var(--text-sec);">ยังไม่มีตารางเรียน</p>';
        } else {
            container.innerHTML = html;
        }

    } catch (error) {
        console.error('Error loading schedules:', error);
        container.innerHTML = '<p class="text-center" style="color: var(--error);">เกิดข้อผิดพลาดในการโหลดข้อมูล</p>';
    } finally {
        loading.classList.add('hidden');
    }
}

function createScheduleCard(schedule) {
    const teacher = schedule.teacher_name || 'ไม่ระบุ';
    const subject = schedule.subject || 'ไม่ระบุ';
    const time = `${schedule.start} - ${schedule.end}`;
    const room = schedule.classroom || '-';
    const code = schedule.course_code || '-';

    return `
        <div class="card">
            <div class="card-title">${subject}</div>
            <div class="card-subtitle">อาจารย์: ${teacher}</div>
            <div style="margin-top: 8px; color: var(--text);">
                <span>⏰ ${time} (${schedule.duration}h)</span>
                <span style="margin-left: 15px;">🏫 ${room}</span>
                <span style="margin-left: 15px;">📚 ${code}</span>
            </div>
        </div>
    `;
}
