# Create a dictionary with the information of the loads
import pandas as pd

# Create a dictionary with the information of the loads
def add_LoadToBus(dict_bus,bus,name, phases, base_kv, base_power, dir_profile):
  load = {
          'phases': phases,
          'voltage': base_kv,
          'power': base_power,
          'profile': pd.read_csv(dir_profile,usecols=['datetime','Ppower','Qpower'])
      }
  dict_bus[bus][name] = load


# Add loads in timestep i for a loop operation in OpenDSS
def add_load(i, name, bus, phases, kV, kW, profile, model=8, classe=1, vminpu=0.92, ZIPV=(0.5, 0, 0.5, 1, 0, 0, 0.5)):
  # Conectada em estrela
  profile['datetime'] = pd.to_datetime(profile['datetime'])
  Ppower = profile[profile['datetime'] == i]['Ppower'].values[0]
  Qpower = profile[profile['datetime'] == i]['Qpower'].values[0]
  new_load = f"New Load.{name} bus1={bus} Phases={phases} kV={kV} kW={kW*Ppower:.2f} kVAr={kW*Qpower:.2f} Model={model} Class={classe} Vminpu={vminpu} ZIPV={ZIPV}"

  return new_load


def bus_dictionary(n_bus):
  bus = { }
  
  for i in range(1,n_bus+1):
    name = f"bus_{str(i).zfill(3)}"
    bus[name] = {}

  return bus

