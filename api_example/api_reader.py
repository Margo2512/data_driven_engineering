import requests
import pandas as pd
import time

categories = {
    "drugs": [2244, 1983, 2662, 3672, 5311],
    "organic": [5365, 6342, 7237, 8122, 9135],
    "inorganic": [222, 333, 444, 555, 666],
    "amino_acids": [5950, 6106, 6287, 6458, 6657],
    "vitamins": [5280343, 5280450, 5280489, 5280494, 5280794],
}
headers = {"Content-Type": "application/json"}


def fetch_pubchem_compounds():
    all_data = []
    for category, cids in categories.items():
        for cid in cids:
            try:
                url = (
                    f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/JSON"
                )
                response = requests.get(url, timeout=10, headers=headers)
                if response.status_code == 200:
                    answer = response.json()
                    all_data.append(extract_compound_info(answer, category))
                    print(f"Собрано: {len(all_data)} соединений")
                    time.sleep(0.5)
                else:
                    print(f"WARNING! Status: {response.status_code}")
            except Exception as e:
                print(f"Ошибка CID {cid}: {e}")
                continue
    return pd.DataFrame(all_data)


def extract_compound_info(data, category):
    compounds = data.get("PC_Compounds", [{}])[0]
    props = compounds.get("props", [])
    properties = {}
    for prop in props:
        label = prop.get("urn", {}).get("label", "")
        value = (
            prop.get("value", {}).get("sval", "")
            or prop.get("value", {}).get("fval", "")
            or prop.get("value", {}).get("ival", "")
        )
        properties[label] = value
    return {
        "cid": data.get("PC_Compounds", [{}])[0]
        .get("id", {})
        .get("id", {})
        .get("cid", ""),
        "category": category,
        "molecular_formula": properties.get("Molecular Formula", ""),
        "molecular_weight": properties.get("Molecular Weight", ""),
        "iupac_name": properties.get("IUPAC Name", ""),
        "smiles": properties.get("SMILES", ""),
        "inchi": properties.get("InChI", ""),
        "logp": properties.get("Log P", ""),
        "polar_surface_area": properties.get("Polar Surface Area", ""),
        "heavy_atom_count": properties.get("Heavy Atom Count", ""),
        "complexity": properties.get("Complexity", ""),
        "h_bond_donor": properties.get("Hydrogen Bond Donor Count", ""),
        "h_bond_acceptor": properties.get("Hydrogen Bond Acceptor Count", ""),
        "rotatable_bonds": properties.get("Rotatable Bond Count", ""),
        "exact_mass": properties.get("Exact Mass", ""),
        "topological_polar_surface": properties.get(
            "Topological Polar Surface Area", ""
        ),
        "atom_stereo_count": properties.get("Atom Stereocenter Count", ""),
        "defined_atom_stereo": properties.get("Defined Atom Stereocenter Count", ""),
    }


df = fetch_pubchem_compounds()
print(f"Итоговый датасет: {df.shape}")
df.to_csv("pubchem_chemical_dataset.csv", index=False)
print(df.info())
print(df.head())
