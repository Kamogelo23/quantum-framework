"""Fix all \\n to \n in latex_generator.py"""

with open(r'c:\Users\KamogeloMahoma\New folder (2)\quantum-framework\backend\apps\plannr\services\latex_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all instances of literal \\n with actual newline in the string concatenations
# Line 68: exp_section
content = content.replace('exp_section += "}\\\\n"', 'exp_section += "}\\n"')
# Line 78: edu_section  
content = content.replace('edu_section += f"\\\\cventry{{{year}}}{{{degree}}}{{{inst}}}{{}}{{}}{{}}\\\\n"', 'edu_section += f"\\\\cventry{{{year}}}{{{degree}}}{{{inst}}}{{}}{{}}{{}}\\n"')
# Line 86: skills_items
content = content.replace('skills_items += "\\\\cvitem{}{" + " \\\\\\\\textbullet\\\\\\\\ ".join(group) + "}\\\\n"', 'skills_items += "\\\\cv item{}{" + " \\\\\\\\textbullet\\\\\\\\ ".join(group) + "}\\n"')

with open(r'c:\Users\KamogeloMahoma\New folder (2)\quantum-framework\backend\apps\plannr\services\latex_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed all \\\\n to \\n")
