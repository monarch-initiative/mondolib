"""Command line interface for mondolib."""
import logging

import click

from mondolib import __version__
from mondolib.main import validate

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


if __name__ == "__main__":
    main()
