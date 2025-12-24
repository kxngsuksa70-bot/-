// Authentication JavaScript
const API_BASE = '';

// Login Page Logic
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');

    // Login form submission
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            try {
                // Try teacher first
                let response = await fetch(`${API_BASE}/api/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username,
                        password,
                        role: 'teacher'
                    })
                });

                let data = await response.json();

                // If teacher login fails, try student
                if (!data.success) {
                    response = await fetch(`${API_BASE}/api/login`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            username,
                            password,
                            role: 'student'
                        })
                    });

                    data = await response.json();
                }

                if (data.success) {
                    // Store user data
                    localStorage.setItem('user', JSON.stringify(data.user));
                    localStorage.setItem('role', data.role);

                    // Show guide for students (if not disabled)
                    if (data.role === 'student' && !localStorage.getItem('hideStudentGuide')) {
                        showGuidePopup(() => {
                            window.location.href = data.redirect;
                        });
                    } else {
                        // Redirect
                        window.location.href = data.redirect;
                    }
                } else {
                    errorMessage.textContent = 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง';
                    errorMessage.style.display = 'block';
                }
            } catch (error) {
                console.error('Login error:', error);
                errorMessage.textContent = 'เกิดข้อผิดพลาดในการเชื่อมต่อ';
                errorMessage.style.display = 'block';
            }
        });
    }
});

// Show Guide Popup for Students
function showGuidePopup(onClose = null) {
    displayPopup();

    function displayPopup() {
        const popup = document.createElement('div');
        popup.className = 'guide-popup-overlay';
        popup.innerHTML = `
            <div class="guide-popup-content">
                <div class="guide-popup-header">
                    <h2>📖 คู่มือการใช้งาน</h2>
                    <button class="guide-popup-close" onclick="closeGuidePopup()">✕ ปิด</button>
                </div>
                <div class="guide-popup-body">
                    <div style="text-align: center; padding: 20px;">
                        <h3 style="color: var(--primary); margin-bottom: 20px; font-size: 24px;">📱 คู่มือการใช้งาน Application</h3>
                        <a href="https://www.canva.com/design/DAG7j7qeW4s/DDWgOYhAyLOeOAtAsPkzOw/view?utm_content=DAG7j7qeW4s&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h7352de97e2" 
                           target="_blank" 
                           style="display: inline-block; background-color: var(--primary); color: white; padding: 15px 30px; text-decoration: none; border-radius: 50px; font-size: 18px; font-weight: bold; transition: all 0.3s; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                            <span style="margin-right: 8px;">👉</span> คลิกเพื่อเปิดดูคู่มือ
                        </a>
                        <p style="margin-top: 25px; color: var(--text); font-size: 16px; opacity: 0.8;">กดปุ่มด้านบนเพื่อเข้าสู่คู่มือการใช้งาน</p>
                    </div>
                    <div class="guide-popup-checkbox">
                        <input type="checkbox" id="hideGuideCheckbox">
                        <label for="hideGuideCheckbox">ไม่ต้องแสดงอีก</label>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(popup);

        // Close popup function
        window.closeGuidePopup = function () {
            const checkbox = document.getElementById('hideGuideCheckbox');
            if (checkbox && checkbox.checked) {
                localStorage.setItem('hideStudentGuide', 'true');
            }
            popup.remove();
            if (onClose) onClose();
        };

        // Close on overlay click
        popup.addEventListener('click', (e) => {
            if (e.target === popup) {
                closeGuidePopup();
            }
        });
    }
}

// Global function to show student guide (can be called from student pages)
function showStudentGuide() {
    showGuidePopup();
}

// Logout function
async function logout() {
    try {
        await fetch(`${API_BASE}/api/logout`, {
            method: 'POST'
        });

        localStorage.removeItem('user');
        localStorage.removeItem('role');
        window.location.href = '/';
    } catch (error) {
        console.error('Logout error:', error);
        window.location.href = '/';
    }
}

// Check authentication
function checkAuth(requiredRole) {
    const role = localStorage.getItem('role');
    if (!role || (requiredRole && role !== requiredRole)) {
        window.location.href = '/';
        return false;
    }
    return true;
}

// Get current user
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}
