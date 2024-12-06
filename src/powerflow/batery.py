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

def add_battery(buses,dss):
    bess_name = f"Bess_{buses[3]}"
    # dss.Command(
    #         f"New Load.{bess_name} bus1={buses[3]} Phases=3 kV=0.22 kW=-5 kVAr=0 "
    #     )
    # Documentation of comand in https://opendss.epri.com/Properties5.html
    dss.Command(
        f"New Storage.{bess_name} bus1={buses[3]} Phases=3 kV=0.22 kW=5 kWhRated=10 %stored=100 %EffCharge=95 %EffDischarge=95 " # kW>0: charging, kW<0: discharging 
    )
    print(f"Bess added to bus: {buses[3]}")