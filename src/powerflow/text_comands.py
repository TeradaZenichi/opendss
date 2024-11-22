##----------------- Funções para escrever o arquivo .dss -----------------##

#Set defaut frequency
def set_frequency(frequency):
  return f"Set DefaultBaseFrequency={frequency} \n"

#define the circuit
def new_circuit(name,bus,base_kv):
    new_comand = '!! Equivalente de Thèvenin \n'
    new_comand = new_comand + f"New Circuit.{name} bus1=bus_{bus}.1.2.3 basekV={base_kv} \n"

    return new_comand


#Define the cable specifications
def line_geometry(Rdc,Rac,Runits,Radius,Nconds,Nphases,X,H):
   new_comand = '!! Dados dos cabos e geometria das linhas\n'
   new_comand = new_comand + f"New WireData.Fios Rdc={Rdc} Rac={Rac} Runits={Runits} Radius={Radius} Radunits=mm \n"
   new_comand = new_comand + f"New LineSpacing.N1 Nconds={Nconds} Nphases={Nphases} Units=cm X=[{X[0]}  {X[1]}  {X[2]}] H=[ {H[0]}  {H[1]}  {H[2]}] \n"
   new_comand = new_comand + f"New LineGeometry.Geometria  Nconds={Nconds}  Spacing=N1 Wires=[Fios, Fios, Fios] Reduce=n' \n"

   return new_comand

def add_line(i,bus1, bus2, length, length_units, phases):
  if i==1:
    new_comand = '!! Linhas\n'
    new_comand = new_comand + f"New Line.Line_{bus1}_{bus2} Bus1=bus_{bus1} Bus2=bus_{bus2} Length={length} Units={length_units} Geometry=Geometria phases={phases}"
  else:
    new_comand = f"New Line.Line_{bus1}_{bus2} Bus1=bus_{bus1} Bus2=bus_{bus2} Length={length} Units={length_units} Geometry=Geometria phases={phases}"
  
  return new_comand 
    
def add_infos():
    new_command = """\
    
!! Outras informações
MakeBusList
Set VoltageBases = [.22]
CalcVoltageBases

Set maxiterations = 500
set mode=snap
!! Solve
"""
    return new_command

