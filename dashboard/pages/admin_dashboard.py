import streamlit as st
import sqlite3
import pandas as pd
import os
import json
import numpy as np
import subprocess
import sys
import psutil


from PIL import Image
import plotly.express as px
from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh
import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

if "monitoring" not in st.session_state:
    st.session_state.monitoring = False

if (
    st.session_state.logged_in == False
    or
    st.session_state.role != "admin"
):

    st.error(
        "Please login first."
    )

    st.stop()
# --------------------------------

if (
    "start_ai" in st.session_state
    and
    st.session_state.start_ai
):

    subprocess.Popen(
        [
            sys.executable,
            "-m",
            "app.recognition.face_attendance"
        ]
    )

    st.session_state.start_ai = False

    st.session_state.monitoring = True

if st.session_state.role != "admin":

    st.error(
        "Access Denied"
    )

    st.stop()

st.set_page_config(
    page_title="AI Surveillance",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st_autorefresh(
    interval=5000,
    key="refresh"
)

# --------------------------------

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #111827
    );
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

h1,h2,h3 {
    color: cyan;
}

div[data-testid="stMetric"] {
    background:#1e293b;
    border-radius:20px;
    padding:20px;
    border:1px solid #334155;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------

try:

    with open(
        "data/system_status.json"
    ) as f:

        status = json.load(f)

except:

    status = {

        "people": 0,
        "recognized": [],
        "unknown": 0,
        "alerts": 0
    }

# --------------------------------

conn = sqlite3.connect(
    "database/surveillance.db",
    check_same_thread=False
)

attendance_df = pd.read_sql_query(
    "SELECT * FROM attendance",
    conn
)

try:

    alerts_df = pd.read_sql_query(
        "SELECT * FROM alerts",
        conn
    )

except:

    alerts_df = pd.DataFrame(
        columns=["event","timestamp"]
    )

image_folder = "evidence/images"

# --------------------------------

# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:

    selected = option_menu(

        "🛡️ AI Security",

        [
            "Dashboard",
            "Live Camera",
            "Attendance",
            "Alerts",
            "Evidence",
            "Analytics",
            "System"
        ],

        icons=[
            "house",
            "camera-video",
            "people",
            "shield-exclamation",
            "camera",
            "bar-chart",
            "cpu"
        ],

        menu_icon="shield-lock",
        default_index=0
    )

    st.divider()

    # --------------------
    # EMPLOYEE COUNT
    # --------------------

    conn = sqlite3.connect(
        "database/surveillance.db"
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM users
        WHERE role='employee'
        """
    )

    count = cursor.fetchone()[0]

    conn.close()

    st.metric(
        "👥 Employees",
        count
    )

    st.divider()

    st.info(
        f"👤 Admin: {st.session_state.username}"
    )

    st.divider()

    # --------------------
    # LOGOUT BUTTON
    # --------------------

if st.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.role = ""
    st.session_state.username = ""

    st.rerun()

# --------------------------------

st.title(
    "🛡️ AI SURVEILLANCE CONTROL CENTER"
)


# ---------------------------------
# HIDE STREAMLIT MENU
# ---------------------------------

st.markdown("""
<style>

[data-testid="stSidebarNav"]{
    display:none;
}

[data-testid="collapsedControl"]{
    display:none;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------

if selected == "Dashboard":

    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "People",
        status["people"]
    )

    c2.metric(
        "Recognized",
        len(status["recognized"])
    )

    c3.metric(
        "Unknown",
        status["unknown"]
    )

    c4.metric(
        "Alerts",
        status["alerts"]
    )

    st.divider()

    st.subheader(
        "Recognized People"
    )

    if status["recognized"]:

        for person in status["recognized"]:

            st.success(person)

# --------------------------------

elif selected == "Live Camera":

    st.subheader(
        "Live Camera Feed"
    )

    if os.path.exists(
        "data/live_frame.jpg"
    ):

        image = Image.open(
            "data/live_frame.jpg"
        )

        st.image(
            image,
            use_container_width=True
        )

# --------------------------------

elif selected == "Attendance":

    st.subheader(
        "Attendance"
    )

    st.dataframe(
    attendance_df[
        [
            "name",
            "date",
            "check_in",
            "check_out"
        ]
    ],
    use_container_width=True
)

# --------------------------------

elif selected == "Alerts":

    st.subheader(
        "Alerts"
    )

    st.dataframe(
        alerts_df,
        use_container_width=True
    )

# --------------------------------

elif selected == "Evidence":

    st.subheader(
        "Evidence Images"
    )

    if os.path.exists(
        image_folder
    ):

        images = sorted(
            os.listdir(image_folder),
            reverse=True
        )

        cols = st.columns(3)

        for i, img_name in enumerate(images):

            path = os.path.join(
                image_folder,
                img_name
            )

            image = Image.open(path)

            cols[i % 3].image(
                image,
                caption=img_name,
                use_container_width=True
            )

# --------------------------------

elif selected == "Analytics":


    st.subheader("📈 Analytics Dashboard")

    # --------------------
    # Attendance Count
    # --------------------

    if len(attendance_df):

        chart_data = (
            attendance_df["name"]
            .value_counts()
            .reset_index()
        )

        chart_data.columns = [
            "Employee",
            "Count"
        ]

        fig1 = px.bar(
            chart_data,
            x="Employee",
            y="Count",
            title="Attendance Count",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # --------------------
    # Attendance Percentage
    # --------------------

    total_employees = 30
    
    # Avoid division by zero if attendance_df is empty
    if len(attendance_df) > 0 and "name" in attendance_df.columns:
        attendance_percent = (
            len(
                attendance_df["name"].unique()
            ) / total_employees
        ) * 100
    else:
        attendance_percent = 0.0

    st.subheader(
        "Attendance Percentage"
    )

    st.progress(
        attendance_percent / 100
    )

    st.write(
        f"{attendance_percent:.1f}%"
    )

    # --------------------
    # Visitor Timeline & Trends (Only runs if data exists)
    # --------------------
    if len(attendance_df) > 0:
        
        # --- Dynamically find the correct time column ---
        time_col = None
        for col in ["time", "timestamp", "Timestamp", "Time"]:
            if col in attendance_df.columns:
                time_col = col
                break
        
        # Fallback to the first available column if standard names aren't found
        if not time_col:
            time_col = attendance_df.columns[0] 

        # Create 'hour' column safely
        attendance_df["hour"] = pd.to_datetime(
            attendance_df[time_col], errors="coerce"
        ).dt.hour
        
        # Fill NaN hours with 0 just in case conversion fails
        attendance_df["hour"] = attendance_df["hour"].fillna(0).astype(int)

        timeline = (
            attendance_df
            .groupby("hour")
            .size()
            .reset_index(name="Visitors")
        )

        fig2 = px.line(
            timeline,
            x="hour",
            y="Visitors",
            title="Visitor Timeline",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # --------------------
        # Attendance Trend
        # --------------------
        # Check if 'date' column exists, otherwise extract it from the time column
        if "date" not in attendance_df.columns:
            attendance_df["date"] = pd.to_datetime(attendance_df[time_col], errors="coerce").dt.date

        trend = (
            attendance_df
            .groupby("date")
            .size()
            .reset_index(name="Attendance")
        )

        fig3 = px.line(
            trend,
            x="date",
            y="Attendance",
            title="Attendance Trend",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )
        
        # --------------------
        # Activity Heatmap
        # --------------------
        fig5 = px.histogram(
            attendance_df,
            x="hour",
            nbins=24,
            title="Activity Heatmap",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig5,
            use_container_width=True
        )
    else:
        st.info("No attendance data available to display timeline charts.")

    # --------------------
    # Alert Distribution
    # --------------------

    if 'alerts_df' in locals() and len(alerts_df):

        alert_data = (
            alerts_df["event"]
            .value_counts()
            .reset_index()
        )

        alert_data.columns = [
            "Alert",
            "Count"
        ]

        fig4 = px.pie(
            alert_data,
            names="Alert",
            values="Count",
            hole=0.5,
            title="Alert Distribution",
            template="plotly_dark"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

# --------------------------------
elif selected == "Employees":

    conn = sqlite3.connect(
        "database/surveillance.db"
    )

    employees = pd.read_sql_query(
        """
        SELECT username
        FROM users
        WHERE role='employee'
        """,
        conn
    )

    st.subheader(
        "Registered Employees"
    )

    st.dataframe(
        employees,
        use_container_width=True
    )

    conn.close()
# --------------------------------


elif selected == "System":

    st.subheader(
        "⚙️ System Status"
    )

    st.success(
        "📷 Camera Online"
    )

    st.success(
        "🤖 AI System Ready"
    )

    st.success(
        "🗄️ Database Connected"
    )

    st.divider()

    st.subheader(
        "🎥 AI Monitoring Control"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "▶ Start Monitoring",
            use_container_width=True
        ):

            try:

                subprocess.Popen(
                    [
                        sys.executable,
                        "-m",
                        "app.recognition.face_attendance"
                    ]
                )

                st.session_state.monitoring = True

                st.success(
                    "AI Monitoring Started"
                )

            except Exception as e:

                st.error(
                    f"Error: {e}"
                )

    with col2:

        if st.button(
            "⏹ Stop Monitoring",
            use_container_width=True
        ):

            for process in psutil.process_iter():

                try:

                    cmd = " ".join(
                        process.cmdline()
                    )

                    if "face_attendance" in cmd:

                        process.kill()

                except:
                    pass

            st.session_state.monitoring = False

            st.success(
                "Monitoring Stopped"
            )

    st.divider()

    if st.session_state.monitoring:

        st.success(
            "🟢 AI Monitoring Running"
        )

    else:

        st.error(
            "🔴 AI Monitoring Stopped"
        )


st.markdown("---")

st.markdown(
    """
    <center>

    <h4 style='color:cyan'>
    AI Surveillance System
    </h4>

    Developed by Arav-Arnav

    </center>
    """,
    unsafe_allow_html=True
)

conn.close()