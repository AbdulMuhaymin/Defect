import streamlit as st
from periodictable import formula

def main():
    st.title("Defect Formation Energy Diagram")

    st.subheader("User input:")
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
        energy_unit = st.selectbox("Unit:", ["Ry", "eV"], index=0)
    # Convert to float and append if valid
    if host_energy_input:
        try:
            host_energy = float(host_energy_input)
        except ValueError:
            st.warning("Invalid value for host supercell energy. Please enter a valid number.")

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

    if isinstance(min_charge, int) and isinstance(max_charge, int):
        # Validate that min_charge is less than or equal to max_charge
        if min_charge <= max_charge:
            # Create a dictionary to store energy values and units for each charge
            charge_energy_data = {}
            for charge in range(min_charge, max_charge + 1):
                col_energy, col_unit = st.columns([3, 1])  # Adjust column proportions if needed
                with col_energy:
                    energy = st.text_input(
                        f"Energy for charge {charge}:",
                        key=f"energy_{charge}",
                        placeholder="Enter energy value"
                    )
                with col_unit:
                    unit = st.selectbox(
                        f"Unit for charge {charge}:",
                        ["Ry", "eV"],
                        key=f"unit_{charge}"
                    )

                # Store the input data in the dictionary
                charge_energy_data[charge] = {"energy": energy, "unit": unit}

            # Display the collected data (optional for debugging)
            #st.write("Collected charge-energy data:", charge_energy_data)
        else:
            st.error("Min charge must be less than or equal to Max charge")

    # Create band gap and vbm input fields
    col_min, col_max = st.columns(2)
    with col_min:
        min_charge = st.text_input("Band gap (eV):", value="3.00", placeholder="Band gap of the host material in eV")
    with col_max:
        max_charge = st.text_input("Host VBM (eV)", value="2.4", placeholder="Valence Band Maximum of the pristine host in eV")


    # Choose an independent variable for the slider (Chemical potential of one species)
    st.subheader("Thermodynamic stability analysis:")
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
    st.subheader("Formation energy diagram:")
    if host_energy and defect_energy:
        # Here, you can compute the defect formation energy based on the inputs.
        defect_formation_energy = defect_energy - host_energy  # Example formula

        st.write(f"Defect Formation Energy: {defect_formation_energy} eV")

        # Here you can plot the defect formation energy, and make it interactive as a function of the chemical potential.
        # Example plot (you can integrate a more complex plot using Matplotlib or Plotly):
        st.line_chart([defect_formation_energy for _ in range(10)])

if __name__ == "__main__":
    main()
