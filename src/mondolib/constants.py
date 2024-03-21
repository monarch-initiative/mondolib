"""Constants used in package."""

from pathlib import Path

ONT_DIR = Path(__file__).resolve().parents[1] / "ontology"
TMP_DIR = Path.joinpath(ONT_DIR, "tmp")
RETAINS_ANCESTOR = "RETAINS_ANCESTOR"
RETAINS_PARENT = "RETAINS_PARENT"
LEAVES_THE_BRANCH = "Leaves the branch"
ORPHANED = "Orphaned"
STAYS_IN_THE_BRANCH = "Stays in branch"
UNDEFINED = "Undefined"
DISEASE = "MONDO:0000001"
HUMAN_DISEASE = "MONDO:0700096"
DISEASE_LABELED = "MONDO:0000001->disease"
HUMAN_DISEASE_LABELED = "MONDO:0700096->human disease"
DISEASES_SET = {DISEASE, HUMAN_DISEASE, DISEASE_LABELED, HUMAN_DISEASE_LABELED}
# Define the column names for the output file
COLUMN_NAMES = [
    "Branch reviewed ID",
    "Children of the obsoletion candidate ID",
    "Children of the obsoletion candidate label",
    "Children of the obsoletion candidate Definition",
    "Parent to be obsoleted",
    "Other direct parents in Branch",
    "Other direct parents NOT in Branch",
    "Ancestor inside the branch",
    "Ancestor outside the branch",
    "AffectedStatus",
]
OBSOLETION_SUFFIX = " - TO_BE_OBSOLETED"
