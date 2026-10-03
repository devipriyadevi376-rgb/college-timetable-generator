import streamlit as st
import pandas as pd
import random
import joblib

st.set_page_config(
    page_title="College Timetable Generator",
    page_icon="📅",
    layout="wide"
)

st.title("🎓 AI-Based College Timetable Generator")

st.write("Generate a weekly college timetable automatically.")

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

slots = [
    "9:00-10:00",
    "10:00-11:00",
    "11:15-12:15",
    "12:15-1:15",
    "2:00-3:00",
    "3:00-4:00"
]

subjects = pd.read_csv("subjects.csv")

selected_class = st.selectbox(
    "Select Class",
    ["II B.Sc AI&DS", "III B.Sc AI&DS"]
)
if st.button("Generate Timetable"):

    timetable = []

    # Subjects-ஐ weekly hours அடிப்படையில் repeat செய்கிறோம்
    subject_list = []

    for _, row in subjects.iterrows():
        for _ in range(int(row["Hours"])):
            subject_list.append(row["Subject"])

    # Monday to Friday + all time slots
    index = 0

    for day in days:
        for slot in slots:

            if index < len(subject_list):
                subject_name = subject_list[index]

                teacher_name = subjects.loc[
                    subjects["Subject"] == subject_name,
                    "Teacher"
                ].iloc[0]

                timetable.append({
                    "Class": selected_class,
                    "Day": day,
                    "Time": slot,
                    "Subject": subject_name,
                    "Teacher": teacher_name
                })

                index += 1

    # Display timetable
    if timetable:
        timetable_df = pd.DataFrame(timetable)

        st.subheader("Generated College Timetable")

        st.dataframe(
            timetable_df,
            use_container_width=True
        )

    else:
        st.error("No timetable could be generated.")
if st.button("Generate Timetable"):

    timetable = []

    faculty_used = set()

    for day in days:
        for slot in slots:

            available = subjects[
                ~subjects["Faculty"].isin(
                    [
                        faculty for d, t, faculty in faculty_used
                        if d == day and t == slot
                    ]
                )
            ]

            if available.empty:
                subject = random.choice(subjects.to_dict("records"))
            else:
                subject = random.choice(
                    available.to_dict("records")
                )

            faculty_used.add(
                (day, slot, subject["Faculty"])
            )
            room_data = pd.read_csv("rooms.csv")

            if subject["Type"] == "Lab":
                available_rooms = room_data[
                    room_data["Type"] == "Lab"
                ]
            else:
                available_rooms = room_data[
                    room_data["Type"] == "Classroom"
                ]

            room = random.choice(
                available_rooms["Room"].tolist()
            )
            timetable = []
            timetable.append({
                "Day": day,
                "Time": slot,
                "Subject": subject["Subject"],
                "Faculty": subject["Faculty"],
                "Room": room,
                "Type": subject["Type"]
            })
df = pd.DataFrame(timetable)

st.subheader(f"Weekly Timetable - {selected_class}")

pivot = df.pivot(
    index="Time",
    columns="Day",
    values="Subject"
)

st.subheader("Weekly Timetable")

st.dataframe(
    pivot,
    use_container_width=True
)

st.subheader("Room Allocation Details")

st.dataframe(
    df[["Day", "Time", "Subject", "Faculty", "Room"]],
    use_container_width=True
)
st.subheader("Faculty Conflict Checking")
st.subheader("Room Conflict Checking")

room_conflicts = df[
    df.duplicated(
        subset=["Day", "Time", "Room"],
        keep=False
    )
]
st.subheader("Subject-wise Period Summary")

subject_summary = df["Subject"].value_counts().reset_index()

subject_summary.columns = ["Subject", "Total Periods"]

st.dataframe(
    subject_summary,
    use_container_width=True
)
st.subheader("ML-Based Timetable Quality Prediction")

import joblib

model = joblib.load("timetable_model.pkl")

faculty_conflicts = df[
    df.duplicated(
        subset=["Day", "Time", "Faculty"],
        keep=False
    )
]

room_conflicts = df[
    df.duplicated(
        subset=["Day", "Time", "Room"],
        keep=False
    )
]

faculty_conflict_count = len(faculty_conflicts)

room_conflict_count = len(room_conflicts)

total_conflicts = (
    faculty_conflict_count + room_conflict_count
)
room_conflict_count = len(room_conflicts)

total_conflicts = (
    faculty_conflict_count + room_conflict_count
)

faculty_load = df["Faculty"].value_counts().max()
room_usage = df["Room"].value_counts().max()

prediction = model.predict([[
    faculty_load,
    room_usage,
    total_conflicts
]])

st.write("Total Conflicts:", total_conflicts)

st.write("Predicted Timetable Quality:", prediction[0])

if room_conflicts.empty:
    st.success("No Room Conflicts Found!")
else:
    st.warning("Room Conflicts Detected!")
    st.dataframe(room_conflicts)

faculty_conflicts = df[
    df.duplicated(
        subset=["Day", "Time", "Faculty"],
        keep=False
    )
]

if faculty_conflicts.empty:
    st.success("No Faculty Conflicts Found!")
else:
    st.warning("Faculty Conflicts Detected!")
    st.dataframe(faculty_conflicts)

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
        label="Download Timetable CSV",
        data=csv,
        file_name="college_timetable.csv",
        mime="text/csv"
    )
