"""Command line interface for mondolib."""
import logging

import click

from mondolib import __version__
from mondolib.main import create_review_table, relax_and_reason, validate

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet")
@click.version_option(__version__)
def main(verbose: int, quiet: bool):
    """
    CLI for mondolib.

    :param verbose: Verbosity while running.
    :param quiet: Boolean to be quiet or verbose.
    """
    if verbose >= 2:
        logger.setLevel(level=logging.DEBUG)
    elif verbose == 1:
        logger.setLevel(level=logging.INFO)
    else:
        logger.setLevel(level=logging.WARNING)
    if quiet:
        logger.setLevel(level=logging.ERROR)


@main.command("validate")
@click.argument("input")
@click.option("-o", "--output", help="Output file path")
def click_validate(input: str, output: str):
    """Run the mondolib's demo command."""
    validate(input, output)


@main.command("create-review-table")
@click.option("-i", "--input", help="DB source file.")
@click.option("-b", "--branch-id", help="Branch ID")
@click.option("-B", "--branch-id-file", help="TSV with one column of obsoletion CURIEs")
@click.option(
    "-f",
    "--obsoletion-candidates-file",
    help="TSV with one column of obsoletion CURIEs",
)
@click.option("-o", "--output-file", help="Path to report file")
def click_create_review_table(branch_id, branch_id_file, obsoletion_candidates_file, output_file, input):
    """Create review table."""
    create_review_table(branch_id, branch_id_file, obsoletion_candidates_file, output_file, input)


@main.command("relax-and-reason")
@click.option("-i", "--input", help="branch review files to be combined.", multiple=True)
@click.option(
    "-f",
    "--obsoletion-candidates-file",
    help="TSV with one column of obsoletion CURIEs",
)
@click.option("-o", "--output-file", help="Path to report file")
@click.option("-r", "--relaxed-resource", help="DB source file.")
def click_relax_and_reason(input, obsoletion_candidates_file, output_file, relaxed_resource):
    """Create final output takinf `reason` and `relax` output of resource via robot."""
    relax_and_reason(input, obsoletion_candidates_file, output_file, relaxed_resource)


if __name__ == "__main__":
    main()
