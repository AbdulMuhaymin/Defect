import streamlit as st

# Session state to manage login status
if "is_authenticated" not in st.session_state:
    st.session_state.is_authenticated = False

# Login logic
def show_login_page():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Log in"):
        if username.lower() == "srg" and password.lower() == "mgo":
            st.session_state.is_authenticated = True
            st.rerun()
        else:
            st.error("Incorrect username or password")

# Logout logic
def show_logout_page():
    if st.button("Log out"):
        st.session_state.is_authenticated = False
        st.rerun()

# Define pages
login_page = st.Page(show_login_page, title="Log in", icon=":material/login:")
logout_page = st.Page(show_logout_page, title="Log out", icon=":material/logout:")

dashboard_page = st.Page(
    "Utilities/dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True
)
formation_energy_page = st.Page("Utilities/dfe.py", title="Formation Energy", icon=":material/bug_report:")
defect_viewer_page = st.Page("Utilities/defects.py", title="Defects", icon=":material/notification_important:")
dos_plotter_page = st.Page("Utilities/dos.py", title="Plot DOS", icon=":material/browse_activity:")
magnetic_moments_page = st.Page("Utilities/magmom.py", title="Magnetic Moments", icon=":material/explore:")

# Page navigation logic
if st.session_state.is_authenticated:
    current_page = st.navigation(
        {
            "Account": [logout_page],
            "Utilities": [
                dashboard_page,
                formation_energy_page,
                defect_viewer_page,
                dos_plotter_page,
                magnetic_moments_page,
            ],
        }
    )
else:
    current_page = st.navigation([login_page])

current_page.run()
