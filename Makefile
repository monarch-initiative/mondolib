RUN = poetry run

all: pyclasses test_inputs

pyclasses: src/mondolib/datamodels/mondolib_schema.py

src/mondolib/datamodels/%.py: src/mondolib/datamodels/%.yaml
	$(RUN) gen-python $< > $@

tests/input/%.owl: tests/input/%.obo
	robot convert -i $< -o $@

test_inputs: tests/input/example.db
tests/input/%.db: tests/input/%.owl
	$(RUN) semsql make --docker $@

