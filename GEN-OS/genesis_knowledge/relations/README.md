# Relation Engine

Relation Engine — базовый механизм описания связей между сущностями Knowledge Registry.

Каждая связь состоит из:

- source
- target
- relation_type
- weight
- confidence
- metadata

Пример:

Profession

↓

requires

↓

Competency

↓

improves

↓

Variable

↓

affects

↓

Digital Twin

Все остальные подсистемы работают через Relation Engine.

Это фундамент Knowledge Graph.