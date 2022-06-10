# Auto generated from mondolib_schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-06-10T11:39:26
# Schema: mondolib_schema
#
# id: https://purl.obolibrary.org/obo/mondo/schema
# description: A schema that is used by mondolib, primarily for bespoke Mondo QC
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, Float, String
from linkml_runtime.utils.metamodelcore import Bool

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
MONDOLIB = CurieNamespace('mondolib', 'https://purl.obolibrary.org/obo/mondo/schema/')
DEFAULT_ = MONDOLIB


# Types

# Class references
class CandidateObsoletionTerm(extended_str):
    pass


@dataclass
class LexicalPattern(YAMLRoot):
    """
    A lexical pattern that is matched against labels
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MONDOLIB.LexicalPattern
    class_class_curie: ClassVar[str] = "mondolib:LexicalPattern"
    class_name: ClassVar[str] = "LexicalPattern"
    class_model_uri: ClassVar[URIRef] = MONDOLIB.LexicalPattern

    pattern: Optional[str] = None
    description: Optional[str] = None
    obsoletion_reason: Optional[str] = None
    scope: Optional[Union[str, "ValidationCheckScope"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.pattern is not None and not isinstance(self.pattern, str):
            self.pattern = str(self.pattern)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.obsoletion_reason is not None and not isinstance(self.obsoletion_reason, str):
            self.obsoletion_reason = str(self.obsoletion_reason)

        if self.scope is not None and not isinstance(self.scope, ValidationCheckScope):
            self.scope = ValidationCheckScope(self.scope)

        super().__post_init__(**kwargs)


@dataclass
class Configuration(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MONDOLIB.Configuration
    class_class_curie: ClassVar[str] = "mondolib:Configuration"
    class_name: ClassVar[str] = "Configuration"
    class_model_uri: ClassVar[URIRef] = MONDOLIB.Configuration

    lexical_patterns: Optional[Union[Union[dict, LexicalPattern], List[Union[dict, LexicalPattern]]]] = empty_list()
    exclude_terms_with_definitions: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.lexical_patterns, list):
            self.lexical_patterns = [self.lexical_patterns] if self.lexical_patterns is not None else []
        self.lexical_patterns = [v if isinstance(v, LexicalPattern) else LexicalPattern(**as_dict(v)) for v in self.lexical_patterns]

        if self.exclude_terms_with_definitions is not None and not isinstance(self.exclude_terms_with_definitions, Bool):
            self.exclude_terms_with_definitions = Bool(self.exclude_terms_with_definitions)

        super().__post_init__(**kwargs)


@dataclass
class CandidateObsoletion(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MONDOLIB.CandidateObsoletion
    class_class_curie: ClassVar[str] = "mondolib:CandidateObsoletion"
    class_name: ClassVar[str] = "CandidateObsoletion"
    class_model_uri: ClassVar[URIRef] = MONDOLIB.CandidateObsoletion

    term: Union[str, CandidateObsoletionTerm] = None
    label: Optional[str] = None
    confidence: Optional[float] = None
    is_ordo_only: Optional[Union[bool, Bool]] = None
    lexical_pattern_matches: Optional[Union[Union[dict, LexicalPattern], List[Union[dict, LexicalPattern]]]] = empty_list()
    direct_child_terms: Optional[Union[str, List[str]]] = empty_list()
    is_likely_grouping: Optional[Union[bool, Bool]] = None
    has_definition: Optional[Union[bool, Bool]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.term):
            self.MissingRequiredField("term")
        if not isinstance(self.term, CandidateObsoletionTerm):
            self.term = CandidateObsoletionTerm(self.term)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.confidence is not None and not isinstance(self.confidence, float):
            self.confidence = float(self.confidence)

        if self.is_ordo_only is not None and not isinstance(self.is_ordo_only, Bool):
            self.is_ordo_only = Bool(self.is_ordo_only)

        if not isinstance(self.lexical_pattern_matches, list):
            self.lexical_pattern_matches = [self.lexical_pattern_matches] if self.lexical_pattern_matches is not None else []
        self.lexical_pattern_matches = [v if isinstance(v, LexicalPattern) else LexicalPattern(**as_dict(v)) for v in self.lexical_pattern_matches]

        if not isinstance(self.direct_child_terms, list):
            self.direct_child_terms = [self.direct_child_terms] if self.direct_child_terms is not None else []
        self.direct_child_terms = [v if isinstance(v, str) else str(v) for v in self.direct_child_terms]

        if self.is_likely_grouping is not None and not isinstance(self.is_likely_grouping, Bool):
            self.is_likely_grouping = Bool(self.is_likely_grouping)

        if self.has_definition is not None and not isinstance(self.has_definition, Bool):
            self.has_definition = Bool(self.has_definition)

        super().__post_init__(**kwargs)


@dataclass
class Report(YAMLRoot):
    """
    A pan-ontology report. This focuses on bespoke Mondo checks rather than generic OBO checks
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = MONDOLIB.Report
    class_class_curie: ClassVar[str] = "mondolib:Report"
    class_name: ClassVar[str] = "Report"
    class_model_uri: ClassVar[URIRef] = MONDOLIB.Report

    candidate_obsoletions: Optional[Union[Dict[Union[str, CandidateObsoletionTerm], Union[dict, CandidateObsoletion]], List[Union[dict, CandidateObsoletion]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_dict(slot_name="candidate_obsoletions", slot_type=CandidateObsoletion, key_name="term", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations
class ValidationCheckScope(EnumDefinitionImpl):
    """
    Some validations are only performed in particular contexts or scopes
    """
    ORDO_ONLY = PermissibleValue(text="ORDO_ONLY",
                                         description="A scope in which the term is mapped solely to Ordo/Orphanet, and there are no mappings to other ontologies, and there have been no non-ORDO axioms added")

    _defn = EnumDefinition(
        name="ValidationCheckScope",
        description="Some validations are only performed in particular contexts or scopes",
    )

# Slots
class slots:
    pass

slots.lexicalPattern__pattern = Slot(uri=MONDOLIB.pattern, name="lexicalPattern__pattern", curie=MONDOLIB.curie('pattern'),
                   model_uri=MONDOLIB.lexicalPattern__pattern, domain=None, range=Optional[str])

slots.lexicalPattern__description = Slot(uri=MONDOLIB.description, name="lexicalPattern__description", curie=MONDOLIB.curie('description'),
                   model_uri=MONDOLIB.lexicalPattern__description, domain=None, range=Optional[str])

slots.lexicalPattern__obsoletion_reason = Slot(uri=MONDOLIB.obsoletion_reason, name="lexicalPattern__obsoletion_reason", curie=MONDOLIB.curie('obsoletion_reason'),
                   model_uri=MONDOLIB.lexicalPattern__obsoletion_reason, domain=None, range=Optional[str])

slots.lexicalPattern__scope = Slot(uri=MONDOLIB.scope, name="lexicalPattern__scope", curie=MONDOLIB.curie('scope'),
                   model_uri=MONDOLIB.lexicalPattern__scope, domain=None, range=Optional[Union[str, "ValidationCheckScope"]])

slots.configuration__lexical_patterns = Slot(uri=MONDOLIB.lexical_patterns, name="configuration__lexical_patterns", curie=MONDOLIB.curie('lexical_patterns'),
                   model_uri=MONDOLIB.configuration__lexical_patterns, domain=None, range=Optional[Union[Union[dict, LexicalPattern], List[Union[dict, LexicalPattern]]]])

slots.configuration__exclude_terms_with_definitions = Slot(uri=MONDOLIB.exclude_terms_with_definitions, name="configuration__exclude_terms_with_definitions", curie=MONDOLIB.curie('exclude_terms_with_definitions'),
                   model_uri=MONDOLIB.configuration__exclude_terms_with_definitions, domain=None, range=Optional[Union[bool, Bool]])

slots.candidateObsoletion__term = Slot(uri=MONDOLIB.term, name="candidateObsoletion__term", curie=MONDOLIB.curie('term'),
                   model_uri=MONDOLIB.candidateObsoletion__term, domain=None, range=URIRef)

slots.candidateObsoletion__label = Slot(uri=MONDOLIB.label, name="candidateObsoletion__label", curie=MONDOLIB.curie('label'),
                   model_uri=MONDOLIB.candidateObsoletion__label, domain=None, range=Optional[str])

slots.candidateObsoletion__confidence = Slot(uri=MONDOLIB.confidence, name="candidateObsoletion__confidence", curie=MONDOLIB.curie('confidence'),
                   model_uri=MONDOLIB.candidateObsoletion__confidence, domain=None, range=Optional[float])

slots.candidateObsoletion__is_ordo_only = Slot(uri=MONDOLIB.is_ordo_only, name="candidateObsoletion__is_ordo_only", curie=MONDOLIB.curie('is_ordo_only'),
                   model_uri=MONDOLIB.candidateObsoletion__is_ordo_only, domain=None, range=Optional[Union[bool, Bool]])

slots.candidateObsoletion__lexical_pattern_matches = Slot(uri=MONDOLIB.lexical_pattern_matches, name="candidateObsoletion__lexical_pattern_matches", curie=MONDOLIB.curie('lexical_pattern_matches'),
                   model_uri=MONDOLIB.candidateObsoletion__lexical_pattern_matches, domain=None, range=Optional[Union[Union[dict, LexicalPattern], List[Union[dict, LexicalPattern]]]])

slots.candidateObsoletion__direct_child_terms = Slot(uri=MONDOLIB.direct_child_terms, name="candidateObsoletion__direct_child_terms", curie=MONDOLIB.curie('direct_child_terms'),
                   model_uri=MONDOLIB.candidateObsoletion__direct_child_terms, domain=None, range=Optional[Union[str, List[str]]])

slots.candidateObsoletion__is_likely_grouping = Slot(uri=MONDOLIB.is_likely_grouping, name="candidateObsoletion__is_likely_grouping", curie=MONDOLIB.curie('is_likely_grouping'),
                   model_uri=MONDOLIB.candidateObsoletion__is_likely_grouping, domain=None, range=Optional[Union[bool, Bool]])

slots.candidateObsoletion__has_definition = Slot(uri=MONDOLIB.has_definition, name="candidateObsoletion__has_definition", curie=MONDOLIB.curie('has_definition'),
                   model_uri=MONDOLIB.candidateObsoletion__has_definition, domain=None, range=Optional[Union[bool, Bool]])

slots.report__candidate_obsoletions = Slot(uri=MONDOLIB.candidate_obsoletions, name="report__candidate_obsoletions", curie=MONDOLIB.curie('candidate_obsoletions'),
                   model_uri=MONDOLIB.report__candidate_obsoletions, domain=None, range=Optional[Union[Dict[Union[str, CandidateObsoletionTerm], Union[dict, CandidateObsoletion]], List[Union[dict, CandidateObsoletion]]]])
