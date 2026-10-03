import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="College Timetable Generator",
    page_icon="📚",
    layout="wide"
)

st.title("📚 College Timetable Generator")
st.write("AI Based College Timetable Generator")

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

# Load subjects
subjects = pd.read_csv("subjects.csv")

# Remove unwanted spaces from column names
subjects.columns = subjects.columns.str.strip()

# Select class
selected_class = st.selectbox(
    "Select Class",
    ["II B.Sc AI&DS", "III B.Sc AI&DS"]
)

# Generate button
if st.button("Generate Timetable"):

    timetable = []

    # Create subject list using Hours
    subject_list = []

    for _, row in subjects.iterrows():

        hours = int(row["Hours"])

        for _ in range(hours):

            subject_list.append({
                "Subject": row["Subject"],
                "Faculty": row["Faculty"],
                "Type": row["Type"]
            })

    # Fill Monday to Friday
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

    # Display
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
