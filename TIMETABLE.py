import pandas as pd

# Read dataset files
subjects = pd.read_csv("dataset/subjects.csv")
teachers = pd.read_csv("dataset/teachers.csv")
rooms = pd.read_csv("dataset/rooms.csv")
classes = pd.read_csv("dataset/classes.csv")

# Display the data
print("\n--- SUBJECTS ---")
print(subjects)

print("\n--- TEACHERS ---")
print(teachers)

print("\n--- ROOMS ---")
print(rooms)

print("\n--- CLASSES ---")
print(classes)
# Define working days

days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]

# Define college time slots

time_slots = [
    "9:00-10:00",
    "10:00-11:00",
    "11:15-12:15",
    "12:15-1:15",
    "2:00-3:00",
    "3:00-4:00"
]

print("\n--- WORKING DAYS ---")
print(days)

print("\n--- TIME SLOTS ---")
print(time_slots)

print("\nTotal Working Days:", len(days))
print("Total Periods Per Day:", len(time_slots))
print("Total Weekly Periods:", len(days) * len(time_slots))
# STEP 12: Conflict-Free Timetable Generation

import random

timetable = []

subject_list = subjects["Subject"].tolist()

faculty_schedule = {}

for day in days:

    for time in time_slots:

        available_subjects = []

        for subject in subject_list:

            faculty = subjects[
                subjects["Subject"] == subject
            ]["Faculty"].iloc[0]

            key = (day, time, faculty)

            if key not in faculty_schedule:

                available_subjects.append(subject)

        if available_subjects:

            subject = random.choice(available_subjects)

            faculty = subjects[
                subjects["Subject"] == subject
            ]["Faculty"].iloc[0]

            faculty_schedule[(day, time, faculty)] = True

            timetable.append({
                "Day": day,
                "Time": time,
                "Subject": subject,
                "Faculty": faculty
            })

        else:

            timetable.append({
                "Day": day,
                "Time": time,
                "Subject": "Free Period",
                "Faculty": "-"
            })

timetable_df = pd.DataFrame(timetable)

print("\n--- CONFLICT-FREE TIMETABLE ---")

print(timetable_df)
# STEP 11: Faculty Conflict Detection

print("\n--- FACULTY CONFLICT CHECK ---")

conflicts = []

for i in range(len(timetable_df)):

    for j in range(i + 1, len(timetable_df)):

        if (
            timetable_df.iloc[i]["Day"] == timetable_df.iloc[j]["Day"]
            and timetable_df.iloc[i]["Time"] == timetable_df.iloc[j]["Time"]
            and timetable_df.iloc[i]["Faculty"] == timetable_df.iloc[j]["Faculty"]
        ):

            conflicts.append({
                "Day": timetable_df.iloc[i]["Day"],
                "Time": timetable_df.iloc[i]["Time"],
                "Faculty": timetable_df.iloc[i]["Faculty"],
                "Subject 1": timetable_df.iloc[i]["Subject"],
                "Subject 2": timetable_df.iloc[j]["Subject"]
            })

if len(conflicts) == 0:

    print("No Faculty Conflicts Found!")

else:

    print("Faculty Conflicts Found!")

    conflict_df = pd.DataFrame(conflicts)

    print(conflict_df)

print("\nTotal Faculty Conflicts:", len(conflicts))
# STEP 13: Display Timetable in Table Format

print("\n--- COLLEGE WEEKLY TIMETABLE ---")

weekly_timetable = timetable_df.pivot(
    index="Day",
    columns="Time",
    values="Subject"
)

weekly_timetable = weekly_timetable.reindex(days)

print(weekly_timetable)
# STEP 14: Export Timetable to CSV

weekly_timetable.to_csv("generated_timetable.csv")

print("\nTimetable saved successfully!")

print("File Name: generated_timetable.csv")