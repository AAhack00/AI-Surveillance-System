import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

if (
    st.session_state.logged_in == False
    or
    st.session_state.role != "employee"
):

    st.error(
        "Please login first."
    )

    st.stop()

st.set_page_config(
    page_title="Employee Dashboard",
    page_icon="👤",
    layout="wide"
)

# ------------------------
# LOGIN CHECK
# ------------------------


if st.session_state.role != "employee":

    st.error("Access Denied")

    st.stop()

# ------------------------
# CSS
# ------------------------

st.markdown("""
<style>

.stApp{
    background:
    linear-gradient(
        135deg,
        #0f172a,
        #111827
    );
}

div[data-testid="stMetric"]{
    background:#1e293b;
    padding:20px;
    border-radius:20px;
    transition:0.3s;
}

div[data-testid="stMetric"]:hover{
    transform:translateY(-8px);
    box-shadow:0 0 20px cyan;
}

h1,h2,h3{
    color:cyan;
}

</style>
""", unsafe_allow_html=True)

# ------------------------
# SIDEBAR
# ------------------------

with st.sidebar:

    st.title("👤 Employee")

    st.write(
        st.session_state.username
    )

if st.button("Logout"):

    st.session_state.logged_in = False
    st.session_state.role = ""
    st.session_state.username = ""

    st.rerun()

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

# ------------------------
# DATABASE
# ------------------------

conn = sqlite3.connect(
    "database/surveillance.db"
)

attendance_df = pd.read_sql_query(
    """
    SELECT *
    FROM attendance
    WHERE name=?
    """,
    conn,
    params=[
        st.session_state.username
    ]
)

# ------------------------
# HEADER
# ------------------------

st.title(
    "👤 EMPLOYEE DASHBOARD"
)

st.write(
    f"Welcome {st.session_state.username}"
)

# ------------------------
# METRICS
# ------------------------

col1,col2,col3 = st.columns(3)

with col1:

    st.metric(
        "Attendance Records",
        len(attendance_df)
    )

with col2:

    if len(attendance_df):

        st.metric(
            "Last Check In",
            attendance_df.iloc[-1]["check_in"]
        )

with col3:

    if len(attendance_df):

        st.metric(
            "Last Check Out",
            attendance_df.iloc[-1]["check_out"]
        )

st.divider()

# ------------------------
# ATTENDANCE TABLE
# ------------------------

st.subheader(
    "Attendance History"
)

st.dataframe(
    attendance_df,
    use_container_width=True
)

# ------------------------
# CHART
# ------------------------

if len(attendance_df):

    chart_data = (
        attendance_df["date"]
        .value_counts()
        .reset_index()
    )

    chart_data.columns = [
        "Date",
        "Attendance"
    ]

    fig = px.bar(
        chart_data,
        x="Date",
        y="Attendance",
        title="Attendance History",
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

conn.close()