# Get the power flow in branchs 
import pandas as pd

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

def get_bus_power(column, i, power_df, buses,dss):
  
  node_power_df = pd.DataFrame(columns = column)
  for bus in buses.keys():
    dss.Circuit.SetActiveBus(bus)

    # Obter as tensões no barramento (em magnitude e ângulo)
    voltages = dss.Bus.VMagAngle()
    voltage_phases = len(voltages) // 2  # Cada par (mag, ang) é uma fase
    voltage_magnitudes = voltages[0::2]  # Apenas magnitudes
    voltage_angles = voltages[1::2]     # Apenas ângulos

    flow_in  = power_df.index[power_df['bus_2'] == bus].tolist()
    # print('flow in\n',flow_in)
    # Tratar flow in para ver se tem algum nó

    flow_out = power_df.index[power_df['bus_1'] == bus].tolist()
    # print('flow out\n',flow_out)
    # Tratar flow out para ver se tem algum nó

    # print(flow_in, flow_out)
    P_in, P_out = 0, 0
    if (flow_in != []): P_in = power_df.loc[flow_in[-1], 'P']
    if (flow_out != []):P_out = power_df.loc[flow_out[0], 'P']
    P_node = P_in + P_out

    Q_in, Q_out = 0, 0
    if (flow_in != []): Q_in = power_df.loc[flow_in[-1], 'Q']
    if (flow_out != []):Q_out = power_df.loc[flow_out[0], 'Q']
    Q_node = Q_in + Q_out

    node_power_df = pd.concat([node_power_df, pd.DataFrame([[i, bus, P_node, Q_node,voltage_magnitudes]], columns=column)])

  return node_power_df
