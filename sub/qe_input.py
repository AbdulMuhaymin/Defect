import streamlit as st

def main():
    st.title("Quantum ESPRESSO Defect Input Generator")
    st.header("Coming soon...")

    defect_type = st.selectbox(label="Type of defect", options=["Cation-substitutional single impurity dopant", "Impurity dopant pair", "Impurity-vacancy complex (NN)", "Impurity-vacancy complex (NNN)"])

    host = st.selectbox("Host material", options=["ZnS", "MgO", "Others"])

    if host == "Others":
        struct_file_type = st.selectbox(label="Choose the structure file format", options=[".xyz", "POSCAR", ".CIF", "Quantum ESPRESSO input", "SIESTA input"])
        host = st.file_uploader("Upload the structure file")

    if "dopant" in defect_type:
        impurity_defect = st.text_input("Enter the impurity defect species (e.g., Cu)", value="Cu")
    elif "complex" in defect_type:
        impurity_defect = st.text_input("Enter the impurity defect species (e.g., Cu)", value="Cu")
        vacancy_defect = st.text_input("Enter the vacancy defect species (e.g., S)", value="S")

    # Create charge range input fields
    col_min, col_max = st.columns(2)
    with col_min:
        min_charge = st.text_input("Min charge:", value="-1", placeholder="Enter min charge")
    with col_max:
        max_charge = st.text_input("Max charge:", value="1", placeholder="Enter max charge")

    # Ensure min_charge and max_charge are valid integers
    if min_charge.isdigit() or (min_charge.startswith("-") and min_charge[1:].isdigit()):
        min_charge = int(min_charge)
    else:
        st.error("Please enter a valid integer for Min charge")

    if max_charge.isdigit() or (max_charge.startswith("-") and max_charge[1:].isdigit()):
        max_charge = int(max_charge)
    else:
        st.error("Please enter a valid integer for Max charge")

    input_file = "Coming soon"
    ofname = impurity_defect + "_in_" + host + ".in"
    st.download_button('Download the input file', input_file, ofname)