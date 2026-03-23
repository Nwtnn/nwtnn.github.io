import os
import re

PORTFOLIO = r"C:\Users\newto\OneDrive\Desktop\portfolio"

SPLASH = '''    <!-- SPLASH SCREEN -->
    <div id="splash-screen">
        <div class="splash-logo">N</div>
        <div class="splash-name">Newton Tiwari</div>
    </div>

'''

MOBILE_ELEMENTS = '''
        <!-- MOBILE OVERLAY -->
        <div id="mobile-overlay"></div>

        <!-- MOBILE DRAWER -->
        <div id="mobile-drawer">
            <div class="drawer-header">
                <div class="drawer-name">NEWTON_TIWARI</div>
                <div class="drawer-ver">VER_2.1.0</div>
            </div>
            <nav>
                <a href="/"><span class="material-symbols-outlined">home</span> HOME</a>
                <a href="/projects"><span class="material-symbols-outlined">grid_view</span> PROJECTS</a>
                <a href="/skills"><span class="material-symbols-outlined">psychology</span> SKILLS</a>
                <a href="/contact"><span class="material-symbols-outlined">alternate_email</span> CONTACT</a>
                <a href="/photos"><span class="material-symbols-outlined">photo_library</span> PHOTOS</a>
                <a href="/activity"><span class="material-symbols-outlined">history</span> ACTIVITY LOG</a>
                <div class="drawer-sub">
                    <a href="/play"><span class="material-symbols-outlined">videogame_asset</span> GAME</a>
                    <a href="/books"><span class="material-symbols-outlined">library_books</span> BOOKS</a>
                    <a href="/research"><span class="material-symbols-outlined">description</span> RESEARCH</a>
                </div>
            </nav>
            <div class="drawer-footer">
                <a href="#" class="shutdown-trigger">
                    <span class="material-symbols-outlined">power_settings_new</span> SYS_OFF
                </a>
            </div>
        </div>

'''

files = [
    "index.html", "projects.html", "skills.html", "contact.html",
    "photos.html", "activity.html", "play.html", "books.html", "research.html"
]

for fname in files:
    path = os.path.join(PORTFOLIO, fname)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    original = html

    # 1. Add splash screen right after <body ...>\r\n (or \n)
    if 'id="splash-screen"' not in html:
        html = re.sub(
            r'(<body[^>]*>)(\r?\n)',
            lambda m: m.group(1) + m.group(2) + SPLASH,
            html, count=1
        )

    # 2. Add hamburger button in header
    if 'id="mobile-menu-btn"' not in html:
        html = re.sub(
            r'(<span class="text-primary-neon font-bold tracking-widest sidebar-toggle[^"]*"[^>]*>\[newton@portfolio ~\]\$</span>)',
            r'\1\n                <button id="mobile-menu-btn" aria-label="Open navigation">&#9776;</button>',
            html, count=1
        )

    # 3. Fix aside classes
    if 'hidden md:flex flex-col' not in html:
        html = html.replace(
            'class="fixed left-0 top-0 h-full w-20 md:w-64 bg-surface-inset border-r border-white/5 pt-20 flex flex-col z-40 transition-all duration-300"',
            'class="fixed left-0 top-0 h-full w-64 bg-surface-inset border-r border-white/5 pt-20 hidden md:flex flex-col z-40 transition-all duration-300 overflow-hidden relative"'
        )
        html = html.replace(
            'class="fixed left-0 top-0 h-full w-20 md:w-64 bg-surface-inset border-r border-white/5 pt-20 hidden md:flex flex-col z-40 transition-all duration-300"',
            'class="fixed left-0 top-0 h-full w-64 bg-surface-inset border-r border-white/5 pt-20 hidden md:flex flex-col z-40 transition-all duration-300 overflow-hidden relative"'
        )

    # 4. Fix sidebar brand div
    if 'id="sidebar-toggle-btn"' not in html:
        html = html.replace(
            '<div class="px-6 mb-8 hidden md:block">',
            '<div class="px-6 mb-8 sidebar-brand">\n                <button id="sidebar-toggle-btn" title="Toggle Sidebar">&#8249;</button>'
        )
        html = html.replace(
            '<div class="px-6 mb-8">',
            '<div class="px-6 mb-8 sidebar-brand">\n                <button id="sidebar-toggle-btn" title="Toggle Sidebar">&#8249;</button>'
        )

    # 5. Add sidebar-label class
    html = html.replace(
        '<span class="text-[10px] font-bold tracking-[0.2em] uppercase hidden md:block">',
        '<span class="text-[10px] font-bold tracking-[0.2em] uppercase sidebar-label">'
    )

    # 6. Add sidebar-sub class
    html = html.replace(
        '<ul class="ml-12 mt-1 space-y-2 hidden md:block opacity-60">',
        '<ul class="ml-12 mt-1 space-y-2 opacity-60 sidebar-sub">'
    )

    # 7. Fix main margin
    html = html.replace(
        'class="ml-16 md:ml-20 pt-16 flex-1',
        'class="ml-0 md:ml-64 pt-16 flex-1'
    )
    html = html.replace(
        'class="ml-16 md:ml-64 pt-16 flex-1',
        'class="ml-0 md:ml-64 pt-16 flex-1'
    )

    # 8. Fix footer margin
    html = html.replace(
        'class="ml-16 md:ml-64 py-4',
        'class="ml-0 md:ml-64 py-4'
    )

    # 9. Inject mobile overlay+drawer INSIDE crt-flicker div
    if 'id="mobile-overlay"' not in html:
        html = html.replace('        <!-- MAIN CONTENT AREA -->', MOBILE_ELEMENTS + '        <!-- MAIN CONTENT AREA -->', 1)

    # 10. Remove duplicate inline active-nav script SAFELY
    old_js = """            // Active Link Highlight
            let currentPath = window.location.pathname.split('/').pop();
            if (currentPath === '' || currentPath === 'index.html') currentPath = '/';
            else currentPath = '/' + currentPath.replace('.html', '');
            
            const navLinks = document.querySelectorAll('nav a, aside a');
            navLinks.forEach(link => {
                const href = link.getAttribute('href');
                if (href === currentPath || href === currentPath + '.html') {
                    link.classList.add('text-primary-neon');
                    link.classList.add('active-nav-link');
                    link.classList.remove('text-on-surface-variant');
                }
            });"""
    html = html.replace(old_js, "")
    html = html.replace("\r\n\r\n        });\r\n    </script>", "\r\n        });\r\n    </script>")
    html = html.replace("\n\n        });\n    </script>", "\n        });\n    </script>")

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ Updated: {fname}")
    else:
        print(f"~ Skipped (no changes): {fname}")

print("\nDone!")
