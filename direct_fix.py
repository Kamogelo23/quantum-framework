import os

file_path = r'c:\Users\KamogeloMahoma\New folder (2)\quantum-framework\backend\apps\plannr\services\latex_generator.py'

# Read all lines
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 81 (index 80) needs to be fixed
# Current (bad): edu_section += f"\\cventry{{{year}}}{{{degree}}}{{{inst}}}{{}}{{}}{{}}\\\\n"  
# Target (good): edu_section += f"\\cventry{{{year}}}{{{degree}}}{{{inst}}}{{}}{{}}{{}}\\n"

# The correct line with proper escaping
correct_line = '            edu_section += f"\\\\cventry{{{year}}}{{{degree}}}{{{inst}}}{{}}{{}}{{}}\\n"\n'

# Replace line 81
print("Before:", repr(lines[80]))
lines[80] = correct_line  
print("After: ", repr(lines[80]))

# Write back
with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("\nFixed! Changed \\\\\\\\n to \\\\n")
