import os
import re

PORTFOLIO = r"C:\Users\newto\OneDrive\Desktop\portfolio"

files = [
    "index.html", "projects.html", "skills.html", "contact.html",
    "photos.html", "activity.html", "play.html", "books.html", "research.html"
]

CONTACT_BLOCK_REGEX = r'(<li>\s*<a href="/contact".*?</li>\s*)'

for fname in files:
    path = os.path.join(PORTFOLIO, fname)
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    original = html

    # 1. Purge py-24 gap from main sections
    # It might be `class="py-24 ..."` or similar
    html = html.replace('class="py-24', 'class="pt-8 pb-24')

    # 2. Convert header absolute text to fixed text so it ignores sidebar margin shifts
    html = html.replace(
        'absolute left-1/2 -translate-x-1/2 top-1/2 -translate-y-1/2',
        'fixed left-1/2 -translate-x-1/2 top-[1.125rem]'
    )

    # 3. Sidebar Reordering
    # Extract Contact block
    match = re.search(CONTACT_BLOCK_REGEX, html, flags=re.DOTALL)
    if match:
        contact_html = match.group(1)
        # Remove it from its current position
        html = html.replace(contact_html, '')
        # Wait, there are TWO contact blocks now! One in sidebar, one in mobile drawer.
        # Let's only do it for the sidebar (the one inside <li>)
        # We find the end of the sidebar list: "</ul>\s*</nav>\s*<div class=\"px-6 py-8 border-t border-white/5\">"
        sidebar_end_target = "                        </ul>\n                    </li>\n                </ul>\n            </nav>"
        if sidebar_end_target in html:
            html = html.replace(
                sidebar_end_target,
                "                        </ul>\n                    </li>\n" + contact_html + "                </ul>\n            </nav>"
            )

    if html != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✓ Updated: {fname}")
    else:
        print(f"~ Skipped (no changes): {fname}")

print("\nDone!")
