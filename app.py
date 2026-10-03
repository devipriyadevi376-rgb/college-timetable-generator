import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="College Timetable Generator",
    page_icon="📚",
    layout="wide"
)

st.title("📚 College Timetable Generator")
st.write("Enter subject details and generate your college timetable.")

# Days
days = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday"
]

# Time slots
slots = [
    "9:00-10:00",
    "10:00-11:00",
    "11:15-12:15",
    "12:15-1:15",
    "2:00-3:00",
    "3:00-4:00"
]

# Class input
selected_class = st.selectbox(
    "Select Class",
    [
        "II B.Sc AI&DS",
        "III B.Sc AI&DS"
    ]
)

# Number of subjects
num_subjects = st.number_input(
    "Number of Subjects",
    min_value=1,
    max_value=15,
    value=6,
    step=1
)

st.subheader("Enter Subject Details")

subject_data = []

for i in range(int(num_subjects)):

    st.markdown(f"### Subject {i + 1}")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        subject_name = st.text_input(
            "Subject Name",
            key=f"subject_{i}"
        )

    with col2:
        faculty_name = st.text_input(
            "Faculty",
            key=f"faculty_{i}"
        )

    with col3:
        hours = st.number_input(
            "Hours",
            min_value=1,
            max_value=10,
            value=3,
            key=f"hours_{i}"
        )

    with col4:
        subject_type = st.selectbox(
            "Type",
            ["Theory", "Lab"],
            key=f"type_{i}"
        )

    subject_data.append({
        "Subject": subject_name,
        "Faculty": faculty_name,
        "Hours": hours,
        "Type": subject_type
    })


if st.button("Generate Timetable"):

    # Check empty inputs
    valid_data = True

    for item in subject_data:

        if item["Subject"].strip() == "":
            valid_data = False

        if item["Faculty"].strip() == "":
            valid_data = False

    if not valid_data:

        st.error("Please enter Subject Name and Faculty for all subjects.")

    else:

        timetable = []

        # Create subject periods
        subject_list = []

        for item in subject_data:

            for _ in range(int(item["Hours"])):

                subject_list.append({
                    "Subject": item["Subject"],
                    "Faculty": item["Faculty"],
                    "Type": item["Type"]
                })

        # Generate timetable
        index = 0

        for day in days:

            for slot in slots:

                if index < len(subject_list):

                    item = subject_list[index]

                    timetable.append({
                        "Class": selected_class,
                        "Day": day,
                        "Time": slot,
                        "Subject": item["Subject"],
                        "Faculty": item["Faculty"],
                        "Type": item["Type"]
                    })

                    index += 1

                else:

                    timetable.append({
                        "Class": selected_class,
                        "Day": day,
                        "Time": slot,
                        "Subject": "Free Period",
                        "Faculty": "-",
                        "Type": "-"
                    })

        # Convert to DataFrame
        timetable_df = pd.DataFrame(timetable)

        st.subheader("Generated College Timetable")

        st.dataframe(
            timetable_df,
            use_container_width=True,
            hide_index=True
        )

        # Download
        csv = timetable_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Timetable CSV",
            csv,
            "college_timetable.csv",
            "text/csv"
        )
