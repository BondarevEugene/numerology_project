BUILD-0018 — Knowledge Workspace
ПОлная структура
GEN-OS/
│
├── UI/
│
├── kernel/
│
├── importer/
│
├── ai/
│
└── genesis/
    │
    ├── api/
    │   │
    │   ├── __init__.py
    │   ├── knowledge_api.py
    │   ├── knowledge_routes.py
    │   └── workspace_api.py      (позже)
    │
    ├── services/
    │   │
    │   ├── __init__.py
    │   ├── knowledge_service.py
    │   ├── import_service.py
    │   ├── graph_service.py
    │   └── recommendation_service.py
    │
    ├── loaders/
    │   │
    │   ├── __init__.py
    │   ├── knowledge_loader.py
    │   ├── domain_loader.py
    │   ├── entity_loader.py
    │   └── relation_loader.py
    │
    ├── workspace/
    │
    ├── graph/
    │
    └── registry/

Сразу:

knowledge_workspace.html
knowledge_workspace.css
knowledge_workspace.js
knowledge_api.py
knowledge_service.py
knowledge_loader.py
knowledge_tree.py
knowledge_editor.py
knowledge_routes.py
README.md

GEN-OS/
│
└── UI/
    │
    ├── workspace/
    │      knowledge_workspace.html
    │
    ├── panels/
    │      entity_tree.html
    │      entity_editor.html
    │      relation_editor.html
    │      inspector.html
    │      toolbar.html
    │
    ├── static/
    │
    │   ├── css/
    │   │      knowledge_workspace.css
    │   │
    │   └── js/
    │          knowledge_workspace.js

Что увидим после запуска
┌─────────────────────────────────────────────────────────────────────────────┐
│ GENESIS KNOWLEDGE WORKSPACE                                     BUILD-0018 │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📂 Domains │ 📋 Entity │ 🔗 Relations │ 📈 Graph │ ⚙ Import │ 💾 Save      │
├────────────┬──────────────────────────────┬─────────────────────────────────┤
│            │                              │                                 │
│ Career     │                              │   Selected Entity               │
│            │                              │                                 │
│ ▸Profession│      Leadership              │  ID                             │
│ ▸Skill     │                              │  Tags                           │
│ ▸Industry  │      Description             │  Metadata                       │
│            │                              │                                 │
│ Dev        │                              │  Relations                      │
│            │                              │                                 │
│ Psych      │                              │  develops                       │
│            │                              │  requires                       │
│ Health     │                              │  destroys                       │
│            │                              │  supports                       │
├────────────┴──────────────────────────────┴─────────────────────────────────┤
│ Status : Registry Loaded                                                OK  │
└─────────────────────────────────────────────────────────────────────────────┘
Что будет работать

Сразу.

✅ поиск

✅ дерево

✅ открытие сущности

✅ просмотр

✅ редактирование

✅ связи

Без графа пока.

Граф будет BUILD-0020.
