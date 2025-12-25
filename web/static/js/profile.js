// Teacher Profile Management
const API_BASE = '';

document.addEventListener('DOMContentLoaded', async () => {
    if (!checkAuth('teacher')) return;

    await loadProfile();
});

async function loadProfile() {
    const loading = document.getElementById('loading');

    try {
        loading.classList.remove('hidden');

        const response = await fetch(`${API_BASE}/api/profile`);
        const data = await response.json();

        console.log('Profile data:', data);

        // Fill form
        document.getElementById('username').value = data.username || '';
        document.getElementById('name').value = data.name || '';
        document.getElementById('subject').value = data.subject || '';
        document.getElementById('contact').value = data.contact || '';
        document.getElementById('room').value = data.room || '';

        // Load profile picture
        if (data.profile_picture) {
            // Check if it's a Supabase Storage URL (starts with https://)
            if (data.profile_picture.startsWith('http://') || data.profile_picture.startsWith('https://')) {
                document.getElementById('profilePicPreview').src = data.profile_picture;
            } else {
                // Local path (old data) - show default avatar
                document.getElementById('profilePicPreview').src = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(data.name || 'Teacher') + '&size=200&background=4285F4&color=fff';
            }
        } else {
            // No profile picture - show default avatar
            document.getElementById('profilePicPreview').src = 'https://ui-avatars.com/api/?name=' + encodeURIComponent(data.name || 'Teacher') + '&size=200&background=4285F4&color=fff';
        }

    } catch (error) {
        console.error('Error loading profile:', error);
        alert('เกิดข้อผิดพลาดในการโหลดข้อมูล');
    } finally {
        loading.classList.add('hidden');
    }
}

// Handle form submit
document.getElementById('profileForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('username', document.getElementById('username').value);
    formData.append('name', document.getElementById('name').value);
    formData.append('subject', document.getElementById('subject').value);
    formData.append('contact', document.getElementById('contact').value);
    formData.append('room', document.getElementById('room').value);

    // Add profile picture if selected
    const profilePic = document.getElementById('profilePicInput').files[0];
    if (profilePic) {
        formData.append('profile_picture', profilePic);
    }

    try {
        const response = await fetch(`${API_BASE}/api/profile`, {
            method: 'PUT',
            body: formData  // Send as FormData for file upload
        });

        const result = await response.json();

        if (result.success) {
            // Update localStorage
            const user = getCurrentUser();
            if (user) {
                user.name = formData.get('name');
                user.username = formData.get('username');
                localStorage.setItem('user', JSON.stringify(user));
            }

            alert('✅ บันทึกข้อมูลเรียบร้อย');

            // Reload profile to show updated picture
            await loadProfile();

            // Optional: redirect after a delay to see the updated picture
            // setTimeout(() => {
            //     window.location.href = '/teacher-dashboard.html';
            // }, 1000);
        } else {
            alert('Error: ' + (result.error || 'Failed to update'));
        }
    } catch (error) {
        console.error('Error saving profile:', error);
        alert('เกิดข้อผิดพลาดในการบันทึก');
    }
});
