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
    rows = [[cell.text for cell in row.find_all('td')] for row in rows]

    pkidb = pd.DataFrame(rows, columns=header)
    
    # Set dtypes
    pkidb = pkidb.astype(
        {
            'Phase': 'float64', 
            'RoF': 'int32', 
            'MW': 'float64', 
            'LogP': 'float64', 
            'TPSA': 'float64',
            'HBA': 'int32', 
            'HBD': 'int32',  
            'NRB': 'int32' 
        }
    )
    
    # Format some columns
    pkidb['Smiles'] = [i.split('InChiKey=')[0].split('Smiles=')[1] for i in pkidb.Canonical_Smiles_InChiKey]
    pkidb['InChIKey'] = [i.split('InChiKey=')[1] for i in pkidb.Canonical_Smiles_InChiKey]
    pkidb.LigID = [i[1:-1] if i != 'NaN' else np.nan for i in pkidb.LigID]

    return pkidb
