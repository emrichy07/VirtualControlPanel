# app.py

import streamlit as st
import pandas as pd
import numpy as np
import time
from machine import Machine  # Import our simulation class

# --- Page Configuration ---
st.set_page_config(
    page_title="Virtual Control Panel",
    page_icon="🤖",
    layout="wide"
)

# --- Initialize Session State ---
if 'machine' not in st.session_state:
    st.session_state.machine = Machine()
    print("Initialized Machine object in session state.")

if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=['time', 'temperature', 'voltage', 'speed'])

# --- Helper Functions ---
def get_status_indicator_html(state):
    """
    Generates a custom HTML/CSS block for a large, color-coded
    state indicator based on HMI best practices.
    """
    color_map = {
        Machine.STATE_ACTIVE: "#28a745",  # Green
        Machine.STATE_OVERHEATING: "#dc3545", # Red
        Machine.STATE_RECOVERY: "#ffc107",  # Yellow
        Machine.STATE_IDLE: "#6c757d"   # Grey
    }
    color = color_map.get(state, "#6c757d") # Default to Grey
    
    indicator_html = f"""
    <div style="
        border: 2px solid {color};
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        background-color: {color}22; /* Light tint */
    ">
        <h2 style="color: {color}; margin: 0; text-transform: uppercase;">
            SYSTEM STATE: {state}
        </h2>
    </div>
    """
    return indicator_html

# --- Dashboard Interface ---
st.title("🤖 Virtual Control Panel – Interactive Machine Dashboard")
st.markdown("A simulation of an industrial HMI for real-time monitoring and control.")

# --- Layout Containers ---
header = st.container()
controls = st.container()
metrics = st.container()
charts = st.container()

# --- Control Panel (Moved up for better flow) ---
with controls:
    st.subheader("Control Panel")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("START Machine"): # 'type' auto-set by theme
            st.session_state.machine.toggle_start()
            
    with col2:
        if st.button("STOP Machine"):
            st.session_state.machine.toggle_stop()
            
    with col3:
        if st.button("Reset Simulation"):
            st.session_state.machine = Machine()
            st.session_state.data = pd.DataFrame(columns=['time', 'temperature', 'voltage', 'speed'])
            st.success("Simulation reset to initial state.")

# --- Header & Status (Placeholders) ---
with header:
    st.header("System Status")
    # This 'status_placeholder' will be updated in real-time
    status_placeholder = st.empty()

# --- Live Metrics (Placeholders) ---
with metrics:
    st.subheader("Live Sensor Data")
    m_col1, m_col2, m_col3 = st.columns(3)
    temp_metric = m_col1.empty()
    voltage_metric = m_col2.empty()
    speed_metric = m_col3.empty()

# --- Live Charts (Placeholder) ---
with charts:
    st.subheader("Sensor Data History")
    chart_placeholder = st.empty()

# --- Main Simulation Loop ---
while True:
    # 1. Update the machine state
    st.session_state.machine.update()
    status = st.session_state.machine.get_status()

    # 2. Update historical data
    new_data = pd.DataFrame({
        'time': [pd.Timestamp.now()],
        'temperature': [status['temperature']],
        'voltage': [status['voltage']],
        'speed': [status['speed']]
    })
    st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
    st.session_state.data = st.session_state.data.tail(100)

    # 3. Update Status Header (NOW WITH COLOR!)
    with status_placeholder.container():
        # Display the new HTML indicator
        st.markdown(get_status_indicator_html(status['state']), unsafe_allow_html=True)
        # Display the text message
        st.info(f"**Message:** {status['state_message']}")
        # st.markdown(f"**Running:** {'YES' if status['running'] else 'NO'}")

    # 4. Update Metrics
    # (Calculate deltas based on current state to be more intelligent)
    temp_delta = status['temperature'] - Machine.AMBIENT_TEMP
    
    if status['state'] == Machine.STATE_ACTIVE:
        volt_delta = status['voltage'] - 240
        speed_delta = status['speed'] - 1500
    else:
        volt_delta = status['voltage']
        speed_delta = status['speed']

    temp_metric.metric(
        label="Temperature", 
        value=f"{status['temperature']:.1f} °C",
        delta=f"{temp_delta:.1f} °C vs. Ambient",
        delta_color="inverse" if status['state'] == Machine.STATE_OVERHEATING else "normal"
    )
    
    voltage_metric.metric(
        label="Voltage", 
        value=f"{status['voltage']:.1f} V", 
        delta=f"{volt_delta:.1f} V vs. Nominal (240V)"
    )
    
    speed_metric.metric(
        label="Motor Speed", 
        value=f"{status['speed']:.0f} RPM",
        delta=f"{speed_delta:.0f} RPM vs. Nominal (1500 RPM)"
    )

    # 5. Update Charts
    with chart_placeholder.container():
        chart_data = st.session_state.data.melt(
            'time', 
            var_name='Sensor', 
            value_name='Value',
            value_vars=['temperature', 'speed']
        )
        
        st.line_chart(
            chart_data,
            x='time',
            y='Value',
            color='Sensor'
        )

    # 6. Wait for the next tick
    time.sleep(1.0)