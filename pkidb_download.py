import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

def get_data_from_pkidb():
    """
    Get PKI table from PKIDB website.
    """
    
    # Request content from URL
    r = requests.get("http://www.icoa.fr/pkidb/index.html")
    r.raise_for_status()

    # Transform into html
    html = BeautifulSoup(r.text, features='html.parser')

    # Get table
    table = html.find('table', id="customers")

    # Get table column names
    header = table.find('thead')
    header = [i.text for i in header.find_all('th')]

    # Get table rows
    body = table.find('tbody')
    rows = body.find_all('tr')    
    # Separator needed to replace <br> with space, otherwise 'a</br>b' becomes 'ab' instead of 'a b'
    rows = [[cell.get_text(separator=u' ') for cell in row.find_all('td')] for row in rows]  
    
    # Cast data to DataFrame
    pkidb_ligands = pd.DataFrame(rows, columns=header)
    pkidb_ligands.rename(columns={i: i.replace(' ', '_') for i in pkidb_ligands.columns}, inplace=True)
    pkidb_ligands.rename(columns={'Melting_points_(°C)': 'Melting_points_C'}, inplace=True)
    
    # Set dtypes
    pkidb_ligands = pkidb_ligands.astype(
        {
            'Phase': 'float64', 
            'Type': 'float64',
            'RoF': 'int32', 
            'MW': 'float64', 
            'LogP': 'float64', 
            'TPSA': 'float64',
            'HBA': 'int32', 
            'HBD': 'int32',  
            'NRB': 'int32',
            #'First_Approval': 'int32'
        }
    )
    
    # Some values are nan or Nan but of type str: Replace by None
    pkidb_ligands.replace(to_replace={'nan': None}, value=None, method=None, inplace=True)
    pkidb_ligands.replace(to_replace={'NaN': None}, value=None, method=None, inplace=True)
    
    # LigID column: Remove '' from string
    pkidb_ligands.LigID = pkidb_ligands.LigID.apply(lambda x: x if x is None else x.replace("'", ''))
    
    # Split multiple entries to list
    pkidb_ligands.BrandName = pkidb_ligands.BrandName.apply(lambda x: x if x is None else x.split(';'))
    pkidb_ligands.pdbID = pkidb_ligands.pdbID.apply(lambda x: x if x is None else x.split())
    pkidb_ligands.Targets = pkidb_ligands.Targets.apply(lambda x: x if x is None else x.split())
    pkidb_ligands.Kinase_families = pkidb_ligands.Kinase_families.apply(lambda x: None if x=='' else x.split())    
    pkidb_ligands.Synonyms = pkidb_ligands.Synonyms.apply(lambda x: x if x is None else x.split())
    
    # FDA_approved, Melting_points_C columns: Replace '' by None
    pkidb_ligands.FDA_approved = pkidb_ligands.FDA_approved.apply(lambda x: None if x=='' else x)
    pkidb_ligands.Melting_points_C = pkidb_ligands.Melting_points_C.apply(lambda x: None if x=='' else x)  # Still not pretty (ranges as strings)
    
    # Extract SMILES and InChIKeys
    encoding = pkidb_ligands.Canonical_Smiles_InChiKey
    encoding = encoding.apply(lambda x: x.replace('Smiles =', 'Smiles='))
    encoding = encoding.apply(lambda x: x.replace('InChiKey =', 'InChiKey='))
    encoding = encoding.apply(lambda x: x.split())
    pkidb_ligands['Canonical_Smiles'] = encoding.apply(lambda x: x[0].replace('Smiles=', ''))
    pkidb_ligands['InChIKey'] = encoding.apply(lambda x: x[1].replace('InChiKey=', ''))
    
    # Links column: Remove
    pkidb_ligands.drop(['Links', 'Canonical_Smiles_InChiKey'], axis=1, inplace=True)
    
    return pkidb_ligands
