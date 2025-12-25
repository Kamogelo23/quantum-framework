import os
import re

# Read the file
file_path = r'c:\Users\KamogeloMahoma\New folder (2)\quantum-framework\backend\apps\plannr\services\latex_generator.py'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix line 81 (0-indexed as 80)
for i, line in enumerate(lines):
    if 'edu_section += f"' in line and '\\\\n"' in line:
        # Replace \\\\n with \\n (double backslash to single)
        old_line = line
        new_line = line.replace('\\\\\\\\n"', '\\\\n"')
        if old_line != new_line:
            lines[i] = new_line
            print(f"Line {i+1}: Fixed double-escaped newline")
            print(f"Before: {old_line.strip()}")
            print(f"After:  {new_line.strip()}")

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nFile updated successfully!")
