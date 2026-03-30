# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
  - I designed a small domain model around pet care scheduling with separate objects for Owner, Pet, Task, Scheduler, and ScheduledTask. The system is centered on generating a daily plan from a set of tasks while respecting owner availability and task priority.
- What classes did you include, and what responsibilities did you assign to each?
  - `Owner`: store owner profile, availability, and preferences. Responsible for providing constraints and settings to the scheduler.
  - `Pet`: store pet details (name, species, age, care requirements). Responsible for representing pet-specific needs and helping identify required tasks.
  - `Task`: represent a single care activity (title, duration, priority, optional windows). Responsible for task state updates, completion, and validation.
  - `Scheduler`: orchestrate planning. Responsible for selecting and ordering tasks, applying constraints, and producing schedule entries + explanations.
  - `ScheduledTask`: represent a task scheduled at a specific time slot with a reason. Responsible for conflict checking and duration tracking.

Core user actions:

1. Add or edit a pet profile (owner/pet details, preferences, constraints) so the system has context.
2. Add and prioritize care tasks (walking, feeding, meds, enrichment, grooming) including duration requirements.
3. Generate and view a daily plan for today, with scheduled tasks and reasoning for the chosen order.

classDiagram
    class Owner {
        +str name
        +float available_hours
        +dict preferences
        +update_profile()
        +set_availability()
        +get_preference(key)
    }

    class Pet {
        +str name
        +str species
        +int age
        +str health_notes
        +dict care_requirements
        +update_health_notes()
        +needs_task(task_type)
        +summary()
    }

    class Task {
        +str title
        +str task_type
        +int duration_minutes
        +str priority
        +datetime? window_start
        +datetime? window_end
        +bool completed
        +mark_complete()
        +update_priority()
        +adjust_duration()
        +is_overdue(today)
    }

    class ScheduledTask {
        +Task task
        +datetime start_time
        +datetime end_time
        +str reason
        +duration()
        +flag_conflict(other)
    }

    class Scheduler {
        +Owner owner
        +Pet pet
        +List~Task~ tasks
        +date date
        +List~ScheduledTask~ scheduled_items
        +str explanation
        +add_task(task)
        +remove_task(task_id)
        +generate_plan()
        +get_today_tasks()
        +explain_plan()
        +score_plan()
    }

    Owner "1" -- "1" Pet : owns
    Scheduler "1" -- "1" Owner
    Scheduler "1" -- "1" Pet
    Scheduler "1" -- "*" Task
    Scheduler "1" -- "*" ScheduledTask
    ScheduledTask "1" -- "1" Task


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
