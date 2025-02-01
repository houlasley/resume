from ruamel.yaml import YAML
from ruamel.yaml.representer import RoundTripRepresenter
from pathlib import Path


def write_formatting(f):
    f.write("""
            \\documentclass[letterpaper,11pt]{article}
            
            \\usepackage{latexsym}
            \\usepackage[empty]{fullpage}
            \\usepackage{titlesec}
            \\usepackage{marvosym}
            \\usepackage[usenames,dvipsnames]{color}
            \\usepackage{verbatim}
            \\usepackage{enumitem}
            \\usepackage[hidelinks]{hyperref}
            \\usepackage{fancyhdr}
            \\usepackage[english]{babel}
            \\usepackage{tabularx}
            \\input{glyphtounicode}
            
            
            %----------FONT OPTIONS----------
            \\usepackage[sfdefault]{roboto}
            
            
            \\pagestyle{fancy}
            \\fancyhf{} % clear all header and footer fields
            \\fancyfoot{}
            \\renewcommand{\\headrulewidth}{0pt}
            \\renewcommand{\\footrulewidth}{0pt}
            
            % Adjust margins
            \\addtolength{\\oddsidemargin}{-0.5in}
            \\addtolength{\\evensidemargin}{-0.5in}
            \\addtolength{\\textwidth}{1in}
            \\addtolength{\\topmargin}{-.5in}
            \\addtolength{\\textheight}{1.0in}
            
            \\urlstyle{same}
            
            \\raggedbottom
            \\raggedright
            \\setlength{\\tabcolsep}{0in}
            
            % Sections formatting
            \\titleformat{\\section}{
              \\vspace{-4pt}\\scshape\\raggedright\\large
            }{}{0em}{}[\\color{black}\\titlerule \\vspace{-5pt}]
            
            % Ensure that generate pdf is machine readable/ATS parsable
            \\pdfgentounicode=1


            \\newcommand{\\resumeItem}[1]{
                \\item\\small{
                {#1 \\vspace{-2pt}}
            }
            }

            \\newcommand{\\resumeSubheading}[4]{
              \\vspace{-2pt}\\item
                \\begin{tabular*}{0.97\\textwidth}[t]{l@{\\extracolsep{\\fill}}r}
                  \\textbf{#1} & #2 \\\\
                  \\textit{\\small#3} & \\textit{\\small #4} \\\\
                \\end{tabular*}\\vspace{-7pt}
            }
            
            \\newcommand{\\resumeSubSubheading}[2]{
                \\item
                \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}
                  \\textit{\\small#1} & \\textit{\\small #2} \\\\
                \\end{tabular*}\\vspace{-7pt}
            }
            
            \\newcommand{\\resumeProjectHeading}[2]{
                \\item
                \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}
                  \\small#1 & #2 \\\\
                \\end{tabular*}\\vspace{-7pt}
            }
            
            \\newcommand{\\resumeSubItem}[1]{\\resumeItem{#1}\\vspace{-4pt}}
            
            \\renewcommand\\labelitemii{$\\vcenter{\\hbox{\\tiny$\\bullet$}}$}
            
            \\newcommand{\\resumeSubHeadingListStart}{\\begin{itemize}[leftmargin=0.15in, label={}]}
            \\newcommand{\\resumeSubHeadingListEnd}{\\end{itemize}}
            \\newcommand{\\resumeItemListStart}{\\begin{itemize}}
            \\newcommand{\\resumeItemListEnd}{\\end{itemize}\\vspace{-5pt}}""")


def write_header(f):
    f.write("""
        \\begin{document}
        \\begin{center}
            \\textbf{\\Huge \\scshape Louis Hasley} \\\\ \\vspace{1pt}
            \\small 319-360-0125 $|$ \\href{mailto:louiemhasley@gmail.com}{\\underline{louiemhasley@gmail.com}} $|$ 
            \\href{https://linkedin.com/in/louis-hasley}{\\underline{LinkedIn}} $|$
            %\\href{https://github.com/houlasley}{\\underline{GitHub}}
        \\end{center}
            """)


def write_skills(f, yaml_data):
    f.write("""
        \\section{Technical Skills}
            \\begin{itemize}[leftmargin=0.15in, label={}]
                \\small{\\item{
        """)
    for skill in yaml_data["skills"]:
        f.write(
            f"""
            \\textbf{{{skill['area']}}}: {', '.join(skill['bullets'])} \\\\
            """
        )

    f.write("""
            }}
                \\end{itemize}
            """)

    pass


def write_experience(f, yaml_data):
    f.write("""
            \\section{Experience}
              \\resumeSubHeadingListStart
            """)
    for job in yaml_data["experience"]:
        f.write(
            f"""
                \\resumeSubheading
                  {{{job['job_title']}}}{{{job['date']}}}
                  {{{job['company']}}}{{{job['location']}}}
            """
        )
        f.write("""
                  \\resumeItemListStart\n""")
        for bullet in job["bullets"]:
            f.write(f"""\t\t\t\\resumeItem{{{bullet}}}\n""")
        f.write("""\\resumeItemListEnd\n""")
    f.write("""
            \\resumeSubHeadingListEnd
            """)


def write_education(f):
    f.write("""
        \\section{Education}
          \\resumeSubHeadingListStart
            \\resumeSubheading
              {University of Iowa}{Iowa City, IA}
              {MS in Business Analytics}{May 2021}
            \\resumeSubSubheading
              {BBA in Business Analytics}{May 2020}
            \\resumeSubSubheading
              {BBA in Finance}{May 2020}
          \\resumeSubHeadingListEnd
            """)
    pass


def write_footer(f):
    f.write("\\end{document}")


def load_yaml(file):
    """Load YAML file."""
    with open(file, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class SingleLineDumper(yaml.Dumper):
    """Custom YAML Dumper to ensure list items remain single-line without quotes."""

    def represent_scalar(self, tag, value, style=None):
        if isinstance(value, str) and "\n" in value:
            value = value.replace("\n", " ")  # Convert newlines to spaces
            style = None  # Forces plain text (no quotes)
        return super().represent_scalar(tag, value, style)


def repr_str(dumper: RoundTripRepresenter, data: str):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


newyaml = YAML()
newyaml.representer.add_representer(str, repr_str)


def save_yaml(filename, data):
    """Save YAML ensuring all list items remain single-line."""
    with open(filename, "w") as file:
        newyaml.dump(
            data, file, default_flow_style=False, allow_unicode=True, sort_keys=False
        )


def compare_and_update_cv(cv_data, resume_data):
    """Compare resume.yaml with cv.yaml and update cv.yaml with missing bullets."""
    updated = False

    for resume_job in resume_data.get("experience", []):
        for cv_job in cv_data.get("experience", []):
            if (
                resume_job["job_title"] == cv_job["job_title"]
                and resume_job["company"] == cv_job["company"]
            ):
                # Find missing bullets
                missing_bullets = [
                    b for b in resume_job["bullets"] if b not in cv_job["bullets"]
                ]
                if missing_bullets:
                    print(
                        f"""Adding {len(missing_bullets)} missing bullet(s) to {resume_job['job_title']} at {resume_job['company']}
                        {', '.join(missing_bullets)}
                        """
                    )
                    cv_job["bullets"].extend(missing_bullets)
                    updated = True

    for resume_skill in resume_data.get("skills", []):
        for cv_skill in cv_data.get("skills", []):
            if resume_skill["area"] == cv_skill["area"]:
                missing_bullets = [
                    b for b in resume_skill["bullets"] if b not in cv_skill["bullets"]
                ]
                if missing_bullets:
                    print(
                        f"""Adding {len(missing_bullets)} missing skill(s) to {resume_skill['area']}
                        {', '.join(missing_bullets)}
                        """
                    )
                    cv_skill["bullets"].extend(missing_bullets)
                    updated = True
    if updated:
        save_yaml("cv.yaml", cv_data)
        print("cv.yaml updated with missing bullets.")
    else:
        print("No updates needed.")


def generate_latex(yaml_data, output_file):
    """Generate LaTeX file from YAML data."""
    latex_path = Path("latex")
    latex_path.mkdir(parents=True, exist_ok=True)

    with open(f"{latex_path}/{output_file}", "w", encoding="utf-8") as f:
        write_formatting(f)
        write_header(f)
        write_skills(f=f, yaml_data=yaml_data)
        write_experience(f=f, yaml_data=yaml_data)
        write_education(f)
        write_footer(f)

    print(f"LaTeX file generated: {output_file}")


def main():
    cv_data = load_yaml("cv.yaml")
    resume_data = load_yaml("resume.yaml")

    # Compare and update cv.yaml with missing bullets from resume.yaml
    compare_and_update_cv(cv_data, resume_data)

    # Generate LaTeX files
    generate_latex(cv_data, "cv.tex")
    generate_latex(resume_data, "resume.tex")


if __name__ == "__main__":
    main()
    # resume_data = load_yaml("resume.yaml")
    # generate_latex(yaml_data=resume_data, output_file="test.tex")
