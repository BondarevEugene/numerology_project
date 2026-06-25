# Propagation Engine

Propagation Engine — вычислительное ядро Genesis.

Любое действие пользователя превращается в событие.

```
Habit

↓

Relation

↓

Competency

↓

Variable

↓

Profession

↓

Prediction
```

Engine не знает ничего о Flask.

Engine не знает ничего о PostgreSQL.

Engine работает только с Registry и Graph.

Это позволяет использовать его:

- Web
- Desktop
- Mobile
- AI Agent
- API
- Tests