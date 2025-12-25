"""Fix the syntax error in latex_generator.py"""

# Read the entire file
with open(r'c:\Users\KamogeloMahoma\New folder (2)\quantum-framework\backend\apps\plannr\services\latex_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# The problematic section needs to be a proper raw string
# Replace the broken template continuation
old_pattern = '''    template += r"""

\\begin{document}
\\makecvtitle

\\section{Professional Summary}
""" + summary + r"""

\\section{Core Competencies}
""" + skills_section + r"""
"""'''

new_pattern = '''    template += r"""

\\begin{document}
\\makecvtitle

\\section{Professional Summary}
"""
    template += summary + r"""

\\section{Core Competencies}
"""
    template += skills_section + r"""
"""'''

content = content.replace(old_pattern, new_pattern)

# Write back
with open(r'c:\Users\KamogeloMahoma\New folder (2)\quantum-framework\backend\apps\plannr\services\latex_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed syntax error!")
