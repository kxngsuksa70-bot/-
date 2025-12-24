// Schedule Grid Renderer
const API_BASE = '';

const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
const DAY_NAMES_TH = {
    'Mon': 'จันทร์',
    'Tue': 'อังคาร',
    'Wed': 'พุธ',
    'Thu': 'พฤหัสบดี',
    'Fri': 'ศุกร์',
    'Sat': 'เสาร์'
};

const TIME_SLOTS = [
    '08:00', '09:00', '10:00', '11:00', '12:00',
    '13:00', '14:00', '15:00', '16:00', '17:00'
];

function timeToMinutes(time) {
    const [hours, minutes] = time.split(':').map(Number);
    return hours * 60 + minutes;
}

function calculateGridPosition(startTime, endTime) {
    const startMins = timeToMinutes(startTime);
    const endMins = timeToMinutes(endTime);
    const baseTime = timeToMinutes('08:00');
    const pixelsPerHour = 60;

    const top = ((startMins - baseTime) / 60) * pixelsPerHour;
    const height = ((endMins - startMins) / 60) * pixelsPerHour;

    return { top, height };
}

function renderScheduleGrid(scheduleData, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    let html = '<div class="schedule-grid">';

    // Header row
    html += '<div class="grid-header">Time</div>';
    DAYS.forEach(day => {
        html += `<div class="grid-header">${DAY_NAMES_TH[day]}</div>`;
    });

    // Time rows
    TIME_SLOTS.forEach((time, idx) => {
        html += `<div class="grid-time-label">${time}</div>`;

        DAYS.forEach(day => {
            const cellId = `cell-${day}-${idx}`;
            html += `<div class="grid-cell" id="${cellId}"></div>`;
        });
    });

    html += '</div>';
    container.innerHTML = html;

    console.log('Grid rendered, placing classes...');

    // Place classes on the grid
    scheduleData.forEach(item => {
        console.log('Placing:', item.subject, 'on', item.day);

        const pos = calculateGridPosition(item.start, item.end);
        const dayIndex = DAYS.indexOf(item.day);

        if (dayIndex === -1) {
            console.warn('Invalid day:', item.day);
            return;
        }

        // Get all cells for this day column
        const dayCells = [];
        for (let i = 0; i < TIME_SLOTS.length; i++) {
            const cell = document.getElementById(`cell-${item.day}-${i}`);
            if (cell) dayCells.push(cell);
        }

        if (dayCells.length === 0) {
            console.warn('No cells found for', item.day);
            return;
        }

        // Use the first cell as parent and position absolutely
        const parentCell = dayCells[0];

        const classDiv = document.createElement('div');
        classDiv.className = 'grid-class';
        classDiv.dataset.scheduleId = item.id;  // Add this for later color update
        classDiv.style.top = `${pos.top}px`;
        classDiv.style.height = `${pos.height}px`;
        classDiv.style.backgroundColor = item.color || '#4285F4';

        classDiv.innerHTML = `
            <div class="grid-class-title">${item.subject}</div>
            <div class="grid-class-code">${item.course_code || ''}</div>
            <div class="grid-class-room">${item.classroom || ''}</div>
        `;

        classDiv.onclick = () => showClassDetails(item);
        parentCell.appendChild(classDiv);

        console.log('Placed', item.subject, 'at top:', pos.top, 'height:', pos.height);
    });
}

function showClassDetails(classItem) {
    const currentColor = classItem.color || '#4285F4';

    const modal = `
        <div id="classDetailModal" style="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.8);display:flex;align-items:center;justify-content:center;z-index:1000;padding:20px" onclick="this.remove()">
            <div style="background:var(--card-bg);border-radius:12px;padding:30px;max-width:400px;width:100%" onclick="event.stopPropagation()">
                <h2 style="color:var(--primary);margin-bottom:20px">${classItem.subject}</h2>
                <p style="margin:10px 0"><strong>รหัสวิชา:</strong> ${classItem.course_code || '-'}</p>
                <p style="margin:10px 0"><strong>วัน:</strong> ${DAY_NAMES_TH[classItem.day]}</p>
                <p style="margin:10px 0"><strong>เวลา:</strong> ${classItem.start} - ${classItem.end}</p>
                <p style="margin:10px 0"><strong>ห้อง:</strong> ${classItem.classroom || '-'}</p>
                <p style="margin:10px 0"><strong>ระยะเวลา:</strong> ${classItem.duration} ชั่วโมง</p>
                
                <!-- Color Picker Section -->
                <div style="margin-top:25px;padding-top:20px;border-top:1px solid rgba(187,134,252,0.3)">
                    <p style="margin-bottom:10px"><strong>🎨 เปลี่ยนสีรายวิชา:</strong></p>
                    <div style="display:flex;gap:10px;align-items:center">
                        <input type="color" id="colorPicker" value="${currentColor}" style="width:60px;height:40px;border:2px solid var(--primary);border-radius:8px;cursor:pointer">
                        <div id="colorPreview" style="flex:1;height:40px;background:${currentColor};border-radius:8px;display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:12px">${currentColor.toUpperCase()}</div>
                    </div>
                    <button class="btn btn-primary" id="saveColorBtn" style="margin-top:15px;width:100%" onclick="saveScheduleColor(${classItem.id}, document.getElementById('colorPicker').value)">
                        💾 บันทึกสี
                    </button>
                </div>
                
                <button class="btn btn-secondary" style="margin-top:15px;width:100%" onclick="this.closest('#classDetailModal').remove()">ปิด</button>
            </div>
        </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modal);

    // Update color preview when color picker changes
    document.getElementById('colorPicker').addEventListener('input', (e) => {
        const preview = document.getElementById('colorPreview');
        preview.style.background = e.target.value;
        preview.textContent = e.target.value.toUpperCase();
    });
}

// Save schedule color to database
async function saveScheduleColor(scheduleId, newColor) {
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

            //Show success message
            showToast('✅ บันทึกสีสำเร็จ!', 'success');

            // Update color in DOM immediately - NO RELOAD NEEDED!
            document.querySelectorAll(`[data-schedule-id="${scheduleId}"]`).forEach(block => {
                block.style.backgroundColor = newColor;
            });
        } else {
            showToast('❌ เกิดข้อผิดพลาด: ' + (result.error || 'ไม่สามารถบันทึกได้'), 'error');
        }
    } catch (error) {
        console.error('Error saving color:', error);
        showToast('❌ เกิดข้อผิดพลาดในการบันทึก', 'error');
    }
}

// Toast notification helper
function showToast(message, type = 'info') {
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
}

// Export for use in other files
if (typeof window !== 'undefined') {
    window.renderScheduleGrid = renderScheduleGrid;
}
