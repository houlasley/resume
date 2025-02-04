create-resume company:
    dagger call get-artifacts --source=. --output=outputs/{{company}}
    mv outputs/{{company}}/cv.yaml .
