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

# *======|=|=||================
tmp/mondo_edit.obo:
	wget -O tmp/mondo_edit.obo https://raw.githubusercontent.com/monarch-initiative/mondo/master/src/ontology/mondo-edit.obo 

tmp/mondo.owl: tmp/mondo_edit.obo
	robot convert -i $< --output $@

tmp/mondo-relaxed-branchreview.owl: tmp/mondo_edit.obo
	robot merge -i $< -i $< relax -o $@

tmp/mondo-reasoned-branchreview.owl: tmp/mondo_edit.obo
	robot merge -i $< -i $< reason -o $@

tmp/mondo%.db: tmp/mondo%.owl
	$(RUN) semsql make $@
	rm -f .template.db
	rm -f tmp/mondo-relation-graph.tsv.gz

tmp/mondo_lexmatch.sssom.tsv: tmp/mondo.db
	$(RUN) runoak -i sqlite:$< lexmatch -o $@ -R $(RULES_FILE) --ensure-strict-prefixes

tmp/mondo_validate_full.tsv: tmp/mondo.db
	$(RUN) runoak -i sqlite:$< validate -o $@

tmp/mondo_validate.tsv: tmp/mondo_validate_full.tsv
	$(RUN) mondoqc validate $< -o $@

obsoletion-tables: tmp/mondo-relaxed-branchreview.db  tmp/mondo-reasoned-branchreview.db
	for id in $(shell cat src/mondolib/config/branch_ids.tsv); do \
        $(RUN) mondoqc create-review-table -i tmp/mondo-reasoned-branchreview.db -o tmp/mondo-reasoned-branch-$$id-review.tsv -f src/mondolib/config/obsoletion_terms.tsv -b $$id;\
		$(RUN) mondoqc create-review-table -i tmp/mondo-relaxed-branchreview.db -o tmp/mondo-relaxed-branch-$$id-review.tsv -f src/mondolib/config/config/obsoletion_terms.tsv -b $$id;\
		$(RUN) mondoqc relax-and-reason -i tmp/mondo-reasoned-branch-$$id-review.tsv -i tmp/mondo-relaxed-branch-$$id-review.tsv -r tmp/mondo-relaxed-branchreview.db   -f src/mondolib/config/obsoletion_terms.tsv -o reports/mondo-combined-branch-$$id-review.tsv;\
    done

lexmatch: tmp/mondo_lexmatch.sssom.tsv
validate: tmp/mondo_validate.tsv

clear-tmp:
	rm -rf tmp/*