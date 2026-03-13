import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(page_title="Student Performance Dashboard", page_icon="📊", layout="wide")

st.title("📊 Student Performance Dashboard")
st.markdown("Analyze student marks, grades, and performance easily.")

# Load dataset
df = pd.read_csv("students.csv")

subjects = ["Math", "Science", "English", "History", "Computer"]

# Calculate total and average
df["Total"] = df[subjects].sum(axis=1)
df["Average"] = df["Total"] / len(subjects)

# Grade system
def calculate_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 50:
        return "D"
    else:
        return "F"

df["Grade"] = df["Average"].apply(calculate_grade)

# Layout columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Student Data")
    st.dataframe(df)

with col2:
    st.subheader("🏆 Class Topper")
    topper = df.loc[df["Total"].idxmax()]
    st.success(f"{topper['Name']} is the topper with {topper['Total']} marks")

# Bar chart for total marks
st.subheader("📈 Total Marks Comparison")

fig = px.bar(
    df,
    x="Name",
    y="Total",
    color="Name",
    text="Total",
    title="Student Total Marks"
)

st.plotly_chart(fig, use_container_width=True)

# Grade distribution
st.subheader("🎯 Grade Distribution")

fig2 = px.pie(
    df,
    names="Grade",
    title="Grade Distribution",
)

st.plotly_chart(fig2, use_container_width=True)

# Subject topper
st.subheader("📚 Subject Toppers")

for subject in subjects:
    top_student = df.loc[df[subject].idxmax()]
    st.write(f"**{subject}** → {top_student['Name']} ({top_student[subject]})")

# Student search
st.subheader("🔍 Search Student")

name = st.text_input("Enter student name")

if name:
    student = df[df["Name"].str.lower() == name.lower()]
    
    if not student.empty:
        st.success("Student Found")
        st.dataframe(student)
    else:
        st.error("Student not found")