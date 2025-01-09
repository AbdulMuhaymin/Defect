import streamlit as st
from periodictable import formula

def main():
    st.title("Defect Formation Energy Diagram")

    # Input: Label for the diagram
    outfile_label = st.text_input("Enter a label for your diagram", value="Defect Formation Energy diagram")

    # Input: Host chemical formula
    species = []
    host_formula = st.text_input("Enter the host chemical formula (e.g., ZnS)", value="ZnS")
    if host_formula:
        parsed_host = formula(host_formula).atoms
        #st.write("Host chemical formula parsed:")
        for element, count in parsed_host.items():
            #st.write(f"Element: {element}, Count: {count}")
            species.append(str(element))

    # Input: Defect species (impurity and vacancy)
    #st.subheader("Defect Species")
    impurity_defect = st.text_input("Enter the impurity defect species (e.g., Cu), leave empty if none", value="Cu")
    vacancy_defect = st.text_input("Enter the vacancy defect species (e.g., S), leave empty if none", value="S")

 # List of species: Combine host and defect species
    if str(impurity_defect) and str(impurity_defect) not in species:
        species.append(impurity_defect)
    if str(vacancy_defect) and str(vacancy_defect) not in species:
        species.append(str(vacancy_defect))

    # Automatically generate chemical potential input fields based on the species list
    chemical_potentials = []
    units = []

    for sp in species:
        # Create two columns for the value input and unit selector
        col1, col2 = st.columns([3, 1])  # Adjust the proportions as needed
        with col1:
            # Directly get the value from the text input
            chem_potential_input = st.text_input(f"Enter chemical potential for **{sp}**:", value="", placeholder="Enter value")
        with col2:
            # Directly get the unit selection
            unit_input = st.selectbox(f"Unit for **{sp}**:", ["eV", "Ry"], index=0)

        # Append the values directly as they are entered
        if chem_potential_input:  # Only append if the user has entered a value
            try:
                # Convert the input value to a float
                chemical_potentials.append(float(chem_potential_input))
                units.append(unit_input)
            except ValueError:
                st.warning(f"Invalid value for chemical potential of {sp}. Please enter a valid number.")

    # Host supercell energy input
    col1, col2 = st.columns([3, 1])  # Adjust the proportions as needed
    with col1:
        # Use text_input instead of number_input to avoid the increment arrows
        host_energy_input = st.text_input("Enter the host supercell energy:", value="", placeholder="Enter value")
    with col2:
        # Unit selector for energy (eV or Ry)
        energy_unit = st.selectbox("Unit:", ["eV", "Ry"], index=0)
    # Convert to float and append if valid
    if host_energy_input:
        try:
            host_energy = float(host_energy_input)
        except ValueError:
            st.warning("Invalid value for host supercell energy. Please enter a valid number.")

    # Charge range input
    col1, col2 = st.columns([3, 3])  # Adjust proportions as needed
    with col1:
        min_charge = st.text_input("Min charge:", value=-1)
    with col2:
        max_charge = st.text_input("Max charge:", value=1)



    # Choose an independent variable for the slider (Chemical potential of one species)
    st.subheader("Choose independent variable for slider:")
    if chemical_potentials:
        chosen_species = st.selectbox("Select species to vary chemical potential:", species)
        slider_min = min(chemical_potentials)
        slider_max = max(chemical_potentials)
        chemical_potential_slider = st.slider(
            f"Adjust chemical potential for {chosen_species}",
            min_value=float(slider_min),
            max_value=float(slider_max),
            value=float(chemical_potentials[species.index(chosen_species)]),
            step=0.01
        )

        st.write(f"Current adjusted chemical potential for {chosen_species}: {chemical_potential_slider} {units[species.index(chosen_species)]}")


    # Plot the defect formation energy
    st.subheader("Defect Formation Energy Diagram")
    if host_energy and defect_energy:
        # Here, you can compute the defect formation energy based on the inputs.
        defect_formation_energy = defect_energy - host_energy  # Example formula

        st.write(f"Defect Formation Energy: {defect_formation_energy} eV")

        # Here you can plot the defect formation energy, and make it interactive as a function of the chemical potential.
        # Example plot (you can integrate a more complex plot using Matplotlib or Plotly):
        st.line_chart([defect_formation_energy for _ in range(10)])

if __name__ == "__main__":
    main()
