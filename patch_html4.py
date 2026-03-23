import os
import re

PORTFOLIO = r"C:\Users\newto\OneDrive\Desktop\portfolio"

files = [
    "index.html", "projects.html", "skills.html", "contact.html",
    "photos.html", "activity.html", "play.html", "books.html", "research.html"
]

for fname in files:
    path = os.path.join(PORTFOLIO, fname)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    original = html

    # 1. Remove Splash logo 'N'
    html = html.replace('<div class="splash-logo">N</div>\n', '')
    html = html.replace('<div class="splash-logo">N</div>\r\n', '')
    html = html.replace('        <div class="splash-logo">N</div>\n', '')

    # 2. Update inline script to use localStorage
    html = html.replace("sessionStorage.getItem('splashShown')", "localStorage.getItem('splashShown')")

    # 3. Strip out flex and min-h-[80vh] constraints completely
    # Change min-h-[80vh] flex flex-col pt-4 md:pt-8 to simply pt-8 md:pt-12
    html = html.replace(
        'class="min-h-[80vh] flex flex-col pt-4 md:pt-8',
        'class="pt-8 md:pt-12'
    )
    
    # Just in case some have justify-center
    html = html.replace(
        'class="min-h-[80vh] flex flex-col justify-center',
        'class="pt-8 md:pt-12'
    )

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ Updated: {fname}")
    else:
        print(f"~ Skipped (no changes): {fname}")

print("\nDone!")
