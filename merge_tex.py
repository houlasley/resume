import difflib


def merge_tex(cv_file, resume_file, output_file="new_cv.tex"):
    """Merges resume.tex into cv.tex while keeping variations but preventing duplicates."""

    # Read both files
    with (
        open(cv_file, "r", encoding="utf-8") as cv,
        open(resume_file, "r", encoding="utf-8") as resume,
    ):
        cv_lines = cv.readlines()
        resume_lines = resume.readlines()

    merged_lines = []
    seen_lines = set()  # Track lines to prevent exact duplicates
    cv_index = 0

    for resume_line in resume_lines:
        stripped_resume_line = resume_line.strip()

        # If the line is already in cv.tex exactly, skip it
        if stripped_resume_line in [line.strip() for line in cv_lines]:
            continue

        # If it's similar to a line in cv.tex, replace it
        if cv_index < len(cv_lines):
            stripped_cv_line = cv_lines[cv_index].strip()
            similarity = difflib.SequenceMatcher(
                None, stripped_resume_line, stripped_cv_line
            ).ratio()

            if similarity > 0.9:  # If it's a slight variation, replace the old one
                if stripped_cv_line not in seen_lines:  # Prevent duplicates
                    merged_lines.append(resume_line)
                    seen_lines.add(stripped_resume_line)
                cv_index += 1
                continue

        # If it's a new line, add it
        if stripped_resume_line and stripped_resume_line not in seen_lines:
            merged_lines.append(resume_line)
            seen_lines.add(stripped_resume_line)

    # Add remaining lines from cv.tex that were not checked
    while cv_index < len(cv_lines):
        stripped_cv_line = cv_lines[cv_index].strip()
        if stripped_cv_line not in seen_lines:
            merged_lines.append(cv_lines[cv_index])
            seen_lines.add(stripped_cv_line)
        cv_index += 1

    # Write merged content back to cv.tex
    with open(output_file, "w", encoding="utf-8") as merged_cv:
        merged_cv.writelines(merged_lines)

    print(f"Updated {output_file} with merged content from {resume_file}")


# Usage
merge_tex("cv.tex", "resume.tex")

