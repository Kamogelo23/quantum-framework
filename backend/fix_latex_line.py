import re

# Read the file
with open(r'apps\plannr\services\latex_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the problematic line
# The issue is in line 86: the separator has \\\\ before and after \textbullet
# It should be just \textbullet{} as a separator between skills

# Match the pattern and replace
old_pattern = r'skills_items \+= "\\\\\\cvitem\{\}\{" \+ " \\\\\\textbullet\{\}\\\\ "\.join\(group\) \+ "\}\\n"'
new_line = r'skills_items += "\\cvitem{}{" + " \\textbullet{} ".join(group) + "}\\n"'

content = re.sub(old_pattern, new_line, content)

# Write back
with open(r'apps\plannr\services\latex_generator.py', 'w', encoding='utf-8', newline='') as f:
    f.write(content)

print("Fixed!")
