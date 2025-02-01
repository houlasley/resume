
Feature
    1. call OpenAI from dagger
        figure out a default prompt that 
            - limits output about 17 bullet points
            - formats yaml
            - more things
            - no special formatting or bolding
            - escape any characters that might be difficult to parse
            - no periods at the end
            - no duplicate bullets. Nothing about 80%? similarity
            - make a limit on the number of skills
    2. dagger call generate resume
        - potentially adjust resume
        - instead of passing in source=., pass in an output/{company_name} ???

DevEx
    3. Clean up cv.yaml
        - Find bullets that are too similar

sample workflow
    dagger call pipeline --update-cv=False (only True if we like the changes to avoid junk)
        pipeline =
            get GPT recommendation(JD, cv.yaml) => resume.yaml
            generate_latex(resume.yaml) => resume.tex
            generate_resume(resume.tex) => resume.pdf
 
