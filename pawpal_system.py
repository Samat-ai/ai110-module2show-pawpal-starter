"""Core backend models and scheduling logic for the PawPal+ app."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import Optional


def _parse_time(value: str) -> datetime.time:
    """Parse HH:MM text into a time object."""
    return datetime.strptime(value, "%H:%M").time()


@dataclass
class Task:
    """Represents one pet-care action scheduled for a specific date and time."""

    description: str
    time: str
    priority: str = "medium"
    frequency: str = "once"
    scheduled_date: date = field(default_factory=date.today)
    completed: bool = False

    def __post_init__(self) -> None:
        """Validate key task fields after construction."""
        _parse_time(self.time)
        if self.priority not in {"low", "medium", "high"}:
            raise ValueError("priority must be one of: low, medium, high")
        if self.frequency not in {"once", "daily", "weekly"}:
            raise ValueError("frequency must be one of: once, daily, weekly")

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.completed = True

    def next_occurrence(self) -> Optional["Task"]:
        """Return the next recurring task instance, if this task recurs."""
        if self.frequency == "daily":
            next_date = self.scheduled_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.scheduled_date + timedelta(days=7)
        else:
            return None

        return Task(
            description=self.description,
            time=self.time,
            priority=self.priority,
            frequency=self.frequency,
            scheduled_date=next_date,
        )


@dataclass
class Pet:
    """Represents one pet and its care task list."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def task_count(self) -> int:
        """Return the number of tasks currently attached to this pet."""
        return len(self.tasks)


class Owner:
    """Represents an owner who manages one or more pets."""

    def __init__(self, name: str) -> None:
        """Initialize owner metadata and pet collection."""
        self.name = name
        self._pets: dict[str, Pet] = {}

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self._pets[pet.name] = pet

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Return a pet by name if it exists."""
        return self._pets.get(pet_name)

    def list_pets(self) -> list[Pet]:
        """Return all pets for this owner."""
        return list(self._pets.values())

    def all_task_entries(self) -> list[tuple[Pet, Task]]:
        """Return every task paired with its source pet."""
        entries: list[tuple[Pet, Task]] = []
        for pet in self._pets.values():
            entries.extend((pet, task) for task in pet.tasks)
        return entries


class Scheduler:
    """Coordinates filtering, sorting, conflicts, and completion workflows."""

    def __init__(self, owner: Owner) -> None:
        """Attach a scheduler to one owner context."""
        self.owner = owner

    def sort_by_time(self, task_entries: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Return tasks sorted chronologically by date then HH:MM time."""
        return sorted(task_entries, key=lambda entry: (entry[1].scheduled_date, _parse_time(entry[1].time)))

    def filter_tasks(
        self,
        task_entries: Optional[list[tuple[Pet, Task]]] = None,
        *,
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
        scheduled_for: Optional[date] = None,
    ) -> list[tuple[Pet, Task]]:
        """Filter task entries by pet, completion state, and/or date."""
        entries = task_entries if task_entries is not None else self.owner.all_task_entries()
        filtered: list[tuple[Pet, Task]] = []
        for pet, task in entries:
            if pet_name is not None and pet.name != pet_name:
                continue
            if completed is not None and task.completed != completed:
                continue
            if scheduled_for is not None and task.scheduled_date != scheduled_for:
                continue
            filtered.append((pet, task))
        return filtered

    def build_schedule(
        self,
        *,
        scheduled_for: Optional[date] = None,
        pet_name: Optional[str] = None,
        include_completed: bool = False,
    ) -> list[tuple[Pet, Task]]:
        """Build a sorted schedule for a date with optional pet filtering."""
        target_date = scheduled_for if scheduled_for is not None else date.today()
        entries = self.filter_tasks(
            pet_name=pet_name,
            completed=None if include_completed else False,
            scheduled_for=target_date,
        )
        return self.sort_by_time(entries)

    def detect_conflicts(self, task_entries: Optional[list[tuple[Pet, Task]]] = None) -> list[str]:
        """Detect duplicate date/time slots and return human-readable warnings."""
        entries = task_entries if task_entries is not None else self.owner.all_task_entries()
        grouped: dict[tuple[date, str], list[tuple[Pet, Task]]] = {}
        for pet, task in entries:
            grouped.setdefault((task.scheduled_date, task.time), []).append((pet, task))

        warnings: list[str] = []
        for (scheduled_date, task_time), same_slot in grouped.items():
            if len(same_slot) < 2:
                continue
            summary = ", ".join(f"{pet.name}: {task.description}" for pet, task in same_slot)
            warnings.append(f"Conflict at {scheduled_date.isoformat()} {task_time} -> {summary}")
        return warnings

    def mark_task_complete(
        self,
        *,
        pet_name: str,
        description: str,
        task_time: str,
        scheduled_for: Optional[date] = None,
    ) -> Task:
        """Complete a task and enqueue the next recurrence when applicable."""
        pet = self.owner.get_pet(pet_name)
        if pet is None:
            raise ValueError(f"pet not found: {pet_name}")

        target_date = scheduled_for if scheduled_for is not None else date.today()
        for task in pet.tasks:
            if (
                task.description == description
                and task.time == task_time
                and task.scheduled_date == target_date
                and not task.completed
            ):
                task.mark_complete()
                next_task = task.next_occurrence()
                if next_task is not None:
                    pet.add_task(next_task)
                return task

        raise ValueError("task not found or already completed")
