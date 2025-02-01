default: (say "something sweet")

say hello:
    echo {{hello}}

create-resume company:
    dagger call get-artifacts --source=. --output=outputs/{{company}}
    mv outputs/{{company}}/cv.yaml .
