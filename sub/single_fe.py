import streamlit as st
from periodictable import formula

def main():
    st.title("Defect Formation Energy Diagram")

    # Input: Label for the diagram
    outfile_label = st.text_input("Enter a label for your diagram")

    # Input: Host chemical formula
    host_formula = st.text_input("Enter the host chemical formula (e.g., Mg2O)")
    if host_formula:
        parsed_host = formula(host_formula).atoms
        st.write("Host chemical formula parsed:")
        for element, count in parsed_host.items():
            st.write(f"Element: {element}, Count: {count}")

    # Input: Defect species (impurity and vacancy)
    st.subheader("Defect Species")
    impurity_defect = st.text_input("Enter the impurity defect species (e.g., Zn)")
    vacancy_defect = st.text_input("Enter the vacancy defect species (e.g., V_Mg)")

    # Input: Chemical potentials for species
    st.subheader("Chemical Potentials")
    species = []
    chemical_potentials = []
    units = []

    # Initial species input
    with st.form(key="chemical_potentials_form"):
        species_input = st.text_input("Enter species symbol (e.g., Zn):")
        chem_potential_input = st.number_input("Enter chemical potential:", format="%.6f")
        unit_input = st.selectbox("Choose unit:", ["eV", "Ry"], index=0)

        add_button = st.form_submit_button("Add Species")
        if add_button:
            if species_input:
                species.append(species_input)
                chemical_potentials.append(chem_potential_input)
                units.append(unit_input)
                st.experimental_rerun()  # To update the displayed fields

    # Display the list of species and chemical potentials
    if species:
        for i, sp in enumerate(species):
            st.write(f"Species: {sp}, Chemical Potential: {chemical_potentials[i]} {units[i]}")

    # Input: Host supercell energy
    host_energy = st.number_input("Enter the host supercell energy:", format="%.6f")

    # Input: Charged defect supercell energy (two inputs: charge and corresponding energy)
    st.subheader("Charged Defect Supercell Energy")
    defect_charge = st.number_input("Enter defect charge:", format="%.6f")
    defect_energy = st.number_input("Enter defect energy:", format="%.6f")

    # Choose an independent variable for the slider (Chemical potential of one species)
    st.subheader("Choose independent variable for slider:")
    if species:
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
