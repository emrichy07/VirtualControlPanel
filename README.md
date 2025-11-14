# Virtual Control Panel – Interactive Machine Dashboard

A Streamlit-based simulation of an industrial control panel (HMI) showing live sensor data, control toggles, and system states. This project demonstrates software engineering and system simulation concepts relevant to industrial automation and digitalization.



---

## Overview

This project is a **Virtual Control Panel** (or Human-Machine Interface) built in Python and Streamlit. It simulates the front-end monitoring and control system for a generic industrial machine. The dashboard displays **live sensor data** (Temperature, Voltage, Motor Speed), provides **operator controls** (Start, Stop, Reset), and visualizes the machine's **finite state** (Idle, Active, Overheating, Recovery).

The application is built with a clean separation of concerns:
* **`machine.py`:** A backend simulation module that manages the machine's state and generates sensor data.
* **`app.py`:** A Streamlit front-end that serves as the visual interface, consuming and displaying data from the simulation.

## Concept & Engineering Context

In industrial settings (factories, power plants, etc.), operators do not interact with machinery directly. Instead, they use an **HMI**—a software application on a screen—to monitor system health and give commands.

These HMIs are critical for:
* **Visualization:** Showing complex data in an easy-to-understand way.
* **Control:** Safely starting, stopping, or adjusting processes.
* **Alarms:** Alerting operators to dangerous conditions, like a motor overheating.

This project simulates a simplified version of this very system, a core component of modern automation.

---

## Features

* **Real-Time Monitoring:** Dashboard updates every second with new, simulated sensor data.
* **Interactive Controls:** Start, Stop, and Reset buttons in the sidebar directly control the machine's simulation.
* **State-Based Simulation:** The machine's behavior (e.g., sensor readings, temperature rise) changes based on its current state.
* **HMI-Style State Indicators:** Large, color-coded banners (Green, Red, Yellow, Grey) make the system status immediately clear.
* **Live Data Charting:** A rolling line chart plots temperature and speed over time.
* **Themed Interface:** Uses a Siemens-like teal color theme (`#009999`) for a professional, industry-specific feel.

---

## Machine Simulation Logic

The core logic is in `machine.py`. The `Machine` class acts as a [Finite State Machine (FSM)](https://en.wikipedia.org/wiki/Finite-state_machine) and sensor data generator.

* **States:** `IDLE`, `ACTIVE`, `OVERHEATING`, `RECOVERY`
* **Sensors:** `temperature`, `voltage`, `speed`
* **Logic:**
    * In `ACTIVE` state, temperature slowly rises, and sensors report nominal values.
    * If `temperature` exceeds **80°C**, the state changes to `OVERHEATING`.
    * In `OVERHEATING`, sensors become erratic, and a recovery counter starts.
    * After 5 "ticks" of overheating, the state moves to `RECOVERY`.
    * In `RECOVERY`, the machine simulates a reduced load (low speed) and active cooling.
    * Once `temperature` drops below **40°C**, the machine returns to `IDLE` and must be manually restarted.

## Machine State Diagram

The diagram below shows the possible transitions between the machine's states.