// Admin User Management
const API_BASE = '';

let currentTab = 'teachers';
let teachers = [];
let students = [];

document.addEventListener('DOMContentLoaded', async () => {
    if (!checkAuth('teacher')) return;

    await loadTeachers();
    await loadStudents();
});

function switchTab(tab) {
    currentTab = tab;

    document.querySelectorAll('.view-toggle-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    document.getElementById('teachersSection').classList.toggle('hidden', tab !== 'teachers');
    document.getElementById('studentsSection').classList.toggle('hidden', tab !== 'students');
}

async function loadTeachers() {
    try {
        const response = await fetch(`${API_BASE}/api/users/teachers`);
        teachers = await response.json();
        renderTeachers();
    } catch (error) {
        console.error('Error loading teachers:', error);
    }
}

async function loadStudents() {
    try {
        const response = await fetch(`${API_BASE}/api/users/students`);
        students = await response.json();
        renderStudents();
    } catch (error) {
        console.error('Error loading students:', error);
    }
}

function renderTeachers() {
    const container = document.getElementById('teachersList');

    if (teachers.length === 0) {
        container.innerHTML = '<p class="text-center">ไม่มีข้อมูลอาจารย์</p>';
        return;
    }

    container.innerHTML = teachers.map(t => `
        <div class="card">
            <div class="card-title">${t.name}</div>
            <div class="card-subtitle">@${t.username}</div>
            <div class="card-subtitle">${t.subject || '-'}</div>
            <div class="card-info">📍 ${t.room || '-'} | 📞 ${t.contact || '-'}</div>
            <div style="display:flex;gap:10px;margin-top:10px">
                <button class="btn btn-primary" style="flex:1;padding:6px 12px" onclick="openEditTeacherDialog(${t.id})">แก้ไข</button>
                <button class="btn btn-danger" style="flex:1;padding:6px 12px" onclick="deleteTeacher(${t.id}, '${t.name}')">ลบ</button>
            </div>
        </div>
    `).join('');
}

function renderStudents() {
    const container = document.getElementById('studentsList');

    if (students.length === 0) {
        container.innerHTML = '<p class="text-center">ไม่มีข้อมูลนักศึกษา</p>';
        return;
    }

    container.innerHTML = students.map(s => `
        <div class="card">
            <div class="card-title">${s.name}</div>
            <div class="card-subtitle">@${s.username}</div>
            <div style="display:flex;gap:10px;margin-top:10px">
                <button class="btn btn-primary" style="flex:1;padding:6px 12px" onclick="openEditStudentDialog(${s.id})">แก้ไข</button>
                <button class="btn btn-danger" style="flex:1;padding:6px 12px" onclick="deleteStudent(${s.id}, '${s.name}')">ลบ</button>
            </div>
        </div>
    `).join('');
}

function openAddTeacherDialog() {
    const modal = `
        <div id="userModal" style="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.8);display:flex;align-items:center;justify-content:center;z-index:1000;padding:20px">
            <div style="background:var(--card-bg);border-radius:12px;padding:30px;max-width:500px;width:100%;max-height:90vh;overflow-y:auto">
                <h2 style="color:var(--primary);margin-bottom:20px">เพิ่มอาจารย์</h2>
                <form id="teacherForm" style="display:flex;flex-direction:column;gap:15px">
                    <div class="form-group">
                        <label>ชื่อผู้ใช้</label>
                        <input type="text" id="username" required>
                    </div>
                    <div class="form-group">
                        <label>รหัสผ่าน</label>
                        <input type="password" id="password" required>
                    </div>
                    <div class="form-group">
                        <label>ชื่อ-นามสกุล</label>
                        <input type="text" id="name" required>
                    </div>
                    <div class="form-group">
                        <label>แผนกวิชา</label>
                        <input type="text" id="subject">
                    </div>
                    <div class="form-group">
                        <label>เบอร์ติดต่อ</label>
                        <input type="text" id="contact">
                    </div>
                    <div class="form-group">
                        <label>ห้องพัก</label>
                        <input type="text" id="room">
                    </div>
                    <div style="display:flex;gap:10px">
                        <button type="submit" class="btn btn-primary" style="flex:1">บันทึก</button>
                        <button type="button" class="btn btn-secondary" style="flex:1" onclick="closeModal()">ยกเลิก</button>
                    </div>
                </form>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modal);

    document.getElementById('teacherForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const data = {
            username: document.getElementById('username').value,
            password: document.getElementById('password').value,
            name: document.getElementById('name').value,
            subject: document.getElementById('subject').value,
            contact: document.getElementById('contact').value,
            room: document.getElementById('room').value
        };

        try {
            console.log('🔍 Adding teacher:', data);

            const response = await fetch(`${API_BASE}/api/admin/teachers`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            console.log('📡 Response status:', response.status);
            const result = await response.json();
            console.log('📦 Result:', result);

            if (result.success) {
                closeModal();
                await loadTeachers();
                alert('✅ เพิ่มอาจารย์สำเร็จ!');
            } else {
                alert('❌ เพิ่มไม่สำเร็จ: ' + (result.error || 'Unknown error'));
            }
        } catch (error) {
            console.error('❌ Error:', error);
            alert('เกิดข้อผิดพลาด: ' + error.message);
        }
    });
}

function openAddStudentDialog() {
    const modal = `
        <div id="userModal" style="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.8);display:flex;align-items:center;justify-content:center;z-index:1000;padding:20px">
            <div style="background:var(--card-bg);border-radius:12px;padding:30px;max-width:500px;width:100%;max-height:90vh;overflow-y:auto">
                <h2 style="color:var(--primary);margin-bottom:20px">เพิ่มนักศึกษา</h2>
                <form id="studentForm" style="display:flex;flex-direction:column;gap:15px">
                    <div class="form-group">
                        <label>ชื่อผู้ใช้</label>
                        <input type="text" id="username" required>
                    </div>
                    <div class="form-group">
                        <label>รหัสผ่าน</label>
                        <input type="password" id="password" required>
                    </div>
                    <div class="form-group">
                        <label>ชื่อ-นามสกุล</label>
                        <input type="text" id="name" required>
                    </div>
                    <div style="display:flex;gap:10px">
                        <button type="submit" class="btn btn-primary" style="flex:1">บันทึก</button>
                        <button type="button" class="btn btn-secondary" style="flex:1" onclick="closeModal()">ยกเลิก</button>
                    </div>
                </form>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modal);

    document.getElementById('studentForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const data = {
            username: document.getElementById('username').value,
            password: document.getElementById('password').value,
            name: document.getElementById('name').value
        };

        try {
            const response = await fetch(`${API_BASE}/api/admin/students`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                closeModal();
                await loadStudents();
                alert('✅ เพิ่มนักศึกษาสำเร็จ! ข้อมูลอัปเดตแล้ว');
            } else {
                alert('Error: ' + (result.error || 'Failed'));
            }
        } catch (error) {
            console.error(error);
            alert('เกิดข้อผิดพลาด');
        }
    });
}

async function deleteTeacher(id, name) {
    if (!confirm(`ลบอาจารย์ ${name}?`)) return;

    try {
        const response = await fetch(`${API_BASE}/api/admin/teachers/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (result.success) {
            await loadTeachers();
            alert('✅ ลบอาจารย์สำเร็จ! ข้อมูลอัปเดตแล้ว');
        } else {
            alert('Error: ' + (result.error || 'Failed'));
        }
    } catch (error) {
        console.error(error);
        alert('เกิดข้อผิดพลาด');
    }
}

async function deleteStudent(id, name) {
    if (!confirm(`ลบนักศึกษา ${name}?`)) return;

    try {
        const response = await fetch(`${API_BASE}/api/admin/students/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (result.success) {
            await loadStudents();
            alert('✅ ลบนักศึกษาสำเร็จ! ข้อมูลอัปเดตแล้ว');
        } else {
            alert('Error: ' + (result.error || 'Failed'));
        }
    } catch (error) {
        console.error(error);
        alert('เกิดข้อผิดพลาด');
    }
}

function openEditTeacherDialog(id) {
    const teacher = teachers.find(t => t.id === id);
    if (!teacher) return;

    const modal = `
        <div id="userModal" style="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.8);display:flex;align-items:center;justify-content:center;z-index:1000;padding:20px">
            <div style="background:var(--card-bg);border-radius:12px;padding:30px;max-width:500px;width:100%;max-height:90vh;overflow-y:auto">
                <h2 style="color:var(--primary);margin-bottom:20px">แก้ไขอาจารย์</h2>
                <form id="editTeacherForm" style="display:flex;flex-direction:column;gap:15px">
                    <div class="form-group">
                        <label>ชื่อผู้ใช้</label>
                        <input type="text" id="username" value="${teacher.username}" required>
                    </div>
                    <div class="form-group">
                        <label>รหัสผ่าน (เว้นว่างถ้าไม่ต้องการเปลี่ยน)</label>
                        <input type="password" id="password" placeholder="ใส่รหัสผ่านใหม่">
                    </div>
                    <div class="form-group">
                        <label>ชื่อ-นามสกุล</label>
                        <input type="text" id="name" value="${teacher.name}" required>
                    </div>
                    <div class="form-group">
                        <label>แผนกวิชา</label>
                        <input type="text" id="subject" value="${teacher.subject || ''}">
                    </div>
                    <div class="form-group">
                        <label>เบอร์ติดต่อ</label>
                        <input type="text" id="contact" value="${teacher.contact || ''}">
                    </div>
                    <div class="form-group">
                        <label>ห้องพัก</label>
                        <input type="text" id="room" value="${teacher.room || ''}">
                    </div>
                    <div style="display:flex;gap:10px">
                        <button type="submit" class="btn btn-primary" style="flex:1">บันทึก</button>
                        <button type="button" class="btn btn-secondary" style="flex:1" onclick="closeModal()">ยกเลิก</button>
                    </div>
                </form>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modal);

    document.getElementById('editTeacherForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const data = {
            username: document.getElementById('username').value,
            name: document.getElementById('name').value,
            subject: document.getElementById('subject').value,
            contact: document.getElementById('contact').value,
            room: document.getElementById('room').value
        };

        const password = document.getElementById('password').value;
        if (password) data.password = password;

        try {
            const response = await fetch(`${API_BASE}/api/admin/teachers/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                closeModal();
                await loadTeachers();
                alert('✅ แก้ไขข้อมูลเรียบร้อย');
            } else {
                alert('Error: ' + (result.error || 'Failed'));
            }
        } catch (error) {
            console.error(error);
            alert('เกิดข้อผิดพลาด');
        }
    });
}

function openEditStudentDialog(id) {
    const student = students.find(s => s.id === id);
    if (!student) return;

    const modal = `
        <div id="userModal" style="position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.8);display:flex;align-items:center;justify-content:center;z-index:1000;padding:20px">
            <div style="background:var(--card-bg);border-radius:12px;padding:30px;max-width:500px;width:100%;max-height:90vh;overflow-y:auto">
                <h2 style="color:var(--primary);margin-bottom:20px">แก้ไขนักศึกษา</h2>
                <form id="editStudentForm" style="display:flex;flex-direction:column;gap:15px">
                    <div class="form-group">
                        <label>ชื่อผู้ใช้</label>
                        <input type="text" id="username" value="${student.username}" required>
                    </div>
                    <div class="form-group">
                        <label>รหัสผ่าน (เว้นว่างถ้าไม่ต้องการเปลี่ยน)</label>
                        <input type="password" id="password" placeholder="ใส่รหัสผ่านใหม่">
                    </div>
                    <div class="form-group">
                        <label>ชื่อ-นามสกุล</label>
                        <input type="text" id="name" value="${student.name}" required>
                    </div>
                    <div style="display:flex;gap:10px">
                        <button type="submit" class="btn btn-primary" style="flex:1">บันทึก</button>
                        <button type="button" class="btn btn-secondary" style="flex:1" onclick="closeModal()">ยกเลิก</button>
                    </div>
                </form>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modal);

    document.getElementById('editStudentForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const data = {
            username: document.getElementById('username').value,
            name: document.getElementById('name').value
        };

        const password = document.getElementById('password').value;
        if (password) data.password = password;

        try {
            const response = await fetch(`${API_BASE}/api/admin/students/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                closeModal();
                await loadStudents();
                alert('✅ แก้ไขข้อมูลเรียบร้อย');
            } else {
                alert('Error: ' + (result.error || 'Failed'));
            }
        } catch (error) {
            console.error(error);
            alert('เกิดข้อผิดพลาด');
        }
    });
}

function closeModal() {
    const modal = document.getElementById('userModal');
    if (modal) modal.remove();
}
