import streamlit as st

import sub.single_fe as fe
import sub.multiple_fe as mfe
import sub.siesta_input as siesta_in
import sub.qe_input as qe_in
import sub.analysis as analysis

def main():
    st.set_page_config(page_title="Isolated Defect Utility", page_icon="💎")        
    st.title("💎 Isolated Defect Utility")

    options = [
        ("Plot defect formation energy (FE) diagram for a single defect", "fe"),
        ("Plot defect FE diagram for multiple defects ", "mfe"),
        ("Generate an input file for defect calculation in Quantum ESPRESSO ", "qe_in"),
        ("Generate an input file for defect calculation in SIESTA", "siesta_in"),
        ("Analyze your defect calculation results", "analysis")
    ]

    st.markdown(
    """
    <style>
    /* Set the base font size for the entire app */
    html, body, [class*="css"]  {
        font-size: 18px; /* Adjust this value as needed */
    }
    </style>
    """,
    unsafe_allow_html=True
)

    page = st.radio("Choose a task:", options=[opt[0] for opt in options])
    page = next(opt[1] for opt in options if opt[0] == page)

    if page == "fe":
        fe.main()
    elif page == "mfe":
        mfe.main()
    elif page == "qe_in":
        qe_in.main()
    elif page == "siesta_in":
        siesta_in.main()
    elif page == "analysis":
        analysis.main()


if __name__ == "__main__":
    main()