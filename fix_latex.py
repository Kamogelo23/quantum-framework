"""Quick fix for latex_generator.py line 81"""
import re

file_path = r"c:\Users\KamogeloMahoma\New folder (2)\quantum-framework\backend\apps\plannr\services\latex_generator.py"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the problematic line
# Change: edu_section += f"\\cventry{{{year}}}{{{degree}}}{{{inst}}}{{}}{{}}{{}}\\\\n"
# To:     edu_section += f"\\cventry{{{year}}}{{{degree}}}{{{inst}}}{{}}{{}}{{}}\\n"

content = content.replace(
    'edu_section += f"\\\\cventry{{{year}}}{{{degree}}}{{{inst}}}{{}}{{}}{{}}\\\\\\\\n"',
    'edu_section += f"\\\\cventry{{{year}}}{{{degree}}}{{{inst}}}{{}}{{}}{{}}\\\\n"'
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed! Changed double-backslash-n to single-backslash-n in education section")
