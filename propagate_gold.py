import os
import re

PORTFOLIO = r"C:\Users\newto\OneDrive\Desktop\portfolio"

# Source of truth: index.html
with open(os.path.join(PORTFOLIO, "index.html"), "r", encoding="utf-8") as f:
    index_html = f.read()

def extract_block(html, start_marker, end_marker):
    start_index = html.find(start_marker)
    end_index = html.find(end_marker, start_index)
    if start_index != -1 and end_index != -1:
        return html[start_index:end_index + len(end_marker)]
    return None

# Extract gold standard blocks
HEADER_BLOCK = extract_block(index_html, '<header id="main-header"', '</header>')
DRAWER_BLOCK = extract_block(index_html, '<!-- MOBILE DRAWER -->', '<!-- END MOBILE DRAWER -->')
FOOTER_BLOCK = extract_block(index_html, '<footer id="main-footer"', '</footer>')

files = [
    "index.html", "projects.html", "skills.html", "contact.html",
    "photos.html", "activity.html", "play.html", "books.html", "research.html"
]

for fname in files:
    if fname == "index.html": continue
    path = os.path.join(PORTFOLIO, fname)
    if not os.path.exists(path): continue

    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Update Header
    html = re.sub(r'<header.*?</header>', HEADER_BLOCK, html, flags=re.DOTALL)
    
    # 2. Ensure Sidebar is GONE
    html = re.sub(r'<aside.*?</aside>', '', html, flags=re.DOTALL)
    
    # 3. Update Mobile Overlay & Drawer (Surgical replacement between markers)
    # If the file has no markers, we'll try to find the old drawer pattern
    
    # Replace anything between <!-- MOBILE OVERLAY --> and <!-- MAIN CONTENT AREA -->
    # with the new Overlay and Drawer blocks
    pattern = r'<!-- MOBILE OVERLAY -->.*?<!-- MAIN CONTENT AREA -->'
    replacement = '<!-- MOBILE OVERLAY -->\n        <div id="mobile-overlay"></div>\n\n        ' + DRAWER_BLOCK + '\n\n        <!-- MAIN CONTENT AREA -->'
    
    if '<!-- MOBILE OVERLAY -->' in html and '<!-- MAIN CONTENT AREA -->' in html:
        html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    else:
        # Fallback: if markers are missing, just ensure the drawer block is inserted before main
        html = html.replace('<main id="main-content"', DRAWER_BLOCK + '\n\n        <main id="main-content"')

    # 4. Standardize Main tag
    html = re.sub(r'<main id="main-content".*?>', '<main id="main-content" class="relative">', html, flags=re.DOTALL)
    
    # 5. Update Footer
    if FOOTER_BLOCK:
        html = re.sub(r'<footer id="main-footer".*?</footer>', FOOTER_BLOCK, html, flags=re.DOTALL)

    # 6. Final Cleanup (Brace/Wrapper)
    html = html.replace('class="crt-flicker min-h-screen flex flex-col"', 'class="crt-flicker min-h-screen"')

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✓ Fixed and Synchronized: {fname}")

print("\nAll pages fully restored and synchronized!")
