import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json

# ------------------------
# Minimal MoodTracker Class
# ------------------------
class MoodTracker:
    def __init__(self):
        self.data = {}

    def add_mood_entry(self, name, mood, notes=""):
        if name not in self.data:
            self.data[name] = {}
        today = str(datetime.today().date())
        self.data[name][today] = {"mood": mood, "notes": notes}
        return True

    def get_all_students(self):
        return list(self.data.keys())

    def get_student_data(self, name):
        return self.data.get(name, {})

    def get_all_data(self):
        return self.data


# ------------------------
# Minimal AdviceEngine Class
# ------------------------
class AdviceEngine:
    def get_advice(self, mood):
        advice_dict = {
            "stressed": "📚 Take a short break, revise with flashcards.",
            "tired": "💤 Rest for 20-30 minutes, hydrate well.",
            "happy": "🎉 Use your positive energy to tackle tough tasks!",
            "anxious": "🧘 Try deep breathing and make a small to-do list.",
            "excited": "⚡ Channel excitement into sports or study.",
            "calm": "😌 Stay consistent, maybe meditate.",
            "overwhelmed": "📝 Break tasks into smaller chunks.",
            "motivated": "💪 Push forward on key goals!"
        }
        return advice_dict.get(mood, "🙂 Stay balanced and plan your day wisely.")


# ------------------------
# Initialize session state
# ------------------------
if 'mood_tracker' not in st.session_state:
    st.session_state.mood_tracker = MoodTracker()
if 'advice_engine' not in st.session_state:
    st.session_state.advice_engine = AdviceEngine()

# ------------------------
# Streamlit Page Config
# ------------------------
st.set_page_config(
    page_title="Student Mood Tracker",
    page_icon="😊",
    layout="wide"
)


def main():
    st.title("😊 Student Mood Tracker AI")
    st.markdown("*Track your daily mood and get personalized advice for better student wellness*")

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Track Mood", "View History", "Analytics", "About"]
    )

    if page == "Track Mood":
        show_mood_tracking()
    elif page == "View History":
        show_mood_history()
    elif page == "Analytics":
        show_analytics()
    elif page == "About":
        show_about()


def show_mood_tracking():
    st.header("📝 Track Your Daily Mood")

    with st.form("mood_form"):
        st.subheader("Tell us how you're feeling today")

        name = st.text_input("Your Name:", placeholder="Enter your name")

        mood_options = {
            "happy": "😊 Happy",
            "stressed": "😰 Stressed",
            "tired": "😴 Tired",
            "excited": "🤩 Excited",
            "anxious": "😟 Anxious",
            "calm": "😌 Calm",
            "overwhelmed": "😵 Overwhelmed",
            "motivated": "💪 Motivated"
        }

        selected_mood = st.selectbox(
            "How are you feeling today?",
            options=list(mood_options.keys()),
            format_func=lambda x: mood_options[x]
        )

        notes = st.text_area("Any additional notes? (optional)")

        submitted = st.form_submit_button("Track My Mood", type="primary")

        if submitted:
            if name.strip():
                success = st.session_state.mood_tracker.add_mood_entry(
                    name.strip(), selected_mood, notes.strip()
                )
                if success:
                    st.success(f"✅ Mood tracked successfully for {name}!")

                    advice = st.session_state.advice_engine.get_advice(selected_mood)
                    st.subheader("💡 Personalized Advice")
                    st.info(advice)
                    st.balloons()
            else:
                st.error("⚠️ Please enter your name to continue.")


def show_mood_history():
    st.header("📊 Your Mood History")
    students = st.session_state.mood_tracker.get_all_students()

    if not students:
        st.info("📝 No mood data yet. Start by tracking your mood!")
        return

    selected_student = st.selectbox("Select Student:", students)

    if selected_student:
        student_data = st.session_state.mood_tracker.get_student_data(selected_student)

        if student_data:
            df_data = []
            for date, entry in student_data.items():
                mood = entry.get("mood")
                notes = entry.get("notes", "")
                df_data.append({"Date": date, "Mood": mood, "Notes": notes})

            df = pd.DataFrame(df_data)
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date', ascending=False)

            st.subheader(f"Recent Mood Entries for {selected_student}")
            for _, row in df.head(10).iterrows():
                mood_emoji = get_mood_emoji(row['Mood'])
                st.write(f"**{row['Date'].strftime('%Y-%m-%d')}** {mood_emoji} {row['Mood'].title()} — {row['Notes'] or '*No notes*'}")
                st.divider()

            if len(df) > 1:
                st.subheader("📈 Mood Trend Over Time")
                mood_mapping = {
                    'happy': 5, 'excited': 5, 'motivated': 4, 'calm': 4,
                    'tired': 2, 'stressed': 1, 'anxious': 1, 'overwhelmed': 1
                }
                df['MoodScore'] = df['Mood'].map(mood_mapping)
                fig = px.line(df.sort_values('Date'), x='Date', y='MoodScore', markers=True)
                st.plotly_chart(fig, use_container_width=True)


def show_analytics():
    st.header("📊 Mood Analytics")
    students = st.session_state.mood_tracker.get_all_students()

    if not students:
        st.info("📝 No mood data yet for analytics.")
        return

    all_data = st.session_state.mood_tracker.get_all_data()
    total_entries = sum(len(student_data) for student_data in all_data.values())

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", len(students))
    col2.metric("Total Entries", total_entries)
    col3.metric("Avg Entries/Student", f"{total_entries/len(students):.1f}")

    selected_student = st.selectbox("Select Student for Details:", students)
    if selected_student:
        student_data = st.session_state.mood_tracker.get_student_data(selected_student)
        moods = [entry["mood"] for entry in student_data.values()]

        if moods:
            st.subheader(f"Mood Distribution for {selected_student}")
            mood_counts = pd.Series(moods).value_counts()
            fig_pie = px.pie(values=mood_counts.values, names=mood_counts.index)
            st.plotly_chart(fig_pie, use_container_width=True)


def show_about():
    st.header("ℹ️ About Student Mood Tracker")
    st.markdown("This app helps students log moods, see trends, and get advice.")


def get_mood_emoji(mood):
    mood_emojis = {
        "happy": "😊", "stressed": "😰", "tired": "😴",
        "excited": "🤩", "anxious": "😟", "calm": "😌",
        "overwhelmed": "😵", "motivated": "💪"
    }
    return mood_emojis.get(mood.lower(), "😐")


if __name__ == "__main__":
    main()