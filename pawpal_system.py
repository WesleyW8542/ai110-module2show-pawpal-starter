from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from typing import List, Optional, Dict

@dataclass
class Task:
    title: str
    task_type: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "daily" 
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.completed = True

    def mark_pending(self) -> None:
        """Mark this task as pending/incomplete."""
        self.completed = False

    def update_duration(self, duration_minutes: int) -> None:
        """Update task duration in minutes."""
        self.duration_minutes = duration_minutes

    def update_priority(self, priority: str) -> None:
        """Set task priority."""
        self.priority = priority

    def is_overdue(self, reference: datetime) -> bool:
        """Return whether the task is overdue compared to reference time."""
        # Placeholder: no strict due date field, but return False for now
        return False


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    health_notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove a task by title from this pet."""
        self.tasks = [t for t in self.tasks if t.title != title]

    def get_tasks(self, include_completed: bool = False) -> List[Task]:
        """Return tasks, optionally including completed tasks."""
        return [t for t in self.tasks if include_completed or not t.completed]

    def summary(self) -> str:
        """Return a short description string for this pet."""
        return f"{self.name} ({self.species}, age {self.age})"


@dataclass
class Owner:
    name: str
    available_hours: float = 8.0
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name."""
        self.pets = [p for p in self.pets if p.name != pet_name]

    def get_pet(self, pet_name: str) -> Optional[Pet]:
        """Get a pet instance by name, or None."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None

    def get_all_tasks(self, include_completed: bool = False) -> List[Task]:
        """Return all tasks for all pets belonging to this owner."""
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks(include_completed=include_completed))
        return tasks


@dataclass
class ScheduledTask:
    task: Task
    pet: Pet
    start_time: datetime
    end_time: datetime
    reason: Optional[str] = None

    def duration(self) -> int:
        """Return the scheduled task duration in minutes."""
        return int((self.end_time - self.start_time).total_seconds() // 60)

    def conflicts_with(self, other: ScheduledTask) -> bool:
        """Return whether this scheduled task conflicts with another one."""
        return not (self.end_time <= other.start_time or self.start_time >= other.end_time)


@dataclass
class Scheduler:
    owner: Owner
    date: date = field(default_factory=date.today)
    scheduled_items: List[ScheduledTask] = field(default_factory=list)
    explanation: str = ""

    def get_pending_tasks(self) -> List[Task]:
        """Return pending tasks for the owner across all pets."""
        return self.owner.get_all_tasks(include_completed=False)

    def get_tasks_sorted(self) -> List[Task]:
        """Return pending tasks sorted by priority, duration, and creation time."""
        priority_rank = {"high": 1, "medium": 2, "low": 3}
        tasks = self.get_pending_tasks()
        return sorted(tasks, key=lambda t: (priority_rank.get(t.priority, 2), -t.duration_minutes, t.created_at))

    def generate_plan(self, start_time: datetime = None) -> List[ScheduledTask]:
        """Build a schedule given available hours and task priorities."""
        if start_time is None:
            start_time = datetime.combine(self.date, datetime.min.time()).replace(hour=8, minute=0)

        self.scheduled_items = []
        remaining_minutes = int(self.owner.available_hours * 60)
        current_time = start_time

        for task in self.get_tasks_sorted():
            if task.duration_minutes > remaining_minutes:
                continue

            end_time = current_time + timedelta(minutes=task.duration_minutes)
            assigned_pet = next((pet for pet in self.owner.pets if task in pet.tasks), None)
            if assigned_pet is None:
                continue

            scheduled = ScheduledTask(task=task, pet=assigned_pet, start_time=current_time, end_time=end_time,
                                      reason=f"Priority {task.priority}")
            self.scheduled_items.append(scheduled)
            current_time = end_time
            remaining_minutes -= task.duration_minutes
            task.mark_complete()

        if not self.scheduled_items:
            self.explanation = "No tasks could be scheduled within available hours."
        else:
            self.explanation = f"Scheduled {len(self.scheduled_items)} tasks in order of priority."

        return self.scheduled_items

    def explain_plan(self) -> str:
        """Return a human-friendly explanation of how the plan was generated."""
        return self.explanation

    def score_plan(self) -> float:
        """Score the plan effectiveness based on completed tasks ratio."""
        if not self.scheduled_items:
            return 0.0
        completed = len(self.scheduled_items)
        total = len(self.owner.get_all_tasks(include_completed=True))
        if total == 0:
            return 1.0
        return completed / total
