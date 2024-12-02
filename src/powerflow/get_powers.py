# Get the power flow in branchs 
import pandas as pd

# def get_dist_power(column, i, power_df, buses):
  
#   bus_to_search = []
#   for bus in buses.keys():
#      loads = buses[bus].keys()
#      for load in loads:
#       buses[bus][load]['profile']['datetime'] = pd.to_datetime(buses[bus][load]['profile']['datetime'])
#       Ppower = buses[bus][load]['profile'][buses[bus][load]['profile']['datetime'] == i]['Ppower'].values[0]
#       Qpower = buses[bus][load]['profile'][buses[bus][load]['profile']['datetime'] == i]['Qpower'].values[0]
#       bus_to_search.append([bus, buses[bus][load]['power']*Ppower, buses[bus][load]['power']*Qpower])  

# #   for gen in distgen:   
# #      distgen[gen]['profile']['datetime'] = pd.to_datetime(distgen[gen]['profile']['datetime'])
# #      Ppower = distgen[gen]['profile'][distgen[gen]['profile']['datetime'] == i]['Ppower'].values[0]
# #      Qpower = distgen[gen]['profile'][distgen[gen]['profile']['datetime'] == i]['Qpower'].values[0]
# #      bus_to_search.append([gen,  distgen[gen]['bus'].split('.', 1)[0], distgen[gen]['power']*Ppower, distgen[gen]['power']*Qpower])
#   # for bess in distbess: bus_to_search.append([bess, distbess[bess]['bus'].split('.', 1)[0], distbess[bess]['power']*distbess[bess]['profile'][0][i], distbess[bess]['power']*distbess[bess]['profile'][1][i]])

#   # print(bus_to_search)

#   node_power_df = pd.DataFrame(columns = column)

#   for bus in bus_to_search:
#       # Procurar os valores de potência dos barramentos das cargas e geração distribuída
#       # print('bus')
#       # print(bus[0], bus[1])

#       flow_in  = power_df.index[power_df['bus_2'] == bus[0]].tolist()
#       # print('flow in\n',flow_in)
#       # Tratar flow in para ver se tem algum nó

#       flow_out = power_df.index[power_df['bus_1'] == bus[0]].tolist()
#       # print('flow out\n',flow_out)
#       # Tratar flow out para ver se tem algum nó

#       # print(flow_in, flow_out)
#       P_in, P_out = 0, 0
#       if (flow_in != []): P_in = power_df.loc[flow_in[-1], 'P']
#       if (flow_out != []):P_out = power_df.loc[flow_out[0], 'P']
#       P_node = P_in + P_out

#       Q_in, Q_out = 0, 0
#       if (flow_in != []): Q_in = power_df.loc[flow_in[-1], 'Q']
#       if (flow_out != []):Q_out = power_df.loc[flow_out[0], 'Q']
#       Q_node = Q_in + Q_out



#       node_power_df = pd.concat([node_power_df, pd.DataFrame([[i, bus[0], P_node, Q_node, bus[1], bus[2]]], columns=column)])

#       # print(bus[0], '// P: ', P_node, '// Q: ', Q_node)

#   # display(node_power_df)
#   return node_power_df

def get_dist_power(i,column, power_df, buses,dss):
  
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
    print(P_in, P_out)
    P_node = P_in + P_out

    Q_in, Q_out = 0, 0
    if (flow_in != []): Q_in = power_df.loc[flow_in[-1], 'Q']
    if (flow_out != []):Q_out = power_df.loc[flow_out[0], 'Q']
    Q_node = Q_in + Q_out

    node_power_df = pd.concat([node_power_df, pd.DataFrame([[i, bus, P_node, Q_node,voltage_magnitudes]], columns=column)])

  return node_power_df


def get_bus_power(datetime,column,buses,dss):

  node_power_df = pd.DataFrame(columns = column)

  bus_data = []
  
  for bus in buses.keys():
    dss.Circuit.SetActiveBus(bus)

    # Obter as tensões no barramento (em magnitude e ângulo)
    voltages = dss.Bus.VMagAngle()
    voltage_phases = len(voltages) // 2  # Cada par (mag, ang) é uma fase
    voltage_magnitudes = voltages[0::2]  # Apenas magnitudes
    voltage_angles = voltages[1::2]     # Apenas ângulos

    # Potências vêm em pares [P1, Q1, P2, Q2, ..., Pn, Qn]
    powers = dss.CktElement.Powers() if dss.CktElement.Name() else []
    active_powers = powers[0::2] if powers else [0]  # Apenas potências ativas (P)
    reactive_powers = powers[1::2] if powers else [0]  # Apenas potências reativas (Q)

    bus_data.append([datetime,bus, sum(active_powers), sum(reactive_powers), sum(voltage_magnitudes)])
  
  node_power_df = pd.concat([node_power_df, pd.DataFrame(bus_data, columns=column)])

  return node_power_df