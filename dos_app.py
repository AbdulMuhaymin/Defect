import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Title of the app
st.title('DFT Results Analyzer')

# Divide the page into two columns
col1, col2 = st.columns([1, 2])

# Editor/Toolbar area
with col1:
    st.header("Editor/Toolbars")

    # File upload section
    uploaded_file = st.file_uploader("Upload DOS file", type=['csv', 'txt', 'dat'])

    # Slider for moving average window
    window_size = st.slider("Moving Average Window", min_value=1, max_value=100, value=10, step=1)
    xlim_values = st.slider('Select a range of values', value=(-100.0, 100.0))

    # Button to plot DOS
    plot_button = st.button("Plot DOS")

# Output area
with col2:
    st.header("Output")

    if uploaded_file is not None and plot_button:
        data = np.loadtxt(uploaded_file, skiprows=1)

        energy = data[:, 0]
        dos_up = data[:, 1]
        dos_down = data[:, 2]

        fermi_energy = 9.844  # replace this with dynamic value extraction if needed
        
        mov_avg_up = np.convolve(dos_up, np.ones(window_size)/window_size, mode='valid')
        mov_avg_down = -1 * np.convolve(dos_down, np.ones(window_size)/window_size, mode='valid')
        
        energy_adjusted = energy[int(window_size/2)-1:int(-1*window_size/2)] - fermi_energy

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=energy_adjusted, y=mov_avg_up, mode='lines', name='Up Spin', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=energy_adjusted, y=mov_avg_down, mode='lines', name='Down Spin', line=dict(color='red')))

        fig.update_layout(title="Density of States (DOS)",
                          xaxis_title="Energy (eV)",
                          yaxis_title="DOS (states/eV)",
                          range_x = xlim_values,
                          legend=dict(font=dict(size=12)))

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please upload a DOS file and click 'Plot DOS' to visualize results.")
