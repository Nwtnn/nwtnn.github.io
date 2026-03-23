/**
 * NEWTON_TIWARI // SYSTEM_LOGIC v3.0
 */

document.addEventListener('DOMContentLoaded', () => {
    initSplash();
    initSidebar();
    initMobileDrawer();
    initShutdown();
    initScrollReveal();
    initActiveNav();
});

function initSplash() {
    const splash = document.getElementById('splash-screen');
    if (!splash) return;

    if (localStorage.getItem('splashShown')) {
        splash.style.display = 'none';
        return;
    }

    localStorage.setItem('splashShown', 'true');
    setTimeout(() => { splash.style.display = 'none'; }, 2000);
}

function initSidebar() {
    const sidebar   = document.querySelector('aside');
    const toggleBtn = document.getElementById('sidebar-toggle-btn');
    if (!sidebar) return;

    const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
    applySidebarState(isCollapsed, false);

    if (toggleBtn) {
        toggleBtn.addEventListener('click', () => {
            const nowCollapsed = !sidebar.classList.contains('sidebar-collapsed');
            applySidebarState(nowCollapsed, true);
        });
    }

    // Also let the header prompt toggle sidebar (original behaviour)
    const headerPrompt = document.querySelector('.sidebar-toggle');
    if (headerPrompt) {
        headerPrompt.style.cursor = 'pointer';
        headerPrompt.addEventListener('click', () => {
            const nowCollapsed = !sidebar.classList.contains('sidebar-collapsed');
            applySidebarState(nowCollapsed, true);
        });
    }
}

function applySidebarState(collapsed, persist) {
    const sidebar = document.querySelector('aside');
    const main    = document.querySelector('main');
    const header  = document.querySelector('header');
    const footer  = document.querySelector('footer');
    const btn     = document.getElementById('sidebar-toggle-btn');
    if (!sidebar) return;

    if (collapsed) {
        sidebar.classList.add('sidebar-collapsed');
        main   && main.classList.add('layout-expanded');
        header && header.classList.add('layout-expanded');
        footer && footer.classList.add('layout-expanded');
        if (btn) btn.innerHTML = '&#8250;';
    } else {
        sidebar.classList.remove('sidebar-collapsed');
        main   && main.classList.remove('layout-expanded');
        header && header.classList.remove('layout-expanded');
        footer && footer.classList.remove('layout-expanded');
        if (btn) btn.innerHTML = '&#8249;';
    }

    if (persist) localStorage.setItem('sidebar-collapsed', collapsed);
}

function initMobileDrawer() {
    const menuBtn = document.getElementById('mobile-menu-btn');
    const drawer  = document.getElementById('mobile-drawer');
    const overlay = document.getElementById('mobile-overlay');
    if (!menuBtn || !drawer || !overlay) return;

    const open  = () => { drawer.classList.add('active'); overlay.classList.add('active'); document.body.style.overflow = 'hidden'; };
    const close = () => { drawer.classList.remove('active'); overlay.classList.remove('active'); document.body.style.overflow = ''; };

    menuBtn.addEventListener('click', open);
    overlay.addEventListener('click', close);
    drawer.querySelectorAll('a').forEach(link => link.addEventListener('click', close));
}

function initScrollReveal() {
    const reveals  = document.querySelectorAll('section');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => { if (entry.isIntersecting) entry.target.classList.add('active'); });
    }, { threshold: 0.1 });
    reveals.forEach(el => { el.classList.add('reveal'); observer.observe(el); });
}

function initActiveNav() {
    let currentPath = window.location.pathname.split('/').pop();
    if (currentPath === '' || currentPath === 'index.html') currentPath = '/';
    else currentPath = '/' + currentPath.replace('.html', '');

    document.querySelectorAll('nav a, aside a, #mobile-drawer a').forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || href === currentPath + '.html') {
            link.classList.add('text-primary-neon', 'active-nav-link');
            link.classList.remove('text-on-surface-variant');
        }
    });
}

function initShutdown() {
    document.querySelectorAll('.shutdown-trigger').forEach(btn => {
        btn.addEventListener('click', e => { e.preventDefault(); performShutdown(); });
    });
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
        </div>`;
    document.body.appendChild(overlay);
    overlay.style.opacity = '0';
    overlay.style.transition = 'opacity 0.5s ease-in';
    setTimeout(() => overlay.style.opacity = '1', 10);
}
