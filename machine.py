# machine.py

import numpy as np

class Machine:
    """
    A class to simulate an industrial machine's state, controls, 
    and sensor readings.
    """

    # Define state constants
    STATE_IDLE = "IDLE"
    STATE_ACTIVE = "ACTIVE"
    STATE_OVERHEATING = "OVERHEATING"
    STATE_RECOVERY = "RECOVERY"

    # Simulation constants
    AMBIENT_TEMP = 25.0
    TEMP_THRESHOLD_HIGH = 80.0
    TEMP_THRESHOLD_LOW = 40.0
    OVERHEAT_TICKS_LIMIT = 5

    def __init__(self):
        # Initial state
        self.state = self.STATE_IDLE
        self.running = False
        
        # Sensor values
        self.temperature = self.AMBIENT_TEMP
        self.voltage = 0.0
        self.speed = 0.0
        
        # State tracking
        self.state_message = "System is idle. Ready to start."
        self.overheat_counter = 0

    def toggle_start(self):
        """User requests to start the machine."""
        if self.state == self.STATE_IDLE:
            self.running = True
            print("User requested START")

    def toggle_stop(self):
        """User requests to stop the machine."""
        self.running = False
        print("User requested STOP")

    def _update_sensors(self):
        """
        Private method to simulate sensor data based on the current state.
        Uses numpy.random for realistic drift.
        """
        if self.state == self.STATE_ACTIVE:
            self.speed = np.random.normal(1500, 5)  # Nominal 1500 RPM
            self.voltage = np.random.normal(240, 0.5) # Nominal 240 V
            # Temperature rises when active
            self.temperature += np.random.uniform(0.5, 1.5)

        elif self.state == self.STATE_OVERHEATING:
            # Speed becomes erratic, voltage fluctuates
            self.speed = np.random.normal(1550, 20) 
            self.voltage = np.random.normal(240, 2)
            # Temperature continues to rise slightly
            self.temperature += np.random.uniform(0.1, 0.5)
            
        elif self.state == self.STATE_RECOVERY:
            # Load is reduced, speed drops
            self.speed = np.random.normal(300, 3) 
            self.voltage = np.random.normal(242, 0.2) # Stabilizing
            # Temperature cools down actively
            self.temperature -= np.random.uniform(1.0, 2.0)

        elif self.state == self.STATE_IDLE:
            self.speed = 0.0
            self.voltage = 0.0
            # Cools down passively to ambient
            if self.temperature > self.AMBIENT_TEMP:
                self.temperature -= np.random.uniform(0.2, 0.5)
            else:
                self.temperature = self.AMBIENT_TEMP

    def _simulate_state_transitions(self):
        """
        Private method to manage the Finite State Machine (FSM) logic.
        """
        current_state = self.state

        if current_state == self.STATE_IDLE:
            if self.running:
                # Transition: IDLE -> ACTIVE
                self.state = self.STATE_ACTIVE
                self.state_message = "System active and stable."
        
        elif current_state == self.STATE_ACTIVE:
            if not self.running:
                # Transition: ACTIVE -> IDLE
                self.state = self.STATE_IDLE
                self.state_message = "System shutting down."
            elif self.temperature > self.TEMP_THRESHOLD_HIGH:
                # Transition: ACTIVE -> OVERHEATING
                self.state = self.STATE_OVERHEATING
                self.state_message = "CRITICAL: Overheating detected! High temp."
                self.overheat_counter = 0

        elif current_state == self.STATE_OVERHEATING:
            if not self.running:
                # Transition: OVERHEATING -> IDLE (Emergency Stop)
                self.state = self.STATE_IDLE
                self.state_message = "Emergency stop initiated."
            elif self.overheat_counter > self.OVERHEAT_TICKS_LIMIT:
                # Transition: OVERHEATING -> RECOVERY
                self.state = self.STATE_RECOVERY
                self.state_message = "System in recovery mode. Reducing load."
            else:
                self.overheat_counter += 1

        elif current_state == self.STATE_RECOVERY:
            if not self.running:
                # Transition: RECOVERY -> IDLE
                self.state = self.STATE_IDLE
                self.state_message = "Shutdown during recovery."
            elif self.temperature < self.TEMP_THRESHOLD_LOW:
                # Transition: RECOVERY -> IDLE (Cooled down)
                self.state = self.STATE_IDLE
                self.running = False  # Force stop after recovery
                self.state_message = "Recovery complete. System idle. Ready for restart."

    def update(self):
        """
        The main public method called on each "tick" of the simulation.
        It updates sensors first, then checks for state transitions.
        """
        # 1. Simulate sensor data based on the *current* state
        self._update_sensors()
        
        # 2. Check for state transitions based on new sensor data
        self._simulate_state_transitions()

    def get_status(self):
        """
        Returns a dictionary of the machine's current state and data
        for the dashboard to consume.
        """
        return {
            "state": self.state,
            "running": self.running,
            "temperature": self.temperature,
            "voltage": self.voltage,
            "speed": self.speed,
            "state_message": self.state_message
        }

if __name__ == "__main__":
    # Example of how to use the class
    print("Initializing machine simulation...")
    machine = Machine()
    
    print(f"Tick 0: {machine.get_status()}")
    
    # Simulate starting
    machine.toggle_start()
    
    # Simulate 10 ticks of running
    for i in range(1, 11):
        machine.update()
        print(f"Tick {i}: {machine.get_status()}")

    # Simulate stopping
    machine.toggle_stop()
    machine.update()
    print(f"Tick 11: {machine.get_status()}")