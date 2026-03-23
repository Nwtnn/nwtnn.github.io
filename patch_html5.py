import os
import re

PORTFOLIO = r"C:\Users\newto\OneDrive\Desktop\portfolio"

files = [
    "index.html", "projects.html", "skills.html", "contact.html",
    "photos.html", "activity.html", "play.html", "books.html", "research.html"
]

NEW_SCRIPT = """
    <script>
        if (localStorage.getItem('splashShown') || sessionStorage.getItem('splashShown') || window.name === 'splashShown' || document.cookie.includes('splashShown=true')) {
            document.documentElement.classList.add('splash-hidden');
        }
    </script>
"""

for fname in files:
    path = os.path.join(PORTFOLIO, fname)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    original = html

    # 1. Update Inline SPLASH Script to use bulletproof checks
    html = re.sub(
        r'<script>\s*if \(localStorage\.getItem\(\'splashShown\'\)\) \{\s*document\.documentElement\.classList\.add\(\'splash-hidden\'\);\s*\}\s*</script>',
        NEW_SCRIPT.strip(),
        html
    )

    # 2. Remove Desktop Navigation Links from Header
    html = re.sub(
        r'<nav class="hidden md:flex gap-8">.*?</nav>',
        '',
        html,
        flags=re.DOTALL
    )

    # 3. Center the title by making position absolute
    html = html.replace(
        '<span class="text-primary-neon font-bold tracking-widest sidebar-toggle hover:glow-primary transition-all">[newton@portfolio ~]$</span>',
        '<span class="text-primary-neon font-bold tracking-widest sidebar-toggle hover:glow-primary transition-all absolute left-1/2 -translate-x-1/2 top-1/2 -translate-y-1/2 whitespace-nowrap">[newton@portfolio ~]$</span>'
    )

    # 4. Zero out the gap. Change pt-8 md:pt-12 to pt-0
    html = html.replace(
        'class="pt-8 md:pt-12',
        'class="pt-0'
    )
    
    # Check if there are any remaining justify-center
    html = html.replace(
        'class="min-h-[80vh] flex flex-col justify-center',
        'class="pt-0'
    )

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ Updated: {fname}")
    else:
        print(f"~ Skipped (no changes): {fname}")

print("\nDone!")
