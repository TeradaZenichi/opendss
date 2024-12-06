# Get the power flow in branchs 
import pandas as pd
import re

def get_dist_power_luiza(column, i, power_df, buses):
  
  bus_to_search = []
  for bus in buses.keys():
     loads = buses[bus].keys()
     for load in loads:
      buses[bus][load]['profile']['datetime'] = pd.to_datetime(buses[bus][load]['profile']['datetime'])
      Ppower = buses[bus][load]['profile'][buses[bus][load]['profile']['datetime'] == i]['Ppower'].values[0]
      Qpower = buses[bus][load]['profile'][buses[bus][load]['profile']['datetime'] == i]['Qpower'].values[0]
      bus_to_search.append([load, bus, buses[bus][load]['power']*Ppower, buses[bus][load]['power']*Qpower])  

  node_power_df = pd.DataFrame(columns = column)

  for bus in bus_to_search:
      flow_in  = power_df.index[power_df['bus_2'] == bus[1]].tolist()

      flow_out = power_df.index[power_df['bus_1'] == bus[1]].tolist()

      P_in, P_out = 0, 0
      if (flow_in != []): P_in = power_df.loc[flow_in[-1], 'P']
      if (flow_out != []):P_out = power_df.loc[flow_out[0], 'P']
      P_node = P_in + P_out

      Q_in, Q_out = 0, 0
      if (flow_in != []): Q_in = power_df.loc[flow_in[-1], 'Q']
      if (flow_out != []):Q_out = power_df.loc[flow_out[0], 'Q']
      Q_node = Q_in + Q_out

      node_power_df = pd.concat([node_power_df, pd.DataFrame([[i, bus[0], P_node, Q_node, bus[2], bus[3]]], columns=column)])

  return node_power_df

def get_bus_power(buses,dss):
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
def display_branch_flows(dss):
    print("\nFlows in Branches:")
    print("Branch\t\tTotal Current (A)\tActive Power (kW)\tReactive Power (kvar)\t\tLosses (kW)")
    lines = dss.Lines.AllNames()  # List of all lines in the circuit
    for line in lines:
        dss.Circuit.SetActiveElement(f"Line.{line}")
        currents = sum(dss.CktElement.CurrentsMagAng()[::2])  # Sum of currents
        powers = dss.CktElement.Powers()  # Powers at both ends
        P_origin = sum(powers[::2][:3])  # Active power at the origin end
        Q_origin = sum(powers[1::2][:3])  # Reactive power at the origin end
        losses = dss.CktElement.Losses()[0] / 1000  # Losses (in kW)
        print(f"{line}\t\t{currents:.4f}\t\t{P_origin:.4f}\t\t\t{Q_origin:.4f}\t\t\t{losses:.4f}")