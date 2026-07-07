from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_sets_task_status() -> None:
    task = Task(description="Evening walk", time="18:00")
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count() -> None:
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(description="Breakfast", time="07:30"))
    assert pet.task_count() == 1


def test_sorting_returns_chronological_order() -> None:
    today = date.today()
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    owner.add_pet(pet)
    pet.add_task(Task("Late task", "18:00", scheduled_date=today))
    pet.add_task(Task("Early task", "07:30", scheduled_date=today))
    pet.add_task(Task("Mid task", "12:00", scheduled_date=today))

    scheduler = Scheduler(owner)
    times = [task.time for _, task in scheduler.build_schedule(scheduled_for=today)]
    assert times == ["07:30", "12:00", "18:00"]


def test_daily_recurrence_creates_next_day_task() -> None:
    today = date.today()
    owner = Owner("Jordan")
    pet = Pet("Mochi", "dog")
    owner.add_pet(pet)
    pet.add_task(Task("Medication", "09:00", frequency="daily", scheduled_date=today))

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(
        pet_name="Mochi",
        description="Medication",
        task_time="09:00",
        scheduled_for=today,
    )

    assert pet.tasks[0].completed is True
    recurrence = [task for task in pet.tasks if task.scheduled_date == today + timedelta(days=1)]
    assert len(recurrence) == 1
    assert recurrence[0].description == "Medication"
    assert recurrence[0].completed is False


def test_conflict_detection_flags_duplicate_time_slots() -> None:
    today = date.today()
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)
    mochi.add_task(Task("Walk", "08:00", scheduled_date=today))
    luna.add_task(Task("Breakfast", "08:00", scheduled_date=today))

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_conflicts(scheduler.build_schedule(scheduled_for=today))
    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "Mochi" in warnings[0]
    assert "Luna" in warnings[0]
