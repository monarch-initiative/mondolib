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

## Modules
### QC
This has intentionally bespoke and mondo-unique checks
