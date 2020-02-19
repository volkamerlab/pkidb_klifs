# Extract protein kinase inhibitor data

This small repository (i) collects protein kinase inhibitors (PKIs) in clinical trails from the PKIDB and (ii) extracts PKIs deposited in KLIFS.

## Quick start

Use the quick start notebook `quick_start.ipynb` to quickly access the datasets on (i) PKIs in PKIDB and (ii) PKIs in KLIFS.

## Data sources

- PKIDB, a curated, annotated and updated database of protein kinase inhibitors in clinical trials
  - Website: http://www.icoa.fr/pkidb/
  - Literature: http://doi.org/10.3390/molecules23040908
- KLIFS, the kinase-ligand interaction fingerprints and structures database
  - Website: https://klifs.vu-compmedchem.nl/
  - Literature: https://doi.org/10.1093/nar/gkv1082 and https://doi.org/10.1021/jm400378w

## Objectives

- Download PKIs from PKIDB (`pkidb_download.ipynb`)
- Extract all KLIFS ligands that are PKIs based on PKIDB (`pkidb_ligands_in_klifs.ipynb`)

## Copyright

Copyright (c) 2020, Dominique Sydow


