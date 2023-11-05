"""Main python file."""
import csv
from typing import List, Tuple

import numpy as np
import pandas as pd
from oaklib import get_adapter
from oaklib.datamodels.vocabulary import IS_A, PART_OF

from mondolib.constants import (
    COLUMN_NAMES,
    DISEASES_SET,
    LEAVES_THE_BRANCH,
    OBSOLETION_SUFFIX,
    ORPHANED,
    STAYS_IN_THE_BRANCH,
    UNDEFINED,
)


def demo():
    """Define API."""
    print("Hello, World!")


def validate(input: str, output: str):
    """Validate."""
    df = pd.read_csv(input, sep="\t", index_col=None)
    mondo_df = df.loc[df["subject"].str.startswith("MONDO:")]
    mondo_df.to_csv(output, sep="\t", index=False)


def update():
    """Update ontology file."""
    pass


def create_review_table(branch_id, branch_id_file, obsoletion_candidates_file, output_file, input):
    """
    Generate review table for branch obsoletion.

    :param branch_id: Branch CURIE.
    :param branch_id_file: TSV file listing all branch IDs.
    :param obsoletion_candidates_file: TTSV listing all obsoletion candidate CURIEs
    :param output_file: output filepath.
    :param input: input  ontology resource (Path to local file or slug for oaklib).
    """
    OI = get_adapter(f"sqlite:{input}")
    all_obsoletes = set(OI.obsoletes())

    # Open the TSV file and read it into a list
    with open(obsoletion_candidates_file, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        # Store the first element of each row in the obsoletion_candidates list
        obsoletion_candidates = [row[0] for row in reader]

    # If branch_id is not provided
    if branch_id is None:
        # If a file containing branch_ids is provided
        if branch_id_file:
            with open(branch_id_file, "r") as f:
                reader = csv.reader(f, delimiter="\t")
                # Store the first element of each row in the branch_ids list
                branch_ids = [row[0] for row in reader]
        else:
            # Raise an error if neither branch_id nor branch_id_file is provided
            raise (ValueError("Please provide either `--branch-id` OR `--branch-id-file` to get results."))
    else:
        # If branch_id is provided, store it in a list
        branch_ids = [branch_id]

    # Create a dictionary where each key is a branch_id and the value is a set of its descendants
    branch_descendants_dict = {
        id: set(OI.descendants(start_curies=id, predicates=[IS_A, PART_OF])) for id in branch_ids
    }

    # Open the output file in write mode
    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter="\t")
        # Write the column names to the output file
        writer.writerow(COLUMN_NAMES)

        # Convert the obsoletion_candidates list to a set for faster operations
        obsoletion_candidates_set = set(obsoletion_candidates)

        # Get the relationships of the obsoletion candidates in the current branch
        obsoletion_candidates_children_relationships = list(
            OI.relationships(objects=obsoletion_candidates_set, predicates=[IS_A, PART_OF])
        )

        children_of_obsoletion_candidate = set()
        # For each branch_id
        for branch_id in branch_ids:
            # Get the descendants of the current branch_id
            branch_descendants_set = branch_descendants_dict[branch_id]
            obsoletion_candidate_child_of_branch = branch_descendants_set & obsoletion_candidates_set

            for obsoletion_candidate in obsoletion_candidate_child_of_branch:
                # Column E: Parent to be obsoleted == obsoletion_candidate
                children_of_obsoletion_candidate.update(
                    set(
                        get_immediate_children(
                            curie=obsoletion_candidate,
                            relationships=obsoletion_candidates_children_relationships,
                        )
                    )
                )

            children_of_obsoletion_candidate_parents_relationship = set(
                OI.relationships(
                    subjects=children_of_obsoletion_candidate,
                    predicates=[IS_A, PART_OF],
                )
            )

            children_of_branch_and_obsoletion_candidates = (
                children_of_obsoletion_candidate & obsoletion_candidate_child_of_branch
            )

            for child in children_of_obsoletion_candidate:
                # if branch_id == 'MONDO:0005151' and child == "MONDO:0018808":
                #     import pdb; pdb.set_trace()
                # Column B: Children of ObsoleteCandidate == child
                parents_of_child = (
                    set(
                        get_immediate_parent(
                            curie=child,
                            relationships=children_of_obsoletion_candidate_parents_relationship,
                        )
                    )
                    - all_obsoletes
                )

                # These are parents that need to be obsoleted
                relevant_obsoletion_parents_in_branch = parents_of_child & obsoletion_candidate_child_of_branch
                # if child == "MONDO:0013310":
                #     import pdb; pdb.set_trace()

                # parents_of_child.difference_update(obsoletion_candidate_child_of_branch)

                # Column F: Other direct parents in Branch = other_parents_in_branch
                other_parents_in_branch = parents_of_child & branch_descendants_set

                # Column G: Other direct parents NOT in Branch = other_parents_not_in_branch
                other_parents_not_in_branch = parents_of_child - other_parents_in_branch

                all_ancestors = (
                    set(OI.ancestors([child], predicates=[IS_A, PART_OF], method="ENTAILMENT"))
                    # - parents_of_child
                    - {child}
                )
                all_ancestors = {anc for anc in all_ancestors if str(anc).startswith("MONDO:")}

                # all_ancestors.difference_update(obsoletion_candidate_child_of_branch)

                # Column H: Ancestor inside the branch = all_mondo_ancestors_in_branch
                all_ancestors_in_branch = all_ancestors & branch_descendants_set

                # Column I: Ancestor outside the branch = all_mondo_ancestors_outside_branch
                all_ancestors_outside_branch = all_ancestors - all_ancestors_in_branch

                # if child == "MONDO:0013310":
                #     import pdb; pdb.set_trace()

                other_parents_in_branch = add_obsoleted_label(other_parents_in_branch, obsoletion_candidates_set)
                other_parents_not_in_branch = add_obsoleted_label(
                    other_parents_not_in_branch, obsoletion_candidates_set
                )
                all_ancestors_in_branch = add_obsoleted_label(all_ancestors_in_branch, obsoletion_candidates_set)
                all_ancestors_outside_branch = add_obsoleted_label(
                    all_ancestors_outside_branch, obsoletion_candidates_set
                )
                relevant_obsoletion_parents_in_branch = add_obsoleted_label(
                    relevant_obsoletion_parents_in_branch, obsoletion_candidates_set
                )

                # Convert the sets to strings for writing to the output file
                other_parents_in_branch_list = stringify(other_parents_in_branch, OI)
                other_parents_not_in_branch_list = stringify(other_parents_not_in_branch, OI)
                all_mondo_ancestors_in_branch_list = stringify(all_ancestors_in_branch, OI)
                all_mondo_ancestors_outside_branch_list = stringify(all_ancestors_outside_branch, OI)
                relevant_obsoletion_parents_list = stringify(relevant_obsoletion_parents_in_branch, OI)
                # parents_of_child_list = stringify(parents_of_child)

                child_label = OI.label(child)
                child_defn = OI.definition(child)
                if child in children_of_branch_and_obsoletion_candidates:
                    child = add_obsoleted_label({child}, obsoletion_candidates_set).pop()

                data = [
                    branch_id,
                    child,
                    child_label,
                    child_defn,
                    relevant_obsoletion_parents_list,
                    other_parents_in_branch_list,
                    other_parents_not_in_branch_list,
                    all_mondo_ancestors_in_branch_list,
                    all_mondo_ancestors_outside_branch_list,
                    "",
                ]

                writer.writerow(data)  # writing the data


def get_immediate_parent(curie: str, relationships: List[Tuple[str]]):
    """Get immediate parents of CURIE passed."""
    return [t[2] for t in relationships if t[0] == curie and t[1] in [IS_A, PART_OF]]


def get_immediate_children(curie: str, relationships: List[Tuple[str]]):
    """Get immediate children of CURIE passed."""
    return [t[0] for t in relationships if t[2] == curie and t[1] in [IS_A, PART_OF]]


def add_obsoleted_label(all_ancestors, obsoletion_candidates_set):
    """Tag all terms that are obsolete candidates."""
    return {
        ancestor + OBSOLETION_SUFFIX if ancestor in obsoletion_candidates_set else ancestor
        for ancestor in all_ancestors
    }


def stringify(item: List[Tuple], OI):
    """Take in a list, add OBSLETION_SUFFIXes wherever appropriate and list => string."""
    # Create a dictionary with obsolete items as keys and normalized items as values
    normalized_obsolete_items_dict = {i: i.replace(OBSOLETION_SUFFIX, "") for i in item if OBSOLETION_SUFFIX in i}

    # Update item list by replacing obsolete items with their normalized versions
    item = [normalized_obsolete_items_dict.get(i, i) for i in item]

    labeled_terms = list(OI.labels(item)) if OI.labels(item) is not None else []

    obsolete_added_label_terms = []

    # Iterate over labeled_terms list
    for term in labeled_terms:
        # If the term[0] exists as a key in the dictionary
        if term[0] in normalized_obsolete_items_dict.values():
            # Replace the term with the corresponding value from the dictionary
            key = [k for k in normalized_obsolete_items_dict.keys() if term[0] in k][0]
            obsolete_added_label_terms.append((key, term[1]))
        else:
            obsolete_added_label_terms.append(term)

    result = " | ".join("->".join(map(str, t)) for t in obsolete_added_label_terms)
    return result


def relax_and_reason(input, obsoletion_candidates_file, output_file, relaxed_resource):
    """
    Take in `robot relax`ed source and given `robot reason`ed (same source), write output.

    :param input: Resource filepath.
    :param obsoletion_candidates_file: TSV file listign obsoletion candidate CURIEs.
    :param output_file: Output file path to write results.
    :param relaxed_resource: File path for `robot relax` output.
    """
    df_reasoned = pd.read_csv(input[0], sep="\t", low_memory=False).fillna("")
    df_relaxed = pd.read_csv(input[1], sep="\t", low_memory=False).fillna("")
    df_uncommon: pd.DataFrame = pd.DataFrame(columns=COLUMN_NAMES)

    for row in df_relaxed.iterrows():
        branch_id = row[1][COLUMN_NAMES[0]]
        child_id = row[1][COLUMN_NAMES[1]]

        (
            relevant_obsoletion_parents_list_1,
            other_parents_in_branch_list_1,
            other_parents_not_in_branch_list_1,
            all_mondo_ancestors_in_branch_list_1,
            all_mondo_ancestors_outside_branch_list_1,
        ) = get_columns_as_sets(row[1])

        condition_1 = df_reasoned[COLUMN_NAMES[0]] == branch_id
        condition_2 = df_reasoned[COLUMN_NAMES[1]] == child_id
        corresp_row_df_reasoned = df_reasoned.loc[condition_1 & condition_2]
        if not corresp_row_df_reasoned.empty:
            relevant_obsoletion_parents_list_2 = (
                {x.strip() for x in str(corresp_row_df_reasoned[COLUMN_NAMES[4]].values[0]).split("|")}
                if row[1][COLUMN_NAMES[4]] != np.NAN
                else set()
            )

            other_parents_in_branch_list_2 = (
                {x.strip() for x in str(corresp_row_df_reasoned[COLUMN_NAMES[5]].values[0]).split("|")}
                if row[1][COLUMN_NAMES[5]] != np.NAN
                else set()
            )

            other_parents_not_in_branch_list_2 = (
                {x.strip() for x in str(corresp_row_df_reasoned[COLUMN_NAMES[6]].values[0]).split("|")}
                if row[1][COLUMN_NAMES[6]] != np.NAN
                else set()
            )

            all_mondo_ancestors_in_branch_list_2 = (
                {x.strip() for x in str(corresp_row_df_reasoned[COLUMN_NAMES[7]].values[0]).split("|")}
                if row[1][COLUMN_NAMES[7]] != np.NAN
                else set()
            )

            all_mondo_ancestors_outside_branch_list_2 = (
                {x.strip() for x in str(corresp_row_df_reasoned[COLUMN_NAMES[8]].values[0]).split("|")}
                if row[1][COLUMN_NAMES[8]] != np.NAN
                else set()
            )

            relevant_obsoletion_parents_list_merged = (relevant_obsoletion_parents_list_1 or set()) | (
                relevant_obsoletion_parents_list_2 or set()
            )

            other_parents_in_branch_list_merged = (other_parents_in_branch_list_1 or set()) | (
                other_parents_in_branch_list_2 or set()
            )
            other_parents_not_in_branch_list_merged = (other_parents_not_in_branch_list_1 or set()) | (
                other_parents_not_in_branch_list_2 or set()
            )
            all_mondo_ancestors_in_branch_list_merged = (all_mondo_ancestors_in_branch_list_1 or set()) | (
                all_mondo_ancestors_in_branch_list_2 or set()
            )
            all_mondo_ancestors_outside_branch_list_merged = (all_mondo_ancestors_outside_branch_list_1 or set()) | (
                all_mondo_ancestors_outside_branch_list_2 or set()
            )
            df_reasoned.loc[
                corresp_row_df_reasoned.index,
                [
                    COLUMN_NAMES[4],
                    COLUMN_NAMES[5],
                    COLUMN_NAMES[6],
                    COLUMN_NAMES[7],
                    COLUMN_NAMES[8],
                ],
            ] = [
                " | ".join(relevant_obsoletion_parents_list_merged),
                " | ".join(other_parents_in_branch_list_merged),
                " | ".join(other_parents_not_in_branch_list_merged),
                " | ".join(all_mondo_ancestors_in_branch_list_merged),
                " | ".join(all_mondo_ancestors_outside_branch_list_merged),
            ]

            status = get_status(
                other_parents_in_branch_list_merged,
                other_parents_not_in_branch_list_merged,
            )
            df_reasoned.loc[corresp_row_df_reasoned.index, COLUMN_NAMES[9]] = status
        else:
            row_df = row[1].to_frame().T
            row_df[COLUMN_NAMES[9]] = get_status(other_parents_in_branch_list_1, other_parents_not_in_branch_list_1)
            df_uncommon = df_uncommon._append(row_df, ignore_index=True)

    df_reasoned_no_status = df_reasoned[df_reasoned[COLUMN_NAMES[9]] == ""]
    # ! Call add_status on rows that were in df_reasoned but not in df_relaxed
    df_reasoned_added_status = add_status_and_update_parents(
        df_reasoned_no_status, relaxed_resource, obsoletion_candidates_file
    )
    df_reasoned_with_status = df_reasoned[df_reasoned[COLUMN_NAMES[9]] != ""]

    result_df = pd.concat(
        [df_reasoned_added_status, df_reasoned_with_status, df_uncommon],
        axis=0,
        ignore_index=True,
    ).reset_index(drop=True)
    result_df = result_df.drop_duplicates().fillna("")
    result_df.to_csv(output_file, sep="\t", index=False)


def add_status_and_update_parents(df: pd.DataFrame, resource: str, obsoletion_candidates_file: str) -> pd.DataFrame:
    """
    Add status based on `robot reason`ed output.

    The Dataframe that is passed here are rows present from the reasoned table
    and that are absent in the relaxed table. The 2 ancestor columns had CURIEs
    missing and thus we get them from oaklib eithout obsoletion terms inolved.

    Spreadsheet explaining this:
    https://docs.google.com/spreadsheets/d/1fbHJAbrq4gDbUX3wg92AuLyqTWKPr_IR-ew6LHuWoMc/edit#gid=0
    """
    OI = get_adapter(f"sqlite:{resource}")
    branch_ids = df[COLUMN_NAMES[0]].unique().tolist()
    child_ids = set(df[COLUMN_NAMES[1]].unique().tolist())
    # Create a dictionary where each key is a branch_id and the value is a set of its descendants
    branch_descendants_dict = {
        id: set(OI.descendants(start_curies=id, predicates=[IS_A, PART_OF])) for id in branch_ids
    }

    # Open the TSV file and read it into a list
    with open(obsoletion_candidates_file, "r") as f:
        reader = csv.reader(f, delimiter="\t")
        # Store the first element of each row in the obsoletion_candidates list
        obsoletion_candidates_set = set([row[0] for row in reader])

    parents_relationship_of_children = set(
        OI.relationships(
            subjects=child_ids,
            predicates=[IS_A, PART_OF],
        )
    )

    for idx, row in df.iterrows():
        (
            _,
            other_parents_in_branch,
            other_parents_not_in_branch,
            _,
            _,
        ) = get_columns_as_sets(row)
        branch_id = row[COLUMN_NAMES[0]]
        child_id = row[COLUMN_NAMES[1]]
        parents_of_child = set(
            get_immediate_parent(
                curie=child_id,
                relationships=parents_relationship_of_children,
            )
        )
        branch_descendants_set = branch_descendants_dict[branch_id]
        parents_in_branch = parents_of_child & branch_descendants_set
        parents_not_in_branch = parents_of_child - parents_in_branch

        # ! Since this part of the code uses the relaxed resource,
        # ! The branch descendants may not contain some parents.
        # ! This extra hack is to avoid ambiguity and confusion in the results
        # ! which shows parents in branch previously to also appear out of branch.
        # Check each item in the set
        for item in list(parents_not_in_branch):
            # If the item is in the string, discard it from the set
            if item in row[COLUMN_NAMES[5]]:
                parents_not_in_branch.discard(item)
        parents_in_branch_absent = {
            parent
            for parent in parents_in_branch
            if all(parent not in other_parent for other_parent in other_parents_in_branch)
        }
        parents_not_in_branch_absent = {
            parent
            for parent in parents_not_in_branch
            if all(parent not in other_parent for other_parent in other_parents_not_in_branch)
        }

        parents_in_branch_absent = add_obsoleted_label(parents_in_branch_absent, obsoletion_candidates_set)

        new_column_5 = f"{row[COLUMN_NAMES[5]]} | {stringify(parents_in_branch_absent, OI)}".strip(" | ")

        parents_not_in_branch_absent = add_obsoleted_label(parents_not_in_branch_absent, obsoletion_candidates_set)

        new_column_6 = f"{row[COLUMN_NAMES[6]]} | {stringify(parents_not_in_branch_absent, OI)}".strip(" | ")

        df.loc[idx, [COLUMN_NAMES[5], COLUMN_NAMES[6], COLUMN_NAMES[9]]] = [
            new_column_5,
            new_column_6,
            get_status(
                (other_parents_in_branch | parents_in_branch_absent),
                (other_parents_not_in_branch | parents_not_in_branch_absent),
            ),
        ]

    return df


def get_columns_as_sets(row):
    """Return each column of a row as a set of CURIEs."""
    relevant_obsoletion_parents_list_1 = (
        {x.strip() for x in str(row[COLUMN_NAMES[4]]).split("|")} if row[COLUMN_NAMES[4]] != np.NAN else set()
    )

    other_parents_in_branch_list_1 = (
        {x.strip() for x in str(row[COLUMN_NAMES[5]]).split("|")} if row[COLUMN_NAMES[5]] != np.NAN else set()
    )

    other_parents_not_in_branch_list_1 = (
        {x.strip() for x in str(row[COLUMN_NAMES[6]]).split("|")} if row[COLUMN_NAMES[6]] != np.NAN else set()
    )
    all_mondo_ancestors_in_branch_list_1 = (
        {x.strip() for x in str(row[COLUMN_NAMES[7]]).split("|")} if row[COLUMN_NAMES[7]] != np.NAN else set()
    )
    all_mondo_ancestors_outside_branch_list_1 = (
        {x.strip() for x in str(row[COLUMN_NAMES[8]]).split("|")} if row[COLUMN_NAMES[8]] != np.NAN else set()
    )

    return (
        relevant_obsoletion_parents_list_1,
        other_parents_in_branch_list_1,
        other_parents_not_in_branch_list_1,
        all_mondo_ancestors_in_branch_list_1,
        all_mondo_ancestors_outside_branch_list_1,
    )


def get_status(
    other_parents_in_branch_list_merged: set,
    other_parents_not_in_branch_list_merged: set,
):
    """Set the status of obsoletion."""
    # Column J: Affected Status = status
    status = ""
    other_parents_in_branch_list_merged.discard("")
    other_parents_not_in_branch_list_merged.discard("")

    if len(other_parents_in_branch_list_merged) > 0 and any(
        " - TO_BE_OBSOLETED" not in parent for parent in other_parents_in_branch_list_merged
    ):
        status = STAYS_IN_THE_BRANCH
    elif (
        len(other_parents_in_branch_list_merged) == 0
        or all(" - TO_BE_OBSOLETED" in parent for parent in other_parents_in_branch_list_merged)
    ) and (
        len(other_parents_not_in_branch_list_merged - DISEASES_SET) > 0
        and any(
            " - TO_BE_OBSOLETED" not in parent for parent in (other_parents_not_in_branch_list_merged - DISEASES_SET)
        )
    ):
        status = LEAVES_THE_BRANCH
    elif (
        len(other_parents_in_branch_list_merged) == 0
        or all(" - TO_BE_OBSOLETED" in parent for parent in other_parents_in_branch_list_merged)
    ) and (
        len(other_parents_not_in_branch_list_merged - DISEASES_SET) == 0
        or all(" - TO_BE_OBSOLETED" in parent for parent in other_parents_not_in_branch_list_merged - DISEASES_SET)
    ):
        status = ORPHANED
    else:
        status = UNDEFINED

    return status


if __name__ == "__main__":
    demo()
