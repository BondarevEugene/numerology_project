BUILD-0017 — Knowledge Workspace

Это будет первый по-настоящему мощный GUI Genesis, где знания будут не просто храниться,
а визуально строиться как граф. И именно этот инструмент станет основной рабочей средой для
наполнения всей платформы в течение следующих месяцев. Он одновременно ускорит разработку MVP
и избавит нас от огромного объема ручной работы с файлами.

BUILD-0017
Knowledge Workspace

Структура:

GEN-OS/
│
├── UI/
│
│   ├── workspace/
│   │
│   │   knowledge_workspace.html
│   │   knowledge_workspace.css
│   │   knowledge_workspace.js
│   │
│   ├── panels/
│   │
│   │   entity_tree.html
│   │   entity_editor.html
│   │   relation_editor.html
│   │   relation_graph.html
│   │   inspector.html
│   │   toolbar.html
│   │
│   └── dialogs/
│
└── genesis/
Вот что увидит пользователь.
┌──────────────────────────────────────────────────────────────┐
│ GENESIS KNOWLEDGE WORKSPACE                                  │
├──────────────────────────────────────────────────────────────┤
│ Toolbar                                                      │
├───────────────┬──────────────────────────────┬───────────────┤
│               │                              │               │
│ Entity Tree   │     Entity Workspace         │   Inspector   │
│               │                              │               │
│ Career        │  Leadership                  │  Relations    │
│  Profession   │                              │               │
│  Competency   │  Description                 │  + Add        │
│               │                              │               │
│ Development   │  Tags                        │  Books        │
│               │                              │  Habits       │
│               │  Metadata                    │  Sports       │
│               │                              │               │
│               │                              │  Weight       │
├───────────────┴──────────────────────────────┴───────────────┤
│ Status                                                       │
└──────────────────────────────────────────────────────────────┘

Вот это уже IDE.

Дальше.

Мы больше никогда не будем делать страницу

Profession Registry

или

Competency Registry

Их не существует.

Есть

Knowledge Workspace

В нем меняется только тип сущности.

Например

Leadership

↓

Открыли.

↓

Справа

Developed by

Basketball

Reading

Mentoring

Leadership Camp

Открыли

Basketball

↓

получили

Develops

Leadership

Communication

Stress Resistance

Discipline

Teamwork