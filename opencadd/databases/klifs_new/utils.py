"""
opencadd.databases.klifs.utils

Defines utility functions.
"""

import logging
from pathlib import Path

from bravado.client import SwaggerClient
import pandas as pd

_logger = logging.getLogger(__name__)

KLIFS_API_DEFINITIONS = "http://klifs.vu-compmedchem.nl/swagger/swagger.json"
KLIFS_CLIENT = SwaggerClient.from_url(
    KLIFS_API_DEFINITIONS, config={"validate_responses": False}
)

RENAME_COLUMNS_LOCAL_KLIFS_EXPORT = {
    "NAME": "kinase.name",
    "FAMILY": "kinase.family",
    "GROUPS": "kinase.group",
    "PDB": "structure.pdb",
    "CHAIN": "structure.chain",
    "ALTERNATE_MODEL": "structure.alternate_model",
    "SPECIES": "species.klifs",
    "LIGAND": "ligand.orthosteric.name",
    "PDB_IDENTIFIER": "ligand.orthosteric.pdb",
    "ALLOSTERIC_NAME": "ligand.allosteric.name",
    "ALLOSTERIC_PDB": "ligand.allosteric.pdb",
    "DFG": "structure.dfg",
    "AC_HELIX": "structure.ac_helix",
}
RENAME_COLUMNS_LOCAL_KLIFS_OVERVIEW = {
    "species": "species.klifs",
    "kinase": "kinase.name",
    "pdb": "structure.pdb",
    "alt": "structure.alternate_model",
    "chain": "structure.chain",
    "orthosteric_PDB": "ligand.orthosteric.pdb",
    "allosteric_PDB": "ligand.allosteric.pdb",
    "rmsd1": "structure.rmsd1",
    "rmsd2": "structure.rmsd2",
    "qualityscore": "structure.qualityscore",
    "pocket": "kinase.pocket",
    "resolution": "structure.resolution",
    "missing_residues": "structure.missing_residues",
    "missing_atoms": "structure.missing_atoms",
    "full_ifp": "structure.ifp",
    "fp_i": "structure.fp_i",
    "fp_ii": "structure.fp_ii",
    "bp_i_a": "structure.bp_i_a",
    "bp_i_b": "structure.bp_i_b",
    "bp_ii_in": "structure.bp_ii_in",
    "bp_ii_a_in": "structure.bp_ii_a_in",
    "bp_ii_b_in": "structure.bp_ii_b_in",
    "bp_ii_out": "structure.bp_ii_out",
    "bp_ii_b": "structure.bp_ii_b",
    "bp_iii": "structure.bp_iii",
    "bp_iv": "structure.bp_iv",
    "bp_v": "structure.bp_v",
}
RENAME_COLUMNS_REMOTE_KINASE = {
    "kinase_ID": "kinase.id",
    "name": "kinase.name",
    "HGNC": "kinase.hgnc",
    "family": "kinase.family",
    "group": "kinase.group",
    "kinase_class": "kinase.class",
    "species": "species.klifs",
    "full_name": "kinase.name_full",
    "uniprot": "kinase.uniprot",
    "iuphar": "kinase.iuphar",
    "pocket": "kinase.pocket",
}
RENAME_COLUMNS_REMOTE_STRUCTURE = {
    "structure_ID": "structure.id",
    "kinase": "kinase.name",
    "species": "species.klifs",
    "kinase_ID": "kinase.id",
    "pdb": "structure.pdb",
    "alt": "structure.alternate_model",
    "chain": "structure.chain",
    "rmsd1": "structure.rmsd1",
    "rmsd2": "structure.rmsd2",
    "pocket": "kinase.pocket",
    "resolution": "structure.resolution",
    "quality_score": "structure.qualityscore",
    "missing_residues": "structure.missing_residues",
    "missing_atoms": "structure.missing_atoms",
    "ligand": "ligand.name",
    "allosteric_ligand": "ligand.name_allosteric",
    "DFG": "structure.dfg",
    "aC_helix": "structure.ac_helix",
    "Grich_distance": "structure.grich_distance",
    "Grich_angle": "structure.grich_angle",
    "Grich_rotation": "structure.grich_rotation",
    "front": "structure.front",
    "gate": "structure.gate",
    "back": "structure.back",
    "fp_I": "structure.fp_i",
    "fp_II": "structure.fp_ii",
    "bp_I_A": "structure.bp_i_a",
    "bp_I_B": "structure.bp_i_b",
    "bp_II_in": "structure.bp_ii_in",
    "bp_II_A_in": "structure.bp_ii_a_in",
    "bp_II_B_in": "structure.bp_ii_b_in",
    "bp_II_out": "structure.bp_ii_out",
    "bp_II_B": "structure.bp_ii_b",
    "bp_III": "structure.bp_iii",
    "bp_IV": "structure.bp_iv",
    "bp_V": "structure.bp_v",
    "index": "structure.pocket_klifs_numbering",  # Interactions.get_interactions_match_residues()
    "Xray_position": "structure.pocket_pdb_numbering",  # Interactions.get_interactions_match_residues()
    "KLIFS_position": "structure.pocket_regions_klifs",  # Interactions.get_interactions_match_residues()
}
RENAME_COLUMNS_REMOTE_LIGAND = {
    "ligand_ID": "ligand.id",
    "PDB-code": "ligand.pdb",
    "Name": "ligand.name",
    "SMILES": "ligand.smiles",
    "InChIKey": "ligand.inchikey",
}
RENAME_COLUMNS_REMOTE_INTERACTION = {
    "position": "interaction.position",  # Interactions.get_interactions_get_types()
    "name": "interaction.name",  # Interactions.get_interactions_get_types()
    "structure_ID": "structure.id",  # Interactions.get_interactions_get_IFP()
    "IFP": "interaction.fingerprint",  # Interactions.get_interactions_get_IFP()
}
RENAME_COLUMNS_REMOTE_BIOACTIVITY = {
    "pref_name": "kinase.pref_name",
    "accession": "kinase.uniprot",
    "organism": "species.chembl",
    "standard_type": "ligand.bioactivity_type",
    "standard_relation": "ligand.bioactivity_relation",
    "standard_value": "ligand.bioactivity_value",
    "standard_units": "ligand.bioactivity_units",
    "pchembl_value": "ligand.bioactivity_value_pchembl",
}


def file_path(
    path_to_klifs_download,
    species,
    kinase_name,
    structure_pdb,
    structure_alternate_model,
    structure_chain,
    entity="complex",
    format="mol2",
    in_dir=False,
):
    """
    Get file path.

    Parameters
    ----------
    path_to_klifs_download : pathlib.Path or str
        Path to folder for file destination (if in_dir=False) or KLIFS_downlaod folder destination (if in_dir=True).
    species : str
        Species.
    kinase_name : str
        Kinase name.
    structure_pdb : str
        PDB ID.
    structure_alternate_model : str
        Alternate model ID.
    structure_chain : str
        Chain ID.
    entitiy : str
        Structural entity: complex (default), ligand, pocket, protein, or water (only in local module).
    format : str
        File format: mol2 (default) or pdb (only for entity=complex).
    in_dir : bool
        Use KLIFS directory structure (default: False).

    Returns
    -------
    pathlib.Path
        File path.
    """

    path_to_klifs_download = Path(path_to_klifs_download)
    species = species.upper()
    structure_alternate_model = structure_alternate_model.replace("-", "")
    structure_chain = structure_chain.replace("-", "")
    structure = f"{structure_pdb}{f'_alt{structure_alternate_model}' if bool(structure_alternate_model) else ''}{f'_chain{structure_chain}' if bool(structure_chain) else ''}"

    if in_dir:
        path = (
            path_to_klifs_download
            / "KLIFS_download"
            / species
            / kinase_name
            / structure
            / f"{entity}.{format}"
        )
    else:
        path = (
            path_to_klifs_download
            / f"{species}_{kinase_name}_{structure}_{entity}.{format}"
        )

    return path


def _abc_idlist_to_dataframe(abc_idlist):
    """
    Transform ABC IDList object into DataFrame.

    Parameters
    ----------
    abc_idlist : list of acb.IDList
        List of labeled list objects from abstract base classes module.

    Returns
    -------
    pandas.DataFrame
        Table with list labels as column names.
    """

    result = abc_idlist

    keys = list(result[0])

    results_dict = {key: [] for key in keys}

    for result in abc_idlist:
        for key in keys:
            results_dict[key].append(result[key])

    return pd.DataFrame(results_dict)
