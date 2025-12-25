// Teacher Dashboard JavaScript
// API_BASE is declared in auth.js

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Teacher dashboard loaded');

    if (!checkAuth('teacher')) {
        console.log('Auth failed');
        return;
    }

    // Load teacher profile
    await loadTeacherProfile();

    // Load schedule data
    await loadDashboardData();

    // ⚡ Real-time WebSocket connection
    const socket = io();
    socket.on('schedule_updated', (data) => {
        console.log('⚡ Dashboard real-time update:', data);
        loadDashboardData();  // Reload instantly!
    });
});

async function loadTeacherProfile() {
    try {
        const response = await fetch('/api/profile');
        if (response.ok) {
            const teacher = await response.json();

            // Update profile info
            document.getElementById('teacherName').textContent = teacher.name || 'อาจารย์';
            document.getElementById('teacherSubject').textContent = teacher.subject || '-';
            document.getElementById('teacherContact').textContent = teacher.contact || '-';

            // Load profile picture
            const profilePicElement = document.getElementById('teacherProfilePic');
            console.log('🔍 DEBUG: teacher.profile_picture =', teacher.profile_picture);

            if (teacher.profile_picture) {
                // Check if it's a Supabase Storage URL (starts with https://)
                if (teacher.profile_picture.startsWith('http://') || teacher.profile_picture.startsWith('https://')) {
                    console.log('✅ Using Supabase URL:', teacher.profile_picture);
                    profilePicElement.src = teacher.profile_picture;
                } else {
                    console.log('⚠️ Using default avatar (local path detected):', teacher.profile_picture);
                    // Local path (old data) - show default avatar
                    profilePicElement.src = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(teacher.name || 'Teacher') + '&size=200&background=4285F4&color=fff';
                }
            } else {
                console.log('⚠️ No profile picture - using default avatar');
                // No profile picture - show default avatar
                profilePicElement.src = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(teacher.name || 'Teacher') + '&size=200&background=4285F4&color=fff';
            }

            // Load schedule to get classrooms
            const scheduleResponse = await fetch('/api/schedule');
            if (scheduleResponse.ok) {
                const schedule = await scheduleResponse.json();

                // Aggregate unique classrooms from schedule
                const classrooms = new Set();
                schedule.forEach(item => {
                    if (item.classroom) {
                        classrooms.add(item.classroom);
                    }
                });

                // Display classrooms
                if (classrooms.size > 0) {
                    document.getElementById('teacherRoom').textContent = Array.from(classrooms).sort().join(', ');
                } else {
                    document.getElementById('teacherRoom').textContent = '-';
                }
            } else {
                document.getElementById('teacherRoom').textContent = '-';
            }
        }
    } catch (error) {
        console.error('Error loading teacher profile:', error);
    }
}

async function loadDashboardData() {
    const loading = document.getElementById('loading');
    const overview = document.getElementById('scheduleOverview');

    try {
        loading.classList.remove('hidden');

        const response = await fetch('/api/schedule');
        console.log('Response status:', response.status);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const schedule = await response.json();
        console.log('Schedule loaded:', schedule.length);

        // Update total classes counter
        document.getElementById('totalClasses').textContent = schedule.length;

        // Calculate total days with classes
        const uniqueDays = new Set(schedule.map(s => s.day));
        document.getElementById('totalDays').textContent = uniqueDays.size;

        // Group by day
        const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        const dayNames = {
            'Mon': 'จันทร์',
            'Tue': 'อังคาร',
            'Wed': 'พุธ',
            'Thu': 'พฤหัสบดี',
            'Fri': 'ศุกร์',
            'Sat': 'เสาร์'
        };

        const scheduleByDay = {};
        days.forEach(day => scheduleByDay[day] = []);

        schedule.forEach(item => {
            if (item.day && scheduleByDay[item.day]) {
                scheduleByDay[item.day].push(item);
            }
        });

        // Render overview
        let html = '';
        days.forEach(day => {
            const classes = scheduleByDay[day];
            if (classes.length > 0) {
                html += `
                    <div style="margin-bottom:20px">
                        <div style="background:var(--primary);padding:10px 15px;border-radius:8px;margin-bottom:10px">
                            <strong style="color:white">${dayNames[day]}</strong>
                        </div>
                        <div class="cards-container">
                            ${classes.sort((a, b) => a.start.localeCompare(b.start)).map(c => createClassCard(c)).join('')}
                        </div>
                    </div>
                `;
            }
        });

        if (html === '') {
            overview.innerHTML = '<p style="color:var(--text-sec);text-align:center">ยังไม่มีตารางสอน</p>';
        } else {
            overview.innerHTML = html;
        }

    } catch (error) {
        console.error('Error loading dashboard:', error);
        overview.innerHTML = '<p style="color:var(--error);text-align:center">เกิดข้อผิดพลาดในการโหลดข้อมูล</p>';
    } finally {
        loading.classList.add('hidden');
    }
}

function createClassCard(classItem) {
    return `
        <div class="card">
            <div class="card-title">${classItem.subject}</div>
            <div style="margin-top:10px;color:var(--text)">
                <div>⏰ ${classItem.start} - ${classItem.end} (${classItem.duration}h)</div>
                <div style="margin-top:5px">📚 ${classItem.course_code || '-'}</div>
                <div>🏫 ${classItem.classroom || '-'}</div>
            </div>
        </div>
    `;
}
