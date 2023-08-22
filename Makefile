RUN = poetry run
RULES_FILE = src/mondolib/config/mondo-match-rules.yaml

all: pyclasses test_inputs

pyclasses: src/mondolib/datamodels/mondolib_schema.py

src/mondolib/datamodels/%.py: src/mondolib/datamodels/%.yaml
	$(RUN) gen-python $< > $@

tests/input/%.owl: tests/input/%.obo
	robot convert -i $< -o $@

test_inputs: tests/input/example.db
tests/input/%.db: tests/input/%.owl
	$(RUN) semsql make --docker $@

# *========================
tmp/mondo_edit.obo:
	wget -O tmp/mondo_edit.obo https://raw.githubusercontent.com/monarch-initiative/mondo/master/src/ontology/mondo-edit.obo 

tmp/mondo.owl: tmp/mondo_edit.obo
	robot convert -i $< --output $@

tmp/mondo.db:
	semsql make $@
	rm .template.db

tmp/mondo_lexmatch.sssom.tsv: tmp/mondo.db
	runoak -i sqlite:$< lexmatch -o $@ -R $(RULES_FILE)

tmp/mondo_validate.tsv: tmp/mondo.db
	runoak -i sqlite:$< validate -o $@

lexmatch: tmp/mondo_lexmatch.sssom.tsv
validate: tmp/mondo_validate.tsv