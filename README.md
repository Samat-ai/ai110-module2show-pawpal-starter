# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Sample CLI output from `python main.py`:

```text
Today's Schedule
----------------
2026-07-07 08:00 | Mochi    | Morning walk       | high   | daily  | pending
2026-07-07 08:00 | Luna     | Breakfast          | medium | daily  | pending
2026-07-07 09:00 | Mochi    | Medication         | high   | daily  | pending
2026-07-07 14:30 | Luna     | Vet appointment    | high   | once   | pending

Conflict Warnings
-----------------
- Conflict at 2026-07-07 08:00 -> Mochi: Morning walk, Luna: Breakfast

Next Day Recurring Tasks
------------------------
2026-07-08 08:00 | Mochi    | Morning walk       | high   | daily  | pending
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite
python -m pytest
```

Sample test output:

```text
============================= test session starts =============================
collected 5 items

tests/test_pawpal.py .....                                              [100%]

============================== 5 passed in 0.04s ==============================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Sorts by date + HH:MM |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet, completion state, and date |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags duplicate date/time slots with warning strings |
| Recurring tasks | `Task.next_occurrence()`, `Scheduler.mark_task_complete()` | Daily and weekly tasks auto-create next instance |

**Confidence Level:** ⭐⭐⭐⭐⭐ (5/5)

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Launch the app with `streamlit run app.py`, then enter or confirm the owner name.
2. Add one or more pets in the **Add Pet** section.
3. Add tasks in **Add Task** by selecting a pet, time (`HH:MM`), priority, and frequency (`once`, `daily`, `weekly`).
4. View **Today's Schedule**, which is pulled from backend `Scheduler` logic and sorted by time.
5. Review conflict warnings shown with `st.warning` when two tasks share the same date/time slot.

**Screenshot or video** *(optional)*: Not included.
