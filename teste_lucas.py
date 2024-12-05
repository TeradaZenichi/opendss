import opendssdirect as dss
import re

# Function to load the circuit
def load_circuit(dss_file):
    print(f"Loading file: {dss_file}")
    dss.Command("ClearAll")  # Clears all previously loaded circuits and elements
    dss.Command(f"Redirect {dss_file}")  # Loads the new circuit
    if not dss.Circuit.Name():
        raise RuntimeError("Error loading the circuit. Check the .dss file.")
    print(f"Circuit loaded: {dss.Circuit.Name()}")

# Function to add fictitious loads to buses
def add_fictitious_loads(buses):
    for bus in buses:
        load_name = f"Load_{bus}"
        # dss.Command(
        #     f"New Load.{load_name} bus1={bus} Phases=3 kV=0.22 kW=10 kVAr=5 Model=8 Class=1 Vminpu=0.92 ZIPV=(0.5, 0, 0.5, 1, 0, 0, 0.5)"
        # )
        dss.Command(
            f"New Load.{load_name} bus1={bus} Phases=3 kV=0.22 kW=10 kVAr=5 "
        )
        print(f"Fictitious load added to bus: {bus}")

#Function to add battery to buses
def add_battery(buses):
    bess_name = f"Bess_{buses[3]}"
    # dss.Command(
    #         f"New Load.{bess_name} bus1={buses[3]} Phases=3 kV=0.22 kW=-5 kVAr=0 "
    #     )
    # Documentation of comand in https://opendss.epri.com/Properties5.html
    dss.Command(
        f"New Storage.{bess_name} bus1={buses[3]} Phases=3 kV=0.22 kW=5 kWhRated=10 %stored=100 " # kW>0: charging, kW<0: discharging 
    )
    print(f"Bess added to bus: {buses[3]}")

# Function to calculate and display power at buses
def display_bus_powers(buses):
    print("\nPowers at Buses:")
    print("Bus\tActive Power (kW)\tReactive Power (kvar)")

    total_active_power = 0
    total_reactive_power = 0
    elements = dss.Circuit.AllElementNames()
    for bus in buses:
        active_power = 0
        reactive_power = 0

        # Filtra as cargas associadas ao barramento atual
        # loads = [element for element in elements if element.startswith("Load.") and bus in element]
        loads = [element for element in elements if re.search(f"{bus}", element)]

        for load in loads:
            dss.Circuit.SetActiveElement(load)
            powers = dss.CktElement.Powers()
            active_power += sum(powers[::2])  # Somando potências ativas
            reactive_power += sum(powers[1::2])  # Somando potências reativas

        # Acumula as potências totais
        total_active_power += active_power
        total_reactive_power += reactive_power

        # Exibe as potências do barramento atual
        print(f"{bus}\t{active_power:.4f}\t\t{reactive_power:.4f}")

    # Exibe as potências totais do sistema
    print("\nTotal Active Power (kW): {:.4f}".format(total_active_power))
    print("Total Reactive Power (kvar): {:.4f}".format(total_reactive_power))

    return total_active_power,total_reactive_power

# Function to calculate and display power and current flows in branches
def display_branch_flows(elements):
    print("\nFlows in Branches:")
    print("Branch\t\tTotal Current (A)\tActive Power (kW)\tReactive Power (kvar)\t\tLosses (kW)")
    for element in elements:
        dss.Circuit.SetActiveElement(f"Line.{element}")
        currents = sum(dss.CktElement.CurrentsMagAng()[::2])  # Sum of currents
        powers = dss.CktElement.Powers()  # Powers at both ends
        P_origin = sum(powers[::2][:3])  # Active power at the origin end
        Q_origin = sum(powers[1::2][:3])  # Reactive power at the origin end
        losses = dss.CktElement.Losses()[0] / 1000  # Losses (in kW)
        print(f"{element}\t\t{currents:.4f}\t\t{P_origin:.4f}\t\t\t{Q_origin:.4f}\t\t\t{losses:.4f}")

# Main function
def main():
    dss_file = "datasets/arquivos_dss/lucas.dss"  # Replace with the correct path
    dss.Basic.ClearAll()
    dss.Basic.Start(0)
    load_circuit(dss_file)
    buses = dss.Circuit.AllBusNames()
    elements = dss.Lines.AllNames()  # List of all lines in the circuit
    add_fictitious_loads(buses)
    add_battery(buses)
    dss.Solution.Solve()  # Solve the power flow

    # Display bus voltages
    voltages = dss.Circuit.AllBusVMag()
    
    print("\nBus Phase Voltages (V):")
    for bus, voltage in zip(buses, voltages):
        print(f"{bus}: {voltage:.4f}")

 
    # Display powers at buses
    total_activepower,total_reactivepower = display_bus_powers(buses)

    # Display power and current flows in branches
    display_branch_flows(elements)

    print("\nPower delivered to circuit:")
    print("Active power (kW)\tReactive power (kvar)")
    total_power = dss.Circuit.TotalPower()
    print(f"\t{total_power[0]:.4f}\t\t{total_power[1]:.4f}")
    print("\nTotal losses (kW): ")
    active_losses,reactive_losses = dss.Circuit.Losses()
    print(f"\t{active_losses / 1000:.4f}")

    print("\nPower Balance:")
    print("Active Power (kW)\tReactive Power (kvar)")
    print(f"\t{abs(total_power[0])-(total_activepower+active_losses/1000):.4f}\t\t{abs(total_power[1])-(total_reactivepower+reactive_losses/1000):.4f}")
if __name__ == "__main__":
    main()
