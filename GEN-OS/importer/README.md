# Genesis Import Framework
---
## Supported Sources
- Excel
- CSV
- ESCO (planned)
- O*NET (planned)
---
## Import Flow
Reader
↓
Mapper
↓
Validator
↓
Preview
↓
Processor
↓
Database
---
## Principles

- Reader никогда не знает о БД.
- Processor никогда не читает Excel.
- Engine только управляет Pipeline.
- Import Center работает только через Engine.
---
Version
Genesis 3.0