import streamlit as st
import sqlite3
import os
import subprocess
from PIL import Image
import sys
import subprocess

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="AI Surveillance Login",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
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

# ---------------------------------
# SESSION
# ---------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "role" not in st.session_state:
    st.session_state.role = ""

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------------------------
# REDIRECT
# ---------------------------------

if st.session_state.logged_in:

    if st.session_state.role == "admin":

        st.switch_page(
            "pages/admin_dashboard.py"
        )

    else:

        st.switch_page(
            "pages/employee_dashboard.py"
        )

# ---------------------------------
# CUSTOM CSS
# ---------------------------------

st.markdown("""
<style>

.stApp{
    background:
    linear-gradient(
        135deg,
        #0f172a,
        #111827,
        #1e293b
    );
}

section[data-testid="stSidebar"]{
    background:
    linear-gradient(
        180deg,
        #111827,
        #0f172a
    );
}

.stTextInput > div > div > input{

    background-color:#1e293b;

    color:white;

    border:1px solid cyan;

    border-radius:10px;
}

.stButton button{

    width:100%;

    height:50px;

    border:none;

    border-radius:15px;

    font-size:18px;

    font-weight:bold;

    background:
    linear-gradient(
        45deg,
        cyan,
        blue
    );

    color:white;

    transition:0.3s;
}

.stButton button:hover{

    transform:translateY(-5px);

    box-shadow:0px 0px 25px cyan;
}

button[data-baseweb="tab"]{

    font-size:18px;

    color:white;
}

h1,h2,h3{

    color:cyan;

    text-shadow:0px 0px 15px cyan;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# SIDEBAR
# ---------------------------------

with st.sidebar:

    st.title("🛡 AI SECURITY")

    st.markdown("---")

    st.success("🟢 Face Recognition")

    st.success("🟢 Attendance System")

    st.success("🟢 AI Surveillance")

    st.success("🟢 Security Alerts")

    st.success("🟢 Dashboard Analytics")

    st.markdown("---")

    st.info(
        "Version 1.0"
    )

    st.caption(
        "Developed by Arav-Arnav"
    )

# ---------------------------------
# HEADER
# ---------------------------------

st.markdown("""
<h1 style='text-align:center'>
🛡 AI SURVEILLANCE SYSTEM
</h1>

<h4 style='text-align:center;color:lightgray'>
Smart Attendance • Face Recognition • Security Monitoring
</h4>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------
# TABS
# ---------------------------------

tab1, tab2 = st.tabs(
    [
        "🔐 Login",
        "👤 Register Employee"
    ]
)

# =================================
# LOGIN
# =================================

with tab1:

    st.subheader(
        "User Login"
    )

    username = st.text_input(
        "Username",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button(
        "Login"
    ):

        conn = sqlite3.connect(
            "database/surveillance.db"
        )

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT role
            FROM users
            WHERE username=?
            AND password=?
            """,
            (
                username,
                password
            )
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            st.session_state.logged_in = True

            st.session_state.role = user[0]

            st.session_state.username = username

            st.success(
                "Login Successful"
            )

            st.rerun()

        else:

            st.error(
                "Invalid Credentials"
            )


# =================================
# REGISTER
# =================================

with tab2:

    st.subheader(
        "Register New Employee"
    )

    poses = [
        "Look Straight",
        "Look Left",
        "Look Right",
        "Look Up",
        "Look Down",
        "Smile",
        "Turn Left",
        "Turn Right",
        "Move Near Camera",
        "Move Away"
    ]

    if "capture_count" not in st.session_state:
        st.session_state.capture_count = 0

    new_user = st.text_input(
        "Employee Name",
        key="register_name"
    )

    new_password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )

    if st.session_state.capture_count < 10:

        st.info(
            f"Step {st.session_state.capture_count+1}: "
            f"{poses[st.session_state.capture_count]}"
        )

        photo = st.camera_input(
            "Capture Face",
            key=f"cam_{st.session_state.capture_count}"
        )

        if st.button(
            "Save Photo"
        ):

            if photo:

                folder = f"faces/{new_user}"

                os.makedirs(
                    folder,
                    exist_ok=True
                )

                image = Image.open(photo)

                image.save(
                    f"{folder}/{st.session_state.capture_count}.jpg"
                )

                st.session_state.capture_count += 1

                st.rerun()

    st.progress(
        st.session_state.capture_count / 10
    )

    st.write(
        f"Captured: "
        f"{st.session_state.capture_count}/10"
    )

    if st.session_state.capture_count == 10:

        st.success(
            "10 Images Captured"
        )

        if st.button(
            "Register Employee"
        ):
            subprocess.run(
    [
        sys.executable,
        "app/recognition/register_faces.py"
    ]
)

            conn = sqlite3.connect(
                "database/surveillance.db"
            )

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE username=?
                """,
                (new_user,)
            )

            existing = cursor.fetchone()

            if existing:

                st.error(
                    "Employee already exists."
                )

            else:

                cursor.execute(
                    """
                    INSERT INTO users
                    (
                        username,
                        password,
                        role
                    )
                    VALUES (?, ?, ?)
                    """,
                    (
                        new_user,
                        new_password,
                        "employee"
                    )
                )

                conn.commit()

                conn.close()

                with st.spinner(
                    "Training Face Model..."
                ):

                    subprocess.run(
                        [
                            sys.executable,
                            "app/recognition/register_faces.py"
                        ]
                    )

                st.success(
                    "Employee Registered Successfully"
                )

                st.session_state.capture_count = 0
# ---------------------------------
# FOOTER
# ---------------------------------

st.markdown("---")

st.markdown("""
<center>

<h4 style='color:cyan'>
AI Surveillance System
</h4>

Developed by Arav-Arnav

</center>
""", unsafe_allow_html=True)