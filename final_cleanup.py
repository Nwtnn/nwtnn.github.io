import os
import re

PORTFOLIO = r"C:\Users\newto\OneDrive\Desktop\portfolio"

files = [
    "index.html", "projects.html", "skills.html", "contact.html",
    "photos.html", "activity.html", "play.html", "books.html", "research.html"
]

# Standardized SIDEBAR Nav Content
SIDEBAR_NAV = """                <ul class="space-y-1">
                    <li>
                        <a href="/" class="flex items-center gap-4 px-6 py-3 text-on-surface-variant hover:text-primary-neon hover:bg-surface-raised stepped-transition group">
                            <span class="material-symbols-outlined text-xl">home</span>
                            <span class="text-[10px] font-bold tracking-[0.2em] uppercase sidebar-label">HOME</span>
                        </a>
                    </li>
                    <li>
                        <a href="/projects" class="flex items-center gap-4 px-6 py-3 text-on-surface-variant hover:text-primary-neon hover:bg-surface-raised stepped-transition group">
                            <span class="material-symbols-outlined text-xl">grid_view</span>
                            <span class="text-[10px] font-bold tracking-[0.2em] uppercase sidebar-label">PROJECTS</span>
                        </a>
                    </li>
                    <li>
                        <a href="/skills" class="flex items-center gap-4 px-6 py-3 text-on-surface-variant hover:text-primary-neon hover:bg-surface-raised stepped-transition group">
                            <span class="material-symbols-outlined text-xl">psychology</span>
                            <span class="text-[10px] font-bold tracking-[0.2em] uppercase sidebar-label">SKILLS</span>
                        </a>
                    </li>
                    <li>
                        <a href="/photos" class="flex items-center gap-4 px-6 py-3 text-on-surface-variant hover:text-primary-neon hover:bg-surface-raised stepped-transition group">
                            <span class="material-symbols-outlined text-xl">photo_library</span>
                            <span class="text-[10px] font-bold tracking-[0.2em] uppercase sidebar-label">PHOTOS</span>
                        </a>
                    </li>
                    <li>
                        <a href="/activity" class="flex items-center gap-4 px-6 py-3 text-on-surface-variant hover:text-tertiary-amber hover:bg-surface-raised stepped-transition group">
                            <span class="material-symbols-outlined text-xl">history</span>
                            <span class="text-[10px] font-bold tracking-[0.2em] uppercase sidebar-label">ACTIVITY LOG</span>
                        </a>
                        <ul class="ml-12 mt-1 space-y-2 opacity-60 sidebar-sub">
                            <li>
                                <a href="/play" class="flex items-center gap-3 text-[9px] font-bold tracking-widest hover:text-primary-neon stepped-transition">
                                    <span class="material-symbols-outlined text-xs">videogame_asset</span> GAME
                                </a>
                            </li>
                            <li>
                                <a href="/books" class="flex items-center gap-3 text-[9px] font-bold tracking-widest hover:text-primary-neon stepped-transition">
                                    <span class="material-symbols-outlined text-xs">library_books</span> BOOKS
                                </a>
                            </li>
                            <li>
                                <a href="/research" class="flex items-center gap-3 text-[9px] font-bold tracking-widest hover:text-primary-neon stepped-transition">
                                    <span class="material-symbols-outlined text-xs">description</span> RESEARCH_PAPERS
                                </a>
                            </li>
                        </ul>
                    </li>
                    <li>
                        <a href="/contact" class="flex items-center gap-4 px-6 py-3 text-on-surface-variant hover:text-primary-neon hover:bg-surface-raised stepped-transition group">
                            <span class="material-symbols-outlined text-xl">alternate_email</span>
                            <span class="text-[10px] font-bold tracking-[0.2em] uppercase sidebar-label">CONTACT</span>
                        </a>
                    </li>
                </ul>"""

# Standardized MOBILE DRAWER Nav Content
DRAWER_NAV = """                <a href="/"><span class="material-symbols-outlined">home</span> HOME</a>
                <a href="/projects"><span class="material-symbols-outlined">grid_view</span> PROJECTS</a>
                <a href="/skills"><span class="material-symbols-outlined">psychology</span> SKILLS</a>
                <a href="/photos"><span class="material-symbols-outlined">photo_library</span> PHOTOS</a>
                <a href="/activity"><span class="material-symbols-outlined">history</span> ACTIVITY LOG</a>
                <div class="drawer-sub">
                    <a href="/play"><span class="material-symbols-outlined">videogame_asset</span> GAME</a>
                    <a href="/books"><span class="material-symbols-outlined">library_books</span> BOOKS</a>
                    <a href="/research"><span class="material-symbols-outlined">description</span> RESEARCH</a>
                </div>
                <a href="/contact"><span class="material-symbols-outlined">alternate_email</span> CONTACT</a>"""

for fname in files:
    path = os.path.join(PORTFOLIO, fname)
    if not os.path.exists(path):
        continue

    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    original = html

    # 1. Update Sidebar Navigation (Be more greedy to catch everything up to the next closing tag)
    # We replace the entire <nav class="flex-1"> block
    sidebar_nav_pattern = r'<nav class="flex-1">.*?</nav>'
    replacement_sidebar = f'<nav class="flex-1">\n{SIDEBAR_NAV}\n            </nav>'
    html = re.sub(sidebar_nav_pattern, replacement_sidebar, html, flags=re.DOTALL)

    # 2. Update Mobile Drawer Navigation
    drawer_nav_pattern = r'<div id="mobile-drawer">.*?<nav>.*?</nav>'
    # We need to preserve the drawer-header
    drawer_header_match = re.search(r'(<div class="drawer-header">.*?</div>)', html, flags=re.DOTALL)
    if drawer_header_match:
        header_html = drawer_header_match.group(1)
        replacement_drawer_full = f'<div id="mobile-drawer">\n            {header_html}\n            <nav>\n{DRAWER_NAV}\n            </nav>'
        html = re.sub(r'<div id="mobile-drawer">.*?<nav>.*?</nav>', replacement_drawer_full, html, flags=re.DOTALL)

    # 3. Remove conflicting Tailwind margin classes and fix vertical gap
    # Remove ml-0 md:ml-64 from main
    html = html.replace('class="ml-0 md:ml-64 pt-16', 'class="pt-4')
    html = html.replace('class="ml-0 md:ml-64 pt-12', 'class="pt-4')
    # Remove ml-0 md:ml-64 from footer
    html = html.replace('class="ml-0 md:ml-64 py-4', 'class="py-4')

    # 4. Add system-status class for mobile hiding (if not already there)
    if 'system-status' not in html:
        html = html.replace('flex items-center gap-4 text-xs">', 'flex items-center gap-4 text-xs system-status">')

    # 5. Fix double spacing issue in some files
    html = html.replace('class="pt-8 pb-24', 'class="pt-0 pb-24')

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ Updated: {fname}")
    else:
        print(f"~ Skipped (no changes): {fname}")

print("\nDone!")
