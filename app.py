import streamlit as st
from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ smart pet care dashboard.

This app is connected to the backend logic in `pawpal_system.py` and demonstrates
pet management, task scheduling, sorting, and conflict warnings in one interface.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

The scheduler logic is connected to this UI through Owner/Pet/Task/Scheduler classes.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
Current implementation:
- Represent pet care tasks with date, time, priority, and recurrence
- Represent the pet and owner with object-oriented classes
- Build a sorted daily schedule and display it in tabular form
- Surface scheduling conflicts as warnings
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
if "owner" not in st.session_state or st.session_state.owner.name != owner_name:
    st.session_state.owner = Owner(owner_name)
st.session_state.scheduler = Scheduler(st.session_state.owner)

st.markdown("### Add Pet")
pet_name_input = st.text_input("Pet name", value="Mochi")
species_input = st.selectbox("Species", ["dog", "cat", "other"])
if st.button("Add pet"):
    if not pet_name_input.strip():
        st.warning("Pet name cannot be empty.")
    elif st.session_state.owner.get_pet(pet_name_input.strip()):
        st.warning("That pet already exists.")
    else:
        st.session_state.owner.add_pet(Pet(name=pet_name_input.strip(), species=species_input))
        st.success(f"Added pet: {pet_name_input.strip()}")

pets = st.session_state.owner.list_pets()
if pets:
    st.table([{"name": pet.name, "species": pet.species, "tasks": pet.task_count()} for pet in pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()
st.markdown("### Add Task")
if not pets:
    st.caption("Create a pet before adding tasks.")
else:
    selected_pet = st.selectbox("Choose pet", [pet.name for pet in pets])
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        task_time = st.text_input("Time (HH:MM)", value="08:00")
    with col3:
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
    task_priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)
    task_date = st.date_input("Date", value=date.today())

    if st.button("Add task"):
        pet = st.session_state.owner.get_pet(selected_pet)
        if pet is None:
            st.warning("Selected pet was not found.")
        else:
            try:
                pet.add_task(
                    Task(
                        description=task_title.strip(),
                        time=task_time.strip(),
                        priority=task_priority,
                        frequency=frequency,
                        scheduled_date=task_date,
                    )
                )
                st.success(f"Added task for {selected_pet}: {task_title.strip()}")
            except ValueError as error:
                st.warning(str(error))

st.divider()
st.subheader("Today's Schedule")

schedule = st.session_state.scheduler.build_schedule(scheduled_for=date.today())
if schedule:
    st.table(
        [
            {
                "pet": pet.name,
                "task": task.description,
                "time": task.time,
                "priority": task.priority,
                "frequency": task.frequency,
                "completed": task.completed,
            }
            for pet, task in schedule
        ]
    )
else:
    st.info("No tasks scheduled for today.")

conflicts = st.session_state.scheduler.detect_conflicts(schedule)
if conflicts:
    for warning in conflicts:
        st.warning(warning)
else:
    st.success("No scheduling conflicts detected for today.")
