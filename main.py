# código que testa a melhor posição da bateria
from dss import DSS # type: ignore
import math
import numpy as np
import opendssdirect as DSS1
import pandas as pd

from scipy.ndimage import gaussian_filter,gaussian_filter1d

Text = DSS.Text
Circuit = DSS.ActiveCircuit
Solution = DSS.ActiveCircuit.Solution

opendssmodel = "ModelagemLabREI.dss"

DSS.ClearAll()
DSS.Start(0)
# print(path, name)

Text.Command = "Clear"
Text.Command = f"Compile {opendssmodel}"

bus_names = np.array(DSS1.Circuit.AllBusNames())
print(bus_names)

# # I would like to add this command Text.Command = "New Line.Line_002_load bus1=bus_002 bus2=bus_021 Length=0.01 Units=m Geometry=Geometria phases=3"
# Text.Command = "New Line.Line_002_load bus1=bus_002 bus2=bus_021 Length=0.01 Units=m Geometry=Geometria phases=3"

# apply to DSS1
DSS1.run_command('New Line.Line_002_load bus1=bus_002 bus2=bus_021 Length=0.01 Units=m Geometry=Geometria phases=3')



bus_names = np.array(DSS1.Circuit.AllBusNames())
print(bus_names)

print('fim do programa')