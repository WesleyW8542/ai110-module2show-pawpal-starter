from pawpal_system import Task, Pet


def test_task_mark_complete():
    task = Task(title="Test task", task_type="feed", duration_minutes=10)
    assert not task.completed

    task.mark_complete()
    assert task.completed


def test_pet_add_task_increases_count():
    pet = Pet(name="Mochi", species="dog")
    initial_count = len(pet.tasks)

    task = Task(title="Walk", task_type="walk", duration_minutes=20)
    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1
    assert pet.tasks[-1] is task
