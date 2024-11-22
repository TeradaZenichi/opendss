# Add generators in timestep i for a loop operation in OpenDSS
import pandas as pd

def add_gd(i, name, bus, phases, conn, kV, kW, profile, model=1, vminpu=0.92):

  # Conectada em estrela
  profile['datetime'] = pd.to_datetime(profile['datetime'])
  Ppower = profile[profile['datetime'] == i]['Ppower'].values[0]
  Qpower = profile[profile['datetime'] == i]['Qpower'].values[0]
  new_gd = f"New Generator.{name} bus1={bus} Phases={phases} Conn={conn} kV={kV} kW={kW*Ppower:.2f} kVAr={kW*Qpower:.2f} Model={model} Vminpu={vminpu}"

  return new_gd

#Add a informations of the generator in a dictionary of generators
def distgen_dictionary(bus, phases, base_kv, base_power, dir_profile):
  distgen = {
          'bus': f"bus_{bus}.1.2.3",
          'phases': phases,
          'voltage': base_kv,
          'power': base_power,
          'profile': pd.read_csv(dir_profile),
          'conn': 'delta'
      }
  return distgen