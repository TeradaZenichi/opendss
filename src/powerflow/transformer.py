def add_transformer(dss, bus1, bus2, phases, kV, kVA, XHL, XHT, XLT, R, conn='wye'):

    # Default transformer with 2 windings
    # More information of parameters in https://opendss.epri.com/Properties16.html
    dss.Command(
        f"New Transformer.Trans_{bus1}_{bus2} Bus1={bus1} Bus2={bus2} Phases={phases} KVs={kV} kVAs={kVA} XHL={XHL} Conn={conn}"
    )
    print(f"Transformer added between buses {bus1} and {bus2}")