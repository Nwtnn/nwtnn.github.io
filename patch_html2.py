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

    # 1. Update Title
    html = re.sub(
        r'<title>.*?</title>',
        '<title>Newton_Tiwari//Establish_connection</title>',
        html, count=1
    )

    # 2. Add Favicon (if not present)
    if 'favicon.svg' not in html:
        html = html.replace(
            '<link rel="stylesheet" href="index.css">',
            '<link rel="icon" type="image/svg+xml" href="/favicon.svg">\n    <link rel="stylesheet" href="index.css">'
        )

    # 3. Fix the huge gap by changing justify-center to pt-12 md:pt-32
    html = html.replace(
        'class="min-h-[80vh] flex flex-col justify-center',
        'class="min-h-[80vh] flex flex-col pt-12 md:pt-32'
    )

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ Updated: {fname}")
    else:
        print(f"~ Skipped (no changes): {fname}")

print("\nDone!")
