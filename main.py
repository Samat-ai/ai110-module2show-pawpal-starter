"""CLI demo for PawPal+ scheduling behavior."""

from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def print_schedule(title: str, schedule: list[tuple[Pet, Task]]) -> None:
    """Print a clean, readable schedule to the terminal."""
    print(f"\n{title}")
    print("-" * len(title))
    if not schedule:
        print("No tasks scheduled.")
        return
    for pet, task in schedule:
        status = "done" if task.completed else "pending"
        print(
            f"{task.scheduled_date.isoformat()} {task.time} | {pet.name:<8} | "
            f"{task.description:<18} | {task.priority:<6} | {task.frequency:<6} | {status}"
        )


def main() -> None:
    """Build sample data and print scheduling results."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)

    today = date.today()
    mochi.add_task(Task("Medication", "09:00", priority="high", frequency="daily", scheduled_date=today))
    mochi.add_task(Task("Morning walk", "08:00", priority="high", frequency="daily", scheduled_date=today))
    luna.add_task(Task("Breakfast", "08:00", priority="medium", frequency="daily", scheduled_date=today))
    luna.add_task(Task("Vet appointment", "14:30", priority="high", frequency="once", scheduled_date=today))

    scheduler = Scheduler(owner)

    schedule = scheduler.build_schedule(scheduled_for=today)
    print_schedule("Today's Schedule", schedule)

    print("\nConflict Warnings")
    print("-----------------")
    warnings = scheduler.detect_conflicts(schedule)
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("No conflicts detected.")

    scheduler.mark_task_complete(
        pet_name="Mochi",
        description="Morning walk",
        task_time="08:00",
        scheduled_for=today,
    )
    next_day_tasks = scheduler.build_schedule(scheduled_for=today + timedelta(days=1))
    print_schedule("Next Day Recurring Tasks", next_day_tasks)


if __name__ == "__main__":
    main()
