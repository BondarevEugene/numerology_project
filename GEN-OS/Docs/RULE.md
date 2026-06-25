GENESIS RULE №31

Все знания — это граф.

Мы никогда больше не будем создавать специальные таблицы вида:

profession_books
profession_hobbies
competency_courses
profession_traits
...

Мы делаем ОДНУ универсальную систему отношений.

Поэтому предлагаю следующее правило проекта
GENOS RULE №1

Workspace никогда не знает про Shell.

GENOS RULE №2

Shell никогда не знает внутренностей Workspace.

GENOS RULE №3

Workspace общается только через API.

Тогда структура становится очень красивой
templates/

    genos_shell.html

    workspaces/

        digital_twin.html

        career_workspace.html

        import_workspace.html

        knowledge_workspace.html

        simulation_workspace.html

        ai_workspace.html

А рядом

static/js/workspaces/

        digital_twin.js

        career.js

        import.js

        knowledge.js

        simulation.js

        ai.js

И рядом

routes/

        workspace_routes.py

====
С этого момента ни один новый модуль не создается "сам по себе".

Для каждого нового функционального блока мы будем создавать ровно четыре файла:

workspaces/
    <module>_workspace.html

static/js/workspaces/
    <module>_workspace.js

routes/
    <module>_routes.py   (или общий workspace_routes.py)

services/
    <module>_service.py

Эта структура будет одинаковой для Import, AI, Career, Knowledge, Digital Twin, 
Simulation и любых будущих модулей. Через полгода ты сможешь открыть проект и мгновенно 
понимать, где находится любой функционал. Именно такой предсказуемый каркас позволит GEN-OS 
расти до действительно большого коммерческого продукта.