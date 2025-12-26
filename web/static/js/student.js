// Student Page JavaScript
// API_BASE is declared in auth.js

let allTeachers = [];

document.addEventListener('DOMContentLoaded', async () => {
    console.log('Student page loaded');
    if (!checkAuth('student')) {
        console.log('Auth failed');
        return;
    }

    const user = getCurrentUser();
    if (user) {
        console.log('Student logged in:', user.name);
    }

    await loadTeachers();

    // ⚡ Real-time WebSocket connection
    const socket = io();
    socket.on('schedule_updated', (data) => {
        console.log('⚡ Real-time update received:', data);
        loadTeachers();  // Reload data instantly!
    });
});

async function loadTeachers() {
    const loading = document.getElementById('loading');
    const teachersList = document.getElementById('teachersList');

    try {
        console.log('Loading teachers...');
        loading.classList.remove('hidden');
        teachersList.innerHTML = '';

        const response = await fetch('/api/teachers');
        console.log('Response status:', response.status);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Teachers loaded:', data.length);

        allTeachers = data;
        applyFilters();

    } catch (error) {
        console.error('Error loading teachers:', error);
        teachersList.innerHTML = '<p class="text-center" style="color: var(--error);">เกิดข้อผิดพลาด: ' + error.message + '</p>';
    } finally {
        loading.classList.add('hidden');
    }
}

function applyFilters() {
    const searchText = document.getElementById('searchInput')?.value.toLowerCase() || '';
    const dayFilter = document.getElementById('dayFilter')?.value || 'all';
    const timeFilter = document.getElementById('timeFilter')?.value || 'all';

    let filtered = allTeachers;

    if (searchText) {
        filtered = filtered.filter(teacher => {
            const name = (teacher.name || '').toLowerCase();
            const subject = (teacher.subject || '').toLowerCase();
            const classrooms = (teacher.classrooms || '').toLowerCase();
            return name.includes(searchText) || subject.includes(searchText) || classrooms.includes(searchText);
        });
    }

    if (dayFilter !== 'all') {
        filtered = filtered.filter(teacher => {
            if (!teacher.schedule || !Array.isArray(teacher.schedule)) return false;
            return teacher.schedule.some(s => s.day === dayFilter);
        });
    }

    if (timeFilter !== 'all') {
        const [startTime, endTime] = timeFilter.split('-');
        filtered = filtered.filter(teacher => {
            if (!teacher.schedule || !Array.isArray(teacher.schedule)) return false;
            return teacher.schedule.some(s => s.start >= startTime && s.start < endTime);
        });
    }

    console.log('Filtered results:', filtered.length);
    renderTeachers(filtered);
}

function renderTeachers(teachers) {
    const teachersList = document.getElementById('teachersList');

    if (!teachers || teachers.length === 0) {
        teachersList.innerHTML = '<p class="text-center" style="color: var(--text-sec);">ไม่พบข้อมูล</p>';
        return;
    }

    teachersList.innerHTML = teachers.map(teacher => createTeacherCard(teacher)).join('');
}

// Helper function to convert day codes to Thai abbreviations
function getDayShortTh(dayCode) {
    const dayMap = {
        'Mon': 'จ.',
        'Tue': 'อ.',
        'Wed': 'พ.',
        'Thu': 'พฤ.',
        'Fri': 'ศ.',
        'Sat': 'ส.',
        'Sun': 'อา.'
    };
    return dayMap[dayCode] || dayCode;
}

function createTeacherCard(teacher) {
    const schedule = teacher.schedule || [];
    const scheduleText = schedule.length > 0
        ? schedule.slice(0, 3).map(s => `${getDayShortTh(s.day)} ${s.start}-${s.end}`).join(', ') + (schedule.length > 3 ? '...' : '')
        : 'ไม่มีตาราง';

    return `
        <div class="card">
            <div class="card-title">${teacher.name || 'ไม่ระบุ'}</div>
            <div class="card-subtitle">${teacher.subject || '-'}</div>
            <div style="margin-top:10px;color:var(--text);">
                <div>📞 ${teacher.contact || '-'}</div>
                <div>🏫 ${teacher.classrooms || '-'}</div>
                <div>📅 ${scheduleText}</div>
            </div>
            <button class="btn btn-primary" style="margin-top:15px;width:100%;" onclick="viewTeacherSchedule(${teacher.id})">
                ดูตารางสอนเต็ม
            </button>
        </div>
    `;
}

function viewTeacherSchedule(teacherId) {
    const teacher = allTeachers.find(t => t.id === teacherId);
    if (!teacher) return;

    const schedule = teacher.schedule || [];

    // Get profile picture path - Support Supabase Storage URLs
    console.log('🔍 [Student Modal] Loading profile picture for:', teacher.name);
    console.log('🔍 [Student Modal] teacher.profile_picture =', teacher.profile_picture);

    let profilePic;
    if (teacher.profile_picture) {
        // Check if it's a Supabase Storage URL (starts with https://)
        if (teacher.profile_picture.startsWith('http://') || teacher.profile_picture.startsWith('https://')) {
            profilePic = teacher.profile_picture;
            console.log('✅ [Student Modal] Using Supabase URL:', profilePic);
        } else {
            // Local path (old data) - show default avatar
            profilePic = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(teacher.name || 'Teacher') + '&size=80&background=BB86FC&color=fff';
            console.log('⚠️ [Student Modal] Local path detected, using default avatar');
        }
    } else {
        // No profile picture - show default avatar
        profilePic = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(teacher.name || 'Teacher') + '&size=80&background=BB86FC&color=fff';
        console.log('⚠️ [Student Modal] No profile_picture, using default avatar');
    }

    const modal = `
        <div style="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.9);display:flex;align-items:center;justify-content:center;z-index:1000;padding:20px" onclick="this.remove()">
            <div style="background:#1E1E1E;border-radius:12px;padding:30px;max-width:95%;width:1200px;max-height:90vh;overflow-y:auto" onclick="event.stopPropagation()">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:20px;padding-bottom:15px;border-bottom:2px solid #BB86FC">
                    <div style="display:flex;align-items:center;gap:20px;flex:1">
                        <!-- Profile Picture - Left -->
                        <img src="${profilePic}" 
                             alt="Profile" 
                             style="width:80px;height:80px;border-radius:50%;object-fit:cover;border:3px solid #BB86FC;flex-shrink:0"
                             onerror="this.src='data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 width=%2280%22 height=%2280%22%3E%3Ccircle fill=%22%23e0e0e0%22 cx=%2240%22 cy=%2240%22 r=%2240%22/%3E%3Ctext x=%2250%25%22 y=%2250%25%22 dominant-baseline=%22middle%22 text-anchor=%22middle%22 font-size=%2230%22 fill=%22%23999%22%3E👤%3C/text%3E%3C/svg%3E';">
                        
                        <!-- Teacher Info - Right -->
                        <div style="flex:1;min-width:0">
                            <h2 style="color:#BB86FC;margin:0;font-size:22px">${teacher.name}</h2>
                            <p style="margin:10px 0 0 0;color:#B0B0B0;font-size:14px">📚 ${teacher.subject || '-'} | 📍 ${teacher.classrooms || '-'} | 🕒 ${teacher.contact || '-'}</p>
                        </div>
                    </div>
                    <button class="btn btn-secondary" style="padding:8px 20px;flex-shrink:0" onclick="this.closest('div[style*=fixed]').remove()">← ย้อนกลับ</button>
                </div>
                <div id="teacherGridContainer" style="overflow-x:auto"></div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modal);
    renderTeacherGrid(schedule);
}

function renderTeacherGrid(schedule) {
    const container = document.getElementById('teacherGridContainer');
    if (!container) return;

    const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const DAY_NAMES = { 'Mon': 'จันทร์', 'Tue': 'อังคาร', 'Wed': 'พุธ', 'Thu': 'พฤหัสบดี', 'Fri': 'ศุกร์', 'Sat': 'เสาร์' };
    const TIME_SLOTS = ['08:30 - 09:30', '09:30 - 10:30', '10:30 - 11:30', '11:30 - 12:30', '12:30 - 13:30', '13:30 - 14:30', '14:30 - 15:30', '15:30 - 16:30', '16:30 - 17:30', '17:30 - 18:30'];

    const DAY_COL_WIDTH = 100;
    const TIME_COL_WIDTH = 100;
    const ROW_HEIGHT = 60;
    const HEADER_HEIGHT = 50;

    let html = '<div style="background:#252525;min-width:fit-content">';

    // Header row - Time slots
    html += '<div style="display:grid;grid-template-columns:' + DAY_COL_WIDTH + 'px repeat(' + TIME_SLOTS.length + ',' + TIME_COL_WIDTH + 'px);background:#252525;height:' + HEADER_HEIGHT + 'px;border-bottom:1px solid #2C2C2C">';
    html += '<div></div>'; // Empty corner

    TIME_SLOTS.forEach(time => {
        html += `<div style="display:flex;align-items:center;justify-content:center;color:#BB86FC;font-weight:bold;font-size:10px;border-left:1px solid #2C2C2C">${time}</div>`;
    });
    html += '</div>';

    // Day rows
    DAYS.forEach((day, dayIdx) => {
        const rowBg = dayIdx % 2 === 0 ? '#1E1E1E' : '#191919';
        html += `<div style="display:grid;grid-template-columns:${DAY_COL_WIDTH}px repeat(${TIME_SLOTS.length},${TIME_COL_WIDTH}px);height:${ROW_HEIGHT}px;background:${rowBg};border-bottom:1px solid #2C2C2C;position:relative">`;

        // Day name column
        html += `<div style="display:flex;align-items:center;justify-content:center;font-weight:bold;color:#FFFFFF;border-right:2px solid #2C2C2C">${DAY_NAMES[day]}</div>`;

        // Time cells
        TIME_SLOTS.forEach(() => {
            html += '<div style="border-left:1px solid #2C2C2C"></div>';
        });

        html += '</div>';
    });

    html += '</div>';
    container.innerHTML = html;

    // Place classes on grid (similar to Python version)
    const gridContainer = container.firstChild;

    schedule.forEach(item => {
        const dayIdx = DAYS.indexOf(item.day);
        if (dayIdx === -1) return;

        // Parse start time
        const [startH, startM] = item.start.split(':').map(Number);
        const currentH = startH + (startM / 60);
        const baseH = 8.5; // 08:30
        const offsetHours = currentH - baseH;

        // Calculate position
        const xStart = DAY_COL_WIDTH + (offsetHours * TIME_COL_WIDTH);
        const duration = parseFloat(item.duration) || 0;
        const width = duration * TIME_COL_WIDTH;

        // Find the row element
        const rowElement = gridContainer.children[dayIdx + 1]; // +1 for header
        if (!rowElement) return;

        // Create class block
        const block = document.createElement('div');
        block.style.cssText = `
            position:absolute;
            left:${xStart}px;
            top:8px;
            width:${width}px;
            height:${ROW_HEIGHT - 16}px;
            background:${item.color || '#4285F4'};
            border-radius:6px;
            padding:8px;
            color:white;
            font-size:9px;
            overflow:hidden;
            display:flex;
            flex-direction:column;
            justify-content:center;
            align-items:center;
            text-align:center;
            box-shadow:0 2px 4px rgba(0,0,0,0.3);
            cursor:pointer;
        `;

        let content = `<div style="font-weight:bold;margin-bottom:2px;font-size:9px">${item.subject}</div>`;
        if (item.course_code) {
            content += `<div style="font-size:8px">${item.course_code}</div>`;
        }
        if (item.classroom) {
            content += `<div style="font-size:8px">🚪 ${item.classroom}</div>`;
        }

        block.innerHTML = content;
        block.title = `${item.subject}\n${item.start}-${item.end}\n${item.course_code || ''}\n${item.classroom || ''}`;

        // Add click handler to show color picker popup
        block.onclick = (e) => {
            e.stopPropagation();
            showClassDetailsInStudentView(item);
        };

        rowElement.appendChild(block);
    });
}

// Show class details popup (read-only for students)
function showClassDetailsInStudentView(classItem) {
    const DAY_NAMES_TH = { 'Mon': 'จันทร์', 'Tue': 'อังคาร', 'Wed': 'พุธ', 'Thu': 'พฤหัสบดี', 'Fri': 'ศุกร์', 'Sat': 'เสาร์' };

    const modal = `
        <div id="classDetailModal" style="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.8);display:flex;align-items:center;justify-content:center;z-index:10000;padding:20px" onclick="this.remove()">
            <div style="background:var(--card-bg);border-radius:12px;padding:30px;max-width:400px;width:100%" onclick="event.stopPropagation()">
                <h2 style="color:var(--primary);margin-bottom:20px">${classItem.subject}</h2>
                <p style="margin:10px 0"><strong>รหัสวิชา:</strong> ${classItem.course_code || '-'}</p>
                <p style="margin:10px 0"><strong>วัน:</strong> ${DAY_NAMES_TH[classItem.day]}</p>
                <p style="margin:10px 0"><strong>เวลา:</strong> ${classItem.start} - ${classItem.end}</p>
                <p style="margin:10px 0"><strong>ห้อง:</strong> ${classItem.classroom || '-'}</p>
                <p style="margin:10px 0"><strong>ระยะเวลา:</strong> ${classItem.duration} ชั่วโมง</p>
                
                <button class="btn btn-secondary" style="margin-top:20px;width:100%" onclick="this.closest('#classDetailModal').remove()">ปิด</button>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modal);
}

// (Removed) Color picker functionality - students can only view class details
/*async function saveScheduleColorInStudentView(scheduleId, newColor) {
    try {
        const response = await fetch(`/api/schedule/${scheduleId}/color`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ color: newColor })
        });

        const result = await response.json();

        if (result.success) {
            // Close the modal
            document.getElementById('classDetailModal')?.remove();

            // Show success message
            showToastInStudentView('✅ บันทึกสีสำเร็จ!', 'success');

            // Update color in DOM immediately - NO RELOAD!
            // Find all blocks in the grid and update the matching one
            const allBlocks = document.querySelectorAll('[style*="position:absolute"]');
            allBlocks.forEach(block => {
                // Check if this block's title matches (simple approach)
                if (block.querySelector && block.style.background) {
                    block.style.background = newColor;
                }
            });
        } else {
            showToastInStudentView('❌ เกิดข้อผิดพลาด: ' + (result.error || 'ไม่สามารถบันทึกได้'), 'error');
        }
    } catch (error) {
        console.error('Error saving color:', error);
        showToastInStudentView('❌ เกิดข้อผิดพลาดในการบันทึก', 'error');
    }
}

// (Removed) Toast notification - no longer needed
/*function showToastInStudentView(message, type = 'info') {
    const bgColor = type === 'success' ? '#0F9D58' : type === 'error' ? '#CF6679' : '#4285F4';
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${bgColor};
        color: white;
        padding: 15px 25px;
        border-radius: 8px;
        font-weight: bold;
        z-index: 10000;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        animation: slideIn 0.3s ease-out;
    `;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => toast.remove(), 300);
    }, 2500);
}*/
// Export Schedule to PDF
// Export Schedule to PDF - FULL PAGE VERSION
