from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional, Dict

@dataclass
class Owner:
    name: str
    available_hours: float = 0.0
    preferences: Dict[str, str] = field(default_factory=dict)

    def update_profile(self, *, name: Optional[str] = None) -> None:
        if name:
            self.name = name

    def set_availability(self, hours: float) -> None:
        self.available_hours = hours

    def get_preference(self, key: str) -> Optional[str]:
        return self.preferences.get(key)

    def set_preference(self, key: str, value: str) -> None:
        self.preferences[key] = value

@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    health_notes: str = ""
    care_requirements: Dict[str, str] = field(default_factory=dict)

    def update_health_notes(self, notes: str) -> None:
        self.health_notes = notes

    def needs_task(self, task_type: str) -> bool:
        return task_type in self.care_requirements

    def summary(self) -> str:
        return f"{self.name} ({self.species}, age {self.age})"

@dataclass
class Task:
    title: str
    task_type: str
    duration_minutes: int
    priority: str = "medium"
    window_start: Optional[datetime] = None
    window_end: Optional[datetime] = None
    completed: bool = False

    def mark_complete(self) -> None:
        self.completed = True

    def update_priority(self, priority: str) -> None:
        self.priority = priority

    def adjust_duration(self, duration_minutes: int) -> None:
        self.duration_minutes = duration_minutes

    def is_overdue(self, now: datetime) -> bool:
        if self.window_end is None:
            return False
        return now > self.window_end and not self.completed

@dataclass
class ScheduledTask:
    task: Task
    start_time: datetime
    end_time: datetime
    reason: Optional[str] = None

    def duration(self) -> int:
        return int((self.end_time - self.start_time).total_seconds() // 60)

    def flag_conflict(self, other: 'ScheduledTask') -> bool:
        return not (self.end_time <= other.start_time or self.start_time >= other.end_time)

@dataclass
class Scheduler:
    owner: Owner
    pet: Pet
    tasks: List[Task] = field(default_factory=list)
    date: date = field(default_factory=date.today)
    scheduled_items: List[ScheduledTask] = field(default_factory=list)
    explanation: str = ""

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        self.tasks = [t for t in self.tasks if t is not task]

    def get_today_tasks(self) -> List[Task]:
        return [t for t in self.tasks if not t.completed]

    def generate_plan(self) -> List[ScheduledTask]:
        # TODO: implement scheduling algorithm based on priority/availability
        self.scheduled_items = []
        self.explanation = "Plan generation not implemented yet."
        return self.scheduled_items

    def explain_plan(self) -> str:
        return self.explanation

    def score_plan(self) -> float:
        # TODO: implement scoring logic for schedule quality
        return 0.0
