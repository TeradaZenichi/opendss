#Add a informations of the battery energy storage system in a dictionary of bess
import pandas as pd

def distbess_dictionary(bus, phases, base_kv, base_power, dir_profile):
  distbess = {
          'bus': f"bus_{bus}.1.2.3",
          'phases': phases,
          'voltage': base_kv,
          'power': base_power,
          'profile': pd.read_csv(dir_profile,usecols=['datetime','power']),
          'conn': 'delta'
      }
  return distbess