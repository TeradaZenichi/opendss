# Get the power flow in branchs 
import pandas as pd

def get_dist_power(column, i, power_df, loads):
  
  bus_to_search = []
  for load in loads:
     loads[load]['profile']['datetime'] = pd.to_datetime(loads[load]['profile']['datetime'])
     Ppower = loads[load]['profile'][loads[load]['profile']['datetime'] == i]['Ppower'].values[0]
     Qpower = loads[load]['profile'][loads[load]['profile']['datetime'] == i]['Qpower'].values[0]
     bus_to_search.append([load, loads[load]['bus'].split('.', 1)[0], loads[load]['power']*Ppower, loads[load]['power']*Qpower])  

#   for gen in distgen:   
#      distgen[gen]['profile']['datetime'] = pd.to_datetime(distgen[gen]['profile']['datetime'])
#      Ppower = distgen[gen]['profile'][distgen[gen]['profile']['datetime'] == i]['Ppower'].values[0]
#      Qpower = distgen[gen]['profile'][distgen[gen]['profile']['datetime'] == i]['Qpower'].values[0]
#      bus_to_search.append([gen,  distgen[gen]['bus'].split('.', 1)[0], distgen[gen]['power']*Ppower, distgen[gen]['power']*Qpower])
  # for bess in distbess: bus_to_search.append([bess, distbess[bess]['bus'].split('.', 1)[0], distbess[bess]['power']*distbess[bess]['profile'][0][i], distbess[bess]['power']*distbess[bess]['profile'][1][i]])

  # print(bus_to_search)

  node_power_df = pd.DataFrame(columns = column)

  for bus in bus_to_search:
      # Procurar os valores de potência dos barramentos das cargas e geração distribuída
      # print('bus')
      # print(bus[0], bus[1])

      flow_in  = power_df.index[power_df['bus_2'] == bus[1]].tolist()
      # print('flow in\n',flow_in)
      # Tratar flow in para ver se tem algum nó

      flow_out = power_df.index[power_df['bus_1'] == bus[1]].tolist()
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



      node_power_df = pd.concat([node_power_df, pd.DataFrame([[i, bus[0], P_node, Q_node, bus[2], bus[3]]], columns=column)])

      # print(bus[0], '// P: ', P_node, '// Q: ', Q_node)

  # display(node_power_df)
  return node_power_df