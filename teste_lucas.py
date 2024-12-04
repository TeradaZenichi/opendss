import opendssdirect as dss

# Function to load the circuit
def load_circuit(dss_file):
    print(f"Loading file: {dss_file}")
    dss.Command("ClearAll")  # Clears all previously loaded circuits and elements
    dss.Command(f"Redirect {dss_file}")  # Loads the new circuit
    if not dss.Circuit.Name():
        raise RuntimeError("Error loading the circuit. Check the .dss file.")
    print(f"Circuit loaded: {dss.Circuit.Name()}")

# Function to add fictitious loads to buses
def add_fictitious_loads():
    buses = dss.Circuit.AllBusNames()  # List of all buses
    for bus in buses:
        load_name = f"Load_{bus}"
        dss.Command(
            f"New Load.{load_name} Bus1={bus} Phases=3 kV=0.22 kW=10 kvar=5"
        )
        print(f"Fictitious load added to bus: {bus}")

# Function to calculate and display power at buses
def display_bus_powers():
    buses = dss.Circuit.AllBusNames()
    print("\nPowers at Buses:")
    print("Bus\tActive Power (kW)\tReactive Power (kvar)")
    for bus in buses:
        dss.Circuit.SetActiveBus(bus)
        active_power = 0
        reactive_power = 0
        for element in dss.Circuit.AllElementNames():
            dss.Circuit.SetActiveElement(element)
            powers = dss.CktElement.Powers()
            active_power += sum(powers[::2])  # Summing active power
            reactive_power += sum(powers[1::2])  # Summing reactive power
        print(f"{bus}\t{active_power:.4f}\t\t{reactive_power:.4f}")

# Function to calculate and display power and current flows in branches
def display_branch_flows():
    elements = dss.Lines.AllNames()  # List of all lines in the circuit
    print("\nFlows in Branches:")
    print("Branch\tTotal Current (A)\tActive Power (kW)\tReactive Power (kvar)\tLosses (kW)")
    for element in elements:
        dss.Circuit.SetActiveElement(f"Line.{element}")
        currents = sum(dss.CktElement.CurrentsMagAng()[::2])  # Sum of currents
        powers = dss.CktElement.Powers()  # Powers at both ends
        P_origin = sum(powers[::2][:3])  # Active power at the origin end
        Q_origin = sum(powers[1::2][:3])  # Reactive power at the origin end
        losses = sum(dss.CktElement.Losses()) / 1000  # Losses (in kW)
        print(f"{element}\t{currents:.4f}\t\t{P_origin:.4f}\t\t\t{Q_origin:.4f}\t\t\t{losses:.4f}")

# Main function
def main():
    dss_file = "datasets/arquivos_dss/lucas.dss"  # Replace with the correct path
    dss.Basic.ClearAll()
    dss.Basic.Start(0)
    load_circuit(dss_file)
    add_fictitious_loads()
    dss.Solution.Solve()  # Solve the power flow

    # Display bus voltages
    voltages = dss.Circuit.AllBusVMag()
    buses = dss.Circuit.AllBusNames()
    print("\nBus Voltages (pu):")
    for bus, voltage in zip(buses, voltages):
        print(f"{bus}: {voltage:.4f}")

    # Display powers at buses
    display_bus_powers()

    # Display power and current flows in branches
    display_branch_flows()

if __name__ == "__main__":
    main()
