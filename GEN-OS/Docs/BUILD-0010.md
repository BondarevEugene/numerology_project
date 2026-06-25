BUILD-0010
Knowledge Packs

Теперь мы будем хранить не код, а знания.

Именно их потом будет импортировать Excel, ESCO, O*NET, AI.



Никакого Python.

BUILD-0010
Career Domain

Создаем

genesis_knowledge/
└── domains/
    └── career/
        │
        ├── professions/
        ├── competencies/
        ├── industries/
        ├── tools/
        ├── environments/
        ├── salaries/
        ├── futures/
        ├── relations/
        └── README.md

BUILD-0011
Development Domain
development/

habits/

books/

courses/

protocols/

sports/

hobbies/

projects/

relations/
BUILD-0012
Psychology Domain
psychology/

traits/

strengths/

weaknesses/

motivation/

temperament/

thinking/

emotions/

relations/
BUILD-0013
Education Domain
education/

schools/

universities/

certifications/

learning_styles/

courses/

relations/
BUILD-0014
Health Domain
health/

sleep/

nutrition/

activity/

stress/

burnout/

relations/
BUILD-0015
Finance Domain
finance/

income/

expenses/

wealth/

investments/

relations/
А теперь самое важное.
Мы перестаем писать JSON вручную.

Мы создаем Knowledge Package.

Например

software_engineer/

сразу содержит ВСЕ.

software_engineer/

    entity.json

    competencies.json

    books.json

    sports.json

    habits.json

    hobbies.json

    environments.json

    salary.json

    future.json

    roadmap.json

Именно это станет импортируемой единицей.

Не одна профессия.

А полный Knowledge Pack профессии.

Пример
Software Engineer

↓

Импортировали

↓

автоматически получили

✅ компетенции

✅ книги

✅ привычки

✅ спорт

✅ обучение

✅ карьерные уровни

✅ зарплаты

✅ AI roadmap

Тогда Import Station становится невероятно простой.
ESCO

↓

Knowledge Pack

↓

Registry

↓

Graph

↓

Done
Дальше начинается то, что я считаю самым важным модулем всего проекта.
BUILD-0016
Competency DNA

Это уже не список компетенций.

Это "генетика профессионального развития".

Например:

Leadership

├── развивается
│
├── ухудшается
│
├── профессии
│
├── книги
│
├── спорт
│
├── игры
│
├── окружение
│
├── возраст
│
├── дети
│
├── взрослые
│
├── AI советы
│
├── ежедневные упражнения
│
├── привычки
│
├── протоколы
│
└── метрики