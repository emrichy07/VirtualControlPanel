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
    # Create and store the machine instance
    st.session_state.machine = Machine()
    print("Initialized Machine object in session state.")

if 'data' not in st.session_state:
    # Store historical data for charts
    st.session_state.data = pd.DataFrame(columns=['time', 'temperature', 'voltage', 'speed'])

# --- Helper Functions ---
def get_status_color(state):
    """Returns a color based on the machine state."""
    if state == Machine.STATE_ACTIVE:
        return "green"
    if state == Machine.STATE_OVERHEATING:
        return "red"
    if state == Machine.STATE_RECOVERY:
        return "yellow"
    return "gray" # Idle

# --- Dashboard Interface ---
st.title("🤖 Virtual Control Panel – Interactive Machine Dashboard")
st.markdown("A simulation of an industrial HMI for real-time monitoring and control.")

# --- Layout Containers ---
# We'll use a combination of columns and empty containers for a dynamic layout
header = st.container()
metrics = st.container()
controls = st.container()
charts = st.container()

# --- Header & Status ---
with header:
    st.header("System Status")
    # This 'status_placeholder' will be updated in real-time
    status_placeholder = st.empty()

# --- Control Panel ---
with controls:
    st.subheader("Control Panel")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("START Machine", type="primary"):
            st.session_state.machine.toggle_start()
            
    with col2:
        if st.button("STOP Machine", type="secondary"):
            st.session_state.machine.toggle_stop()
            
    with col3:
        if st.button("Reset Simulation"):
            # Re-initialize the machine and data
            st.session_state.machine = Machine()
            st.session_state.data = pd.DataFrame(columns=['time', 'temperature', 'voltage', 'speed'])
            st.success("Simulation reset to initial state.")


# --- Live Metrics ---
with metrics:
    st.subheader("Live Sensor Data")
    # These placeholders will be updated by the main loop
    m_col1, m_col2, m_col3 = st.columns(3)
    temp_metric = m_col1.empty()
    voltage_metric = m_col2.empty()
    speed_metric = m_col3.empty()

# --- Live Charts ---
with charts:
    st.subheader("Sensor Data History")
    # This placeholder will hold our updating line chart
    chart_placeholder = st.empty()

# --- Main Simulation Loop ---
# This is the core logic that makes the dashboard "live".
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
    # Keep only the last 100 data points for performance
    st.session_state.data = st.session_state.data.tail(100)

    # 3. Update Status Header
    with status_placeholder.container():
        st.subheader(f"Current State: {status['state']}")
        st.write(status['state_message'])
        st.markdown(f"**Running:** {'YES' if status['running'] else 'NO'}")

    # 4. Update Metrics
    temp_metric.metric(
        label="Temperature", 
        value=f"{status['temperature']:.1f} °C",
        delta=f"{status['temperature'] - Machine.AMBIENT_TEMP:.1f} °C vs. Ambient"
    )
    
    voltage_metric.metric(
        label="Voltage", 
        value=f"{status['voltage']:.1f} V", 
        delta=f"{status['voltage'] - 240:.1f} V vs. Nominal (240V)"
    )
    
    speed_metric.metric(
        label="Motor Speed", 
        value=f"{status['speed']:.0f} RPM",
        delta=f"{status['speed'] - 1500:.0f} RPM vs. Nominal (1500 RPM)"
    )

    # 5. Update Charts
    with chart_placeholder.container():
        # Create a chart with Temperature and Speed
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
    # This controls the refresh rate of the dashboard
    time.sleep(1.0)