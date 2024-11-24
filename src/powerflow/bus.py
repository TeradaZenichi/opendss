import pandas as pd

def bus_dictionary(n_bus):
  bus = { }
  
  for i in range(1,n_bus+1):
    name = f"bus_{str(i).zfill(3)}"
    bus[name] = {}

  return bus