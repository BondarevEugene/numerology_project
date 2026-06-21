спринт полностью посвящен Capability Graph.
BUILD-0008 — Capability Knowledge Graph

Новые сущности:

✅ Profession
✅ Competency
✅ Habit
✅ Hobby
✅ Sport
✅ Book
✅ Course
✅ Behavior
✅ Environment
✅ Protocol

И новый набор связей:

✅ requires
✅ develops
✅ improves
✅ weakens
✅ supports
✅ recommends
✅ contraindicated_for
✅ useful_for_children
✅ useful_for_adults

                Profession

                     │

             requires 95

                     │

             Leadership

         ┌────────┼────────┐

      Sport     Habit     Book

         │          │          │

Basketball   Daily Planning  Extreme Ownership

         │          │          │

        +8         +3          +5


СУТЬ:
Это будет первая действительно "умная" часть Genesis.
После нее импорт ESCO, O*NET и других справочников станет не просто загрузкой 
профессий, а наполнением живого графа знаний. А затем уже на этом графе можно 
строить HR-матчинг, персональные рекомендации, цифрового двойника человека и прогноз развития.
Именно этот слой, на мой взгляд, станет тем самым "двигателем", вокруг которого 
будет строиться весь продукт.