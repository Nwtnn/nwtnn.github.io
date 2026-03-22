/**
 * NEWTON_TIWARI // SYTEM_LOGIC
 * Handles sidebar collapse, persistent state, and system shutdown sequence.
 */

document.addEventListener('DOMContentLoaded', () => {
    initSidebar();
    initShutdown();
    updateFooter();
});

function initSidebar() {
    const sidebar = document.querySelector('aside');
    const main = document.querySelector('main');
    const header = document.querySelector('header');
    const footer = document.querySelector('footer');
    const toggleTrigger = document.querySelector('.sidebar-toggle');

    if (!sidebar || !main || !header || !footer) return;

    // Load persisted state
    const isCollapsed = localStorage.getItem('sidebar-collapsed') === 'true';
    if (isCollapsed) {
        applySidebarState(true);
    }

    // Add toggle event to the header prompt
    if (toggleTrigger) {
        toggleTrigger.style.cursor = 'pointer';
        toggleTrigger.addEventListener('click', () => {
            const nowCollapsed = !sidebar.classList.contains('sidebar-collapsed');
            applySidebarState(nowCollapsed);
            localStorage.setItem('sidebar-collapsed', nowCollapsed);
        });
    }
}

function applySidebarState(collapsed) {
    const sidebar = document.querySelector('aside');
    const main = document.querySelector('main');
    const header = document.querySelector('header');
    const footer = document.querySelector('footer');

    if (collapsed) {
        sidebar.classList.add('sidebar-collapsed');
        main.classList.add('layout-expanded');
        header.classList.add('layout-expanded');
        footer.classList.add('layout-expanded');
    } else {
        sidebar.classList.remove('sidebar-collapsed');
        main.classList.remove('layout-expanded');
        header.classList.remove('layout-expanded');
        footer.classList.remove('layout-expanded');
    }
}

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
    // Create shutdown overlay
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
    
    // Fade in effect
    overlay.style.opacity = '0';
    overlay.style.transition = 'opacity 0.5s ease-in';
    setTimeout(() => overlay.style.opacity = '1', 10);
}

function updateFooter() {
    const footers = document.querySelectorAll('footer div');
    footers.forEach(div => {

    });
}
