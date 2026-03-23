import os
import re

PORTFOLIO = r"C:\Users\newto\OneDrive\Desktop\portfolio"

files = [
    "index.html", "projects.html", "skills.html", "contact.html",
    "photos.html", "activity.html", "play.html", "books.html", "research.html"
]

INLINE_SCRIPT = """
    <script>
        if (sessionStorage.getItem('splashShown')) {
            document.documentElement.classList.add('splash-hidden');
        }
    </script>
    <style>
        html.splash-hidden #splash-screen { display: none !important; animation: none !important; opacity: 0 !important; visibility: hidden !important; }
    </style>
"""

for fname in files:
    path = os.path.join(PORTFOLIO, fname)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    original = html

    # 1. Update Title to 'Newton Tiwari'
    html = re.sub(
        r'<title>.*?</title>',
        '<title>Newton Tiwari</title>',
        html, count=1
    )

    # 2. Add inline splash-hiding script to prevent flash
    if 'html.splash-hidden #splash-screen' not in html:
        # insert right before </head>
        html = html.replace('</head>', INLINE_SCRIPT + '</head>')

    # 3. Remove md:pt-32 to fix huge gap on desktop
    html = html.replace(
        'class="min-h-[80vh] flex flex-col pt-12 md:pt-32',
        'class="min-h-[80vh] flex flex-col pt-4 md:pt-8'
    )

    # Also check if other pages like projects.html still have justify-center
    html = html.replace(
        'class="min-h-[80vh] flex flex-col justify-center',
        'class="min-h-[80vh] flex flex-col pt-4 md:pt-8'
    )

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ Updated: {fname}")
    else:
        print(f"~ Skipped (no changes): {fname}")

print("\nDone!")
