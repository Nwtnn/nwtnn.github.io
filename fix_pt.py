import os, glob

for f in glob.glob("*.html"):
    with open(f, "r", encoding="utf-8") as file:
        content = file.read()
    if 'class="pt-0 ' in content or 'class="pt-0"' in content:
        content = content.replace('class="pt-0 ', 'class="pt-8 ').replace('class="pt-0"', 'class="pt-8"')
        with open(f, "w", encoding="utf-8") as file:
            file.write(content)
        print("Fixed padding in", f)
