# mondolib
Python library for Mondo.

## Prerequisites
**1. OAK**
Currently in order to understand how to use or code with this library you should understand the basics of [OAK](https://incatools.github.io/ontology-access-kit/)

**2. Inputs**
The intended input of this lib is generally the editors file.

We recommend that this is converted into sqlite first for speed

```
robot convert -i mondo-edit.obo -o mondo-edit.owl
poetry run semsql make --docker mondo-edit.db
```

See the Makefile and tests/input for an example file

## Installation

No PyPI yet

from this repo, do a 

```
poetry install
```

If Poetry is not already installed, follow these instructions:
- create a virual environment ([venv](https://docs.python.org/3/library/venv.html#creating-virtual-environments) or [conda](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands))
- activate the virtual environment
- run `pipx install poetry`
    - install `pipx` (as needed) following these [details](https://pipx.pypa.io/stable/installation/)
- clone the `mondolib` repo
- run `poetry install` from within `mondolib` directory
Note: this repo is known to work with Python 3.9 (and may also work with 3.10 or 3.11 or 3.12) as of 13-Mar-2024.


## Modules
### QC
This has intentionally bespoke and mondo-unique checks
