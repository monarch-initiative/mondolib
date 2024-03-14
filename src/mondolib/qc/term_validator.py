"""mondolib term-validator."""

import logging
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from linkml_runtime.loaders import yaml_loader
from oaklib import BasicOntologyInterface
from oaklib.types import CURIE

from mondolib.datamodels.mondolib_schema import CandidateObsoletion, Configuration, Report, ValidationCheckScope
from mondolib.datamodels.vocabulary import ORPHANET_PREFIX
from mondolib.utilities.curie_utilities import get_curie_prefix

MAPPING_DICT_BY_SOURCE = Dict[str, str]


@dataclass
class TermValidator:

    """A bespoke Mondo validator."""

    ontology: BasicOntologyInterface = None
    configuration: Configuration = None

    def get_ontology_report(self, threshold: float = 0.0) -> Report:
        """
        Get report from the entire ontology.

        :return:
        """
        report = Report()
        for term in self.ontology.all_entity_curies():
            obs = self.get_candidate_obsoletion(term, threshold=threshold)
            if obs is not None:
                report.candidate_obsoletions[obs.term] = obs
        return report

    def get_candidate_obsoletion(self, term: CURIE, threshold: float = 0.0) -> Optional[CandidateObsoletion]:
        """
        Given a term, yield the reasons why this should be obsoleted.

        If there are no detectable reasons, return None

        :param term:
        :return:
        """
        logging.info(f"Checking {term}")
        oi = self.ontology
        conf = self.configuration
        confidence = 0.0
        label = oi.get_label_by_curie(term)
        if label is None:
            logging.info(f"No name - possible dangling? {term}")
            return None
        obs = CandidateObsoletion(term=term, label=label)
        incoming = oi.incoming_relationship_map(term)
        mdict = self.get_mappings_by_source(term)
        prefixes = list(mdict.keys())

        defn = oi.get_definition_by_curie(term)
        obs.has_definition = defn is not None
        if len(incoming) > 0:
            obs.is_likely_grouping = True
        else:
            confidence -= 1.0
        if obs.has_definition:
            confidence -= 2
        scope = None
        if prefixes == [ORPHANET_PREFIX]:
            scope = ValidationCheckScope(ValidationCheckScope.ORDO_ONLY)
            confidence += 1
        for lp in conf.lexical_patterns:
            if lp.scope == scope:
                if re.match(lp.pattern, label):
                    obs.lexical_pattern_matches.append(lp)
                    confidence += 3
        if confidence > threshold:
            obs.confidence = confidence
            return obs
        else:
            return None

    def load_configuration(self, path: str = None) -> None:
        """
        Load configuration.

        :param path: uses default if not specified
        :return:
        """
        if path is None:
            d = Path(os.path.dirname(sys.modules["mondolib"].__file__))
            path = d / "config" / "qc_config.yaml"
        logging.info(f"Loading from {path}")
        self.configuration = yaml_loader.loads(str(path), Configuration)

    def get_mappings_by_source(self, term: CURIE) -> MAPPING_DICT_BY_SOURCE:
        """Get CURIE mappings."""
        oi = self.ontology
        mapping_dict = defaultdict(list)
        for m in oi.simple_mappings_by_curie(term):
            # ignore mapping predicate for now
            x = m[1]
            mapping_dict[get_curie_prefix(x)].append(x)
        return mapping_dict
