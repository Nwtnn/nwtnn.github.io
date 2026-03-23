/**
 * NEWTON_TIWARI // SYSTEM_LOGIC v3.0
 * Splash screen, sidebar collapse, mobile drawer, shutdown sequence.
 */

document.addEventListener('DOMContentLoaded', () => {
    initSplash();
    initSidebar();
    initMobileDrawer();
    initShutdown();
    initActiveNav();
});

/* =====================================================
   SPLASH SCREEN
   ===================================================== */
function initSplash() {
    const splash = document.getElementById('splash-screen');
    if (!splash) return;

    // Remove from DOM after animation completes (2s)
    setTimeout(() => {
        splash.style.display = 'none';
    }, 2000);
}

/* =====================================================
   SIDEBAR COLLAPSE (DESKTOP)
   ===================================================== */
function initSidebar() {
    const sidebar   = document.getElementById('main-sidebar');
    const toggleBtn = document.getElementById('sidebar-toggle-btn');
    if (!sidebar) return;

    // Restore persisted state
    const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
    applySidebarState(isCollapsed, false);

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            const nowCollapsed = !sidebar.classList.contains('sidebar-collapsed');
            applySidebarState(nowCollapsed, true);
        });
    }

    // Also keep the old header-prompt click working
    const headerPrompt = document.querySelector('.sidebar-toggle');
    if (headerPrompt) {
        headerPrompt.addEventListener('click', () => {
            const nowCollapsed = !sidebar.classList.contains('sidebar-collapsed');
            applySidebarState(nowCollapsed, true);
        });
    }
}

function applySidebarState(collapsed, persist) {
    const sidebar = document.getElementById('main-sidebar');
    const main    = document.getElementById('main-content');
    const header  = document.getElementById('main-header');
    const footer  = document.getElementById('main-footer');
    const btn     = document.getElementById('sidebar-toggle-btn');

    if (!sidebar) return;

    if (collapsed) {
        sidebar.classList.add('sidebar-collapsed');
        main   && main.classList.add('layout-expanded');
        header && header.classList.add('layout-expanded');
        footer && footer.classList.add('layout-expanded');
        if (btn) btn.textContent = '›';
    } else {
        sidebar.classList.remove('sidebar-collapsed');
        main   && main.classList.remove('layout-expanded');
        header && header.classList.remove('layout-expanded');
        footer && footer.classList.remove('layout-expanded');
        if (btn) btn.textContent = '‹';
    }

    if (persist) {
        localStorage.setItem('sidebar-collapsed', collapsed);
    }
}

/* =====================================================
   MOBILE DRAWER
   ===================================================== */
function initMobileDrawer() {
    const menuBtn  = document.getElementById('mobile-menu-btn');
    const drawer   = document.getElementById('mobile-drawer');
    const overlay  = document.getElementById('mobile-overlay');
    if (!menuBtn || !drawer || !overlay) return;

    function openDrawer() {
        drawer.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
        drawer.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    menuBtn.addEventListener('click', openDrawer);
    overlay.addEventListener('click', closeDrawer);

    // Close on nav link click
    drawer.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', closeDrawer);
    });
}

/* =====================================================
   ACTIVE NAV HIGHLIGHT
   ===================================================== */
function initActiveNav() {
    let currentPath = window.location.pathname.split('/').pop();
    if (currentPath === '' || currentPath === 'index.html') currentPath = '/';
    else currentPath = '/' + currentPath.replace('.html', '');

    const allLinks = document.querySelectorAll('nav a, aside a, #mobile-drawer a');
    allLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || href === currentPath + '.html') {
            link.classList.add('active-nav-link');
        }
    });
}

/* =====================================================
   SHUTDOWN SEQUENCE
   ===================================================== */
function initShutdown() {
    const shutdownBtn = document.querySelector('.shutdown-trigger');
    if (shutdownBtn) {
        shutdownBtn.addEventListener('click', (e) => {
            e.preventDefault();
            performShutdown();
        });
    }
}

function performShutdown() {
    const overlay = document.createElement('div');
    overlay.id = 'shutdown-overlay';
    overlay.className = 'fixed inset-0 z-[1000] bg-black flex flex-col items-center justify-center font-mono text-primary-neon p-12';

    overlay.innerHTML = `
        <div class="max-w-md w-full">
            <p class="mb-4 text-xs opacity-50">[  OK  ] Stopping System Logging Service...</p>
            <p class="mb-4 text-xs opacity-50">[  OK  ] Unmounting Virtual Identity Buffers...</p>
            <p class="mb-4 text-xs opacity-50">[  OK  ] Disconnecting from Uplink Node...</p>
            <p class="mt-8 text-xl font-bold glow-primary text-center">SYSTEM_OFFLINE</p>
            <p class="mt-4 text-[10px] opacity-30 text-center uppercase tracking-[0.3em]">Connection Severed // Return to reality</p>
            <div class="mt-12 flex justify-center">
                <button onclick="location.reload()" class="border border-primary-neon/30 px-4 py-2 text-[10px] hover:bg-primary-neon hover:text-black transition-colors">REBOOT_SYSTEM</button>
            </div>
        </div>
    `;

    document.body.appendChild(overlay);
    overlay.style.opacity = '0';
    overlay.style.transition = 'opacity 0.5s ease-in';
    setTimeout(() => overlay.style.opacity = '1', 10);
}
