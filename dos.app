import streamlit as st
import pandas as pd
import plotly.express as px

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
    window_size = st.slider("Moving Average Window", min_value=1, max_value=20, value=1, step=1)

    # Button to plot DOS
    plot_button = st.button("Plot DOS")

# Output area
with col2:
    st.header("Output")

    # Check if file is uploaded and button clicked
    if uploaded_file is not None and plot_button:
        # Assume uploaded file is two-column data: energy and dos
        dos_df = pd.read_csv(uploaded_file, sep='\\s+', header=None, names=['Energy', 'DOS'])

        # Apply moving average
        dos_df['Smoothed DOS'] = dos_df['DOS'].rolling(window=window_size, center=True).mean()

        # Plot using plotly
        fig = px.line(dos_df, x='Energy', y='Smoothed DOS',
                      title='Density of States (DOS)',
                      labels={'Energy': 'Energy (eV)', 'Smoothed DOS': 'DOS (states/eV)'})

        # Display interactive plot
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please upload a DOS file and click 'Plot DOS' to visualize results.")
