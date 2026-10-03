# STEP 15: Machine Learning Model

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score

# Training Dataset

data = {
    "Faculty_Load": [
        10, 12, 15, 18, 20,
        8, 14, 17, 22, 25, 
        11, 13, 16, 19, 21,
        9, 12, 18, 23, 24
    ],

    "Room_Usage": [
        50, 60, 70, 80, 90,
        40, 65, 75, 95, 98,
        55, 62, 72, 85, 92,
        45, 58, 78, 96, 99
    ],

    "Conflicts": [
        0, 0, 0, 1, 2,
        0, 0, 1, 3, 5,
        0, 0, 0, 1, 3,
        0, 0, 1, 4, 5
    ],

    "Quality": [
        1, 1, 1, 0, 0,
        1, 1, 0, 0, 0,
        1, 1, 1, 0, 0,
        1, 1, 0, 0, 0
    ]
}

df = pd.DataFrame(data)

print("\n--- TRAINING DATASET ---")

print(df)

# Input and Output

X = df[[
    "Faculty_Load",
    "Room_Usage",
    "Conflicts"
]]

y = df["Quality"]

# Split Dataset

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

# Create ML Model

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train Model

model.fit(X_train, y_train)
joblib.dump(model, "timetable_model.pkl")

# Prediction

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\n--- MODEL ACCURACY ---")

print("Accuracy:", accuracy)

# New Timetable Prediction

new_timetable = pd.DataFrame({
    "Faculty_Load": [12],
    "Room_Usage": [65],
    "Conflicts": [0]
})

prediction = model.predict(new_timetable)

print("\n--- TIMETABLE QUALITY PREDICTION ---")

if prediction[0] == 1:

    print("Good Quality Timetable")

else:

    print("Timetable Needs Improvement")