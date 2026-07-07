# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

I centered the design around four classes: `Owner`, `Pet`, `Task`, and `Scheduler`.
`Owner` stores and manages pets, `Pet` stores identity plus its list of `Task` objects, `Task` holds scheduling details (description, time, date, priority, frequency, completion), and `Scheduler` is the orchestration layer for sorting, filtering, conflict detection, and completion workflows.

Three core user actions I designed for:
1. Add a pet to an owner profile.
2. Add scheduled care tasks (walk/feed/medication/appointment) to a selected pet.
3. Generate and review a daily schedule with conflict warnings.

**b. Design changes**

Yes. I initially considered putting sorting and filtering methods on `Pet`, but moved them into `Scheduler` to keep domain models simple and centralize algorithmic behavior in one place.
I also added `Task.next_occurrence()` after implementing recurrence so the recurrence rule lives with the task object while `Scheduler.mark_task_complete()` controls when to create the next task.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler currently considers date, exact time (`HH:MM`), completion status, pet selection, and recurrence frequency (`once`, `daily`, `weekly`).
I prioritized chronological clarity and predictable behavior first (sort/filter/recurrence/conflicts) before adding more complex optimization constraints.

**b. Tradeoffs**

A key tradeoff is that conflict detection only flags exact date/time collisions, not partial overlaps with durations.
That is reasonable for this version because tasks only store one timestamp (not start/end ranges), and the lightweight warning is enough to demonstrate core algorithmic logic without overcomplicating the model.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI for architecture scaffolding, implementing class methods, and producing a clean first draft of tests and UI wiring.
The most useful prompts were specific and code-grounded, such as asking how `Scheduler` should retrieve tasks from `Owner` and how to structure recurrence with `timedelta`.

**b. Judgment and verification**

I rejected a suggestion to keep all behavior in large utility functions because it weakened the class responsibilities.
I kept recurrence behavior split between `Task` and `Scheduler` to preserve object boundaries and then verified behavior through targeted pytest cases.

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion, task addition to pets, chronological sorting, daily recurrence creation, and conflict detection.
These are important because they validate the highest-risk interactions where class coordination matters most.

**b. Confidence**

I am highly confident for the current project scope because all core behaviors pass automated tests and match expected CLI/UI behavior.
Next I would test invalid time formats from UI inputs, duplicate pet names, weekly recurrence edge cases across month boundaries, and empty-state behavior with larger mixed task sets.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the modular architecture: the logic layer works independently in CLI tests and is then reused directly in Streamlit.

**b. What you would improve**

I would add task duration and true overlap detection, then expose more scheduler constraints (owner availability windows and priority weighting).

**c. Key takeaway**

The key takeaway is that AI is strongest when guided by a clear class design; human architectural judgment is still essential to keep solutions maintainable and aligned with project goals.
