import streamlit as st
from periodictable import formula
import matplotlib.pyplot as plt
import numpy as np

def main():
    st.title("Defect Formation Energy Diagram")

    st.subheader("User input:")
    # Input: Label for the diagram
    outfile_label = st.text_input("Enter a label for your diagram", value="Defect Formation Energy diagram")

    # Input: Host chemical formula
    host_species = []
    host_formula = st.text_input("Enter the host chemical formula (e.g., ZnS)", value="ZnS")
    if host_formula:
        parsed_host = formula(host_formula).atoms
        #st.write("Host chemical formula parsed:")
        for element, count in parsed_host.items():
            #st.write(f"Element: {element}, Count: {count}")
            host_species.append(str(element))

    # Input: Defect species (impurity and vacancy)
    #st.subheader("Defect Species")
    impurity_defect = st.text_input("Enter the impurity defect species (e.g., Cu), leave empty if none", value="Cu")
    vacancy_defect = st.text_input("Enter the vacancy defect species (e.g., S), leave empty if none", value="S")

    species = host_species.copy()
 # List of species: Combine host and defect species
    if str(impurity_defect) and str(impurity_defect) not in species:
        species.append(impurity_defect)
    if str(vacancy_defect) and str(vacancy_defect) not in species:
        species.append(str(vacancy_defect))

    # Automatically generate chemical potential input fields based on the species list
    chemical_potentials = {}
    units = {}

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
                chemical_potentials[str(sp)] = float(chem_potential_input)
                units[str(sp)] = unit_input
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
                col_energy, col_unit = st.columns([3, 1])  
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
    col_min, col_max, atom_num = st.columns(3)
    with col_min:
        min_charge = st.text_input("Band gap (eV):", value="3.00", placeholder="Band gap of the host material in eV")
    with col_max:
        max_charge = st.text_input("Host VBM (eV)", value="2.4", placeholder="Valence Band Maximum of the pristine host in eV")
    with atom_num:
        atom_number = st.text_input("# of atoms", value="64", placeholder="Number of atoms in the host supercell")

    # Thermodynamic stability analysis
    st.subheader("Thermodynamic Stability Analysis")
    Delta_H_f = (
        host_energy * 13.6057039763 / (int(atom_number) / len(host_species))
        - chemical_potentials[species[0]]
        - chemical_potentials[species[1]] )
    st.write(f"The heat of formation is: **{Delta_H_f:.4f}** eV.")

    # Calculate formation energy for the range of chemical potentials
    def dfe_q0(mu):
        dfe = (float(charge_energy_data[0]["energy"]) * 13.6057039763
        - host_energy * 13.6057039763
        - (-1*chemical_potentials[vacancy_defect] - mu)
        - chemical_potentials[impurity_defect] )
        return dfe

    mu_v_range = np.linspace(Delta_H_f, 0, 100)
    E_formation = dfe_q0(mu_v_range)

    # Plot the graph
    fig, ax = plt.subplots()
    ax.plot(mu_v_range, E_formation, color="red", label = None)
    ax.set_xlabel(f"$\\Delta \,\\mu_{{{vacancy_defect}}} = \\mu_{{{vacancy_defect}}} - \\mu_{{{vacancy_defect}}}^{{0}} $ (eV)", fontsize = 15)
    ax.set_xlim(Delta_H_f,0)
    ax.set_ylabel(f"$E_f$ (eV)", fontsize = 14)
    ax.set_title("Thermodynamic Stability Analysis", fontsize = 14)
    ax.grid(False)

        # Add vertical text on the left y-axis (inside the image)
    ax.text(
        x=Delta_H_f + 0.1,  
        y=(max(E_formation) + min(E_formation)) / 2, 
        s=f"Zn-poor or S-rich environment",  
        rotation=90,  
        va="center",  
        ha="center", 
        fontsize=12,
        color="black",
        bbox=dict(facecolor="r", edgecolor="none", alpha=0.3)
    )
    ax.text(
        x= 0 - 0.1,  
        y=(max(E_formation) + min(E_formation)) / 2, 
        s=f"Zn-rich or S-poor environment",  
        rotation=90,  
        va="center",  
        ha="center", 
        fontsize=12,
        color="black",
        bbox=dict(facecolor="g", edgecolor="none", alpha=0.3)
    )
    # Display the plot
    st.pyplot(fig)


    def dfe_q(mu, charge):
        dfe = (float(charge_energy_data[charge]["energy"]) * 13.6057039763
            - host_energy * 13.6057039763
            + (chemical_potentials[vacancy_defect] - mu)
            - chemical_potentials[impurity_defect])
        return dfe

    # Create slider for chemical potential of Zn
    mu_slider = st.slider(
        label="Delta chemical potential of Zn",
        min_value=Delta_H_f,
        max_value=0.0,
        value=Delta_H_f,
        step=0.01,
    )

    # List of charges to plot (you can modify this based on the charges you want to calculate)
    charges = [0, 1, -1, 2, -2]

    # Calculate formation energies for each charge and plot them
    mu_v_range = np.linspace(Delta_H_f, 0, 100)
    fig, ax = plt.subplots()

    for charge in charges:
        E_formation = [dfe_q(mu, charge) for mu in mu_v_range]
        ax.plot(mu_v_range, E_formation, label=f"Charge {charge}")

    # Customize plot
    ax.set_xlabel(f"$\\Delta \,\\mu_{{{vacancy_defect}}}$ (eV)", fontsize=15)
    ax.set_xlim(Delta_H_f, 0)
    ax.set_ylabel(f"$E_f$ (eV)", fontsize=14)
    ax.set_title("Charged Defect Formation Energy Diagram", fontsize=14)
    ax.grid(True)

    # Display the plot with Streamlit
    st.pyplot(fig)













if __name__ == "__main__":
    main()
