// SPA Router for TeachMap PWA
const API_BASE = '';

// Page Management
const pages = {
    'teacher': '/teacher',
    'grid': '/schedule-grid.html',
    'admin': '/admin.html',
    'student': '/student'
};

// Load page content dynamically
async function loadPage(pageName, addToHistory = true) {
    const pageUrl = pages[pageName];
    if (!pageUrl) return;

    try {
        // Show loading
        const mainContent = document.querySelector('.main-content');
        if (mainContent) {
            mainContent.innerHTML = '<div class="loading"><div class="spinner"></div><p>กำลังโหลด...</p></div>';
        }

        // Fetch page content
        const response = await fetch(pageUrl);
        const html = await response.text();

        // Parse HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const newContent = doc.querySelector('.main-content');

        if (newContent && mainContent) {
            mainContent.innerHTML = newContent.innerHTML;

            // Execute page-specific scripts
            loadPageScripts(pageName);

            // Update navigation active state
            updateNavigation(pageName);

            // Update history
            if (addToHistory) {
                history.pushState({ page: pageName }, '', pageUrl);
            }
        }

    } catch (error) {
        console.error('Error loading page:', error);
        alert('เกิดข้อผิดพลาดในการโหลดหน้า');
    }
}

// Load page-specific JavaScript
function loadPageScripts(pageName) {
    // Remove old scripts
    document.querySelectorAll('script[data-page-script]').forEach(s => s.remove());

    const scriptMap = {
        'teacher': '/js/teacher.js',
        'grid': '/js/schedule-grid.js',
        'admin': '/js/admin.js',
        'student': '/js/student.js'
    };

    const scriptUrl = scriptMap[pageName];
    if (scriptUrl) {
        const script = document.createElement('script');
        script.src = scriptUrl;
        script.setAttribute('data-page-script', 'true');
        document.body.appendChild(script);
    }
}

// Update navigation active state
function updateNavigation(pageName) {
    document.querySelectorAll('.header-buttons .btn-secondary').forEach(btn => {
        btn.classList.remove('active');
    });

    const activeMap = {
        'teacher': 0,
        'grid': 1,
        'admin': 2,
        'student': 0
    };

    const buttons = document.querySelectorAll('.header-buttons .btn-secondary');
    const index = activeMap[pageName];
    if (buttons[index]) {
        buttons[index].classList.add('active');
    }
}

// Handle browser back/forward
window.addEventListener('popstate', (event) => {
    if (event.state && event.state.page) {
        loadPage(event.state.page, false);
    }
});

// Intercept navigation clicks
document.addEventListener('DOMContentLoaded', () => {
    // This will be initialized after DOM loads
});

// Export for use in other files
if (typeof window !== 'undefined') {
    window.navigateTo = (pageName) => {
        loadPage(pageName);
    };
}
