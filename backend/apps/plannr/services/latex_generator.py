import os
import subprocess
import tempfile
from pathlib import Path

def generate_pdf(job, resume, keywords, resume_data=None):
    """
    Generate a tailored resume PDF using ModernCV LaTeX template.
    """
    latex_source = generate_modern_cv_latex(job, resume, keywords, resume_data)
    
    # DEBUG: Save generated LaTeX to inspect
    debug_path = os.path.join(os.path.dirname(__file__), 'debug_resume.tex')
    with open(debug_path, 'w', encoding='utf-8') as f:
        f.write(latex_source)
    print(f"[DEBUG] LaTeX source saved to: {debug_path}")
    
    return compile_latex_to_pdf(latex_source)

def generate_modern_cv_latex(job, resume, keywords, resume_data=None):
    """
    Generate professional ModernCV LaTeX resume using banking style.
    """
    
    # Safe string formatting helper
    def escape_latex(s):
        if not s: return ""
        s = str(s).strip().replace('\n', ' ').replace('\r', '')
        CHARS = {
            '\\': r'\textbackslash{}',
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
            '<': r'\textless{}',
            '>': r'\textgreater{}',
        }
        if '\\' in s:
            s = s.replace('\\', CHARS['\\'])
        for char, replacement in CHARS.items():
            if char != '\\':
                s = s.replace(char, replacement)
        return s

    # Default data if parsing failed
    data = resume_data or {}
    
    # Extract personal information
    name_parts = (data.get('name', '') or getattr(resume, 'candidate_name', '') or 'Professional').split()
    first_name = escape_latex(name_parts[0] if name_parts else 'Professional')
    last_name = escape_latex(' '.join(name_parts[1:]) if len(name_parts) > 1 else '')
    
    # Get job title for the title field
    job_title = escape_latex(getattr(job, 'title', '') or 'Full-Stack Developer')
    
    # Contact information
    phone = escape_latex(data.get('phone', ''))
    email = escape_latex(data.get('email', ''))
    location = escape_latex(data.get('location', ''))
    linkedin = escape_latex(data.get('linkedin', ''))
    github = escape_latex(data.get('github', ''))
    
    # Professional summary
    top_skills = ', '.join([escape_latex(str(k)) for k in keywords[:5]]) if keywords else "full-stack development"
    summary = f"Results-driven professional with expertise in {top_skills}, seeking to leverage technical skills in a {job_title} role."
    
    # Build header
    template = r"""\documentclass[11pt,a4paper,sans]{moderncv}
% ModernCV themes
\moderncvstyle{banking}
\moderncvcolor{blue}
% Character encoding
\usepackage[utf8]{inputenc}
% Adjust page margins
\usepackage[scale=0.85]{geometry}
\setlength{\hintscolumnwidth}{3cm}

% Personal information
"""
    
    template += f"\\name{{{first_name}}}{{{last_name}}}\n"
    template += f"\\title{{{job_title}}}\n"
    
    if phone:
        template += f"\\phone[mobile]{{{phone}}}\n"
    if email:
        template += f"\\email{{{email}}}\n"
    if linkedin:
        template += f"\\social[linkedin]{{{linkedin}}}\n"
    if github:
        template += f"\\social[github]{{{github}}}\n"
    if location:
        template += f"\\extrainfo{{{location}}}\n"
    
    template += "\n\\begin{document}\n\\makecvtitle\n\n"
    
    # Professional Profile/Summary
    template += "\\section{Professional Profile}\n"
    template += f"\\cvitem{{}}{{{summary}}}\n\n"
    
    # Core Competencies / Skills
    if keywords:
        template += "\\section{Core Competencies}\n"
        # Group skills by category if possible, otherwise list them
        for i in range(0, min(len(keywords), 15), 3):
            skills_group = keywords[i:i+3]
            skills_text = " \\textbullet{} ".join([escape_latex(str(skill)) for skill in skills_group])
            template += f"\\cvitem{{}}{{{skills_text}}}\n"
        template += "\n"
    
    # Professional Experience
    experiences = data.get('experience', [])
    if experiences:
        template += "\\section{Professional Experience}\n"
        for exp in experiences:
            period = escape_latex(exp.get('period', ''))
            title = escape_latex(exp.get('title', ''))
            company = escape_latex(exp.get('company', ''))
            location_exp = escape_latex(exp.get('location', ''))
            description = escape_latex(exp.get('description', ''))
            
            if title and company:
                template += f"\\cventry{{{period}}}{{{title}}}{{{company}}}{{{location_exp}}}{{}}{{\n"
                
                # Split description into bullet points if it contains multiple items
                if description:
                    bullets = [d.strip() for d in description.split('.') if d.strip()]
                    if len(bullets) > 1:
                        for bullet in bullets[:5]:  # Limit to 5 bullets
                            template += f"\\cvlistitem{{{bullet}}}\n"
                    else:
                        template += f"{description}\n"
                
                template += "}\n"
        template += "\n"
    
    # Education
    education = data.get('education', [])
    if education:
        template += "\\section{Education}\n"
        for edu in education:
            year = escape_latex(edu.get('year', ''))
            degree = escape_latex(edu.get('degree', ''))
            institution = escape_latex(edu.get('institution', ''))
            
            if degree and institution:
                template += f"\\cventry{{{year}}}{{{degree}}}{{{institution}}}{{}}{{}}{{}}\n"
        template += "\n"
    
    # Certifications if available
    certifications = data.get('certifications', [])
    if certifications:
        template += "\\section{Certifications}\n"
        for cert in certifications:
            cert_text = escape_latex(str(cert))
            template += f"\\cvlistitem{{{cert_text}}}\n"
        template += "\n"
    
    template += "\\end{document}\n"
    
    return template


def compile_latex_to_pdf(latex_source):
    """
    Compile LaTeX source to PDF using Tectonic.
    """
    try:
        # Create temporary directory for LaTeX compilation
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            
            # Write LaTeX source to file
            tex_file = tmpdir_path / "resume.tex"
            tex_file.write_text(latex_source, encoding='utf-8')
            
            print(f"[INFO] Compiling LaTeX with Tectonic...")
            
            # Run Tectonic directly (installed in container)
            result = subprocess.run(
                ['tectonic', str(tex_file)],
                cwd=str(tmpdir_path),
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                print(f"[ERROR] Tectonic stderr: {result.stderr}")
                print(f"[ERROR] Tectonic stdout: {result.stdout}")
                raise RuntimeError(f"LaTeX compilation failed: {result.stderr}")
            
            # Read generated PDF
            pdf_file = tmpdir_path / "resume.pdf"
            if not pdf_file.exists():
                raise RuntimeError("PDF was not generated by Tectonic")
            
            # Copy to a new temporary file that won't be deleted
            import shutil
            final_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            shutil.copy2(pdf_file, final_pdf.name)
            final_pdf.close()
            
            print(f"[INFO] PDF generated successfully: {final_pdf.name}")
            return final_pdf.name
            
    except subprocess.TimeoutExpired:
        raise RuntimeError("LaTeX compilation timed out after 120 seconds")
    except FileNotFoundError as e:
        print(f"[ERROR] Tectonic not found: {e}")
        print("[INFO] Make sure Tectonic is installed in the container")
        raise RuntimeError("Tectonic LaTeX compiler not found. Please rebuild the Docker image.")
    except Exception as e:
        print(f"[ERROR] PDF generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        raise RuntimeError(f"PDF generation failed: {str(e)}")
