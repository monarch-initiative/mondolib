"""mondolib QC test: test validator."""

import unittest

from linkml_runtime.dumpers import yaml_dumper
from mondolib.qc.term_validator import TermValidator
from oaklib.selector import get_implementation_from_shorthand

from tests import INPUT_DIR


class TermValidatorTestCase(unittest.TestCase):

    """Tests for term validator."""

    def setUp(self) -> None:
        """Set up."""
        tv = TermValidator()
        tv.load_configuration()
        self.term_validator = tv
        tv.ontology = get_implementation_from_shorthand(str(INPUT_DIR / "example.db"))

    def test_qc(self):
        """QC test."""
        tv = self.term_validator
        report = tv.get_ontology_report(threshold=-10)
        print(yaml_dumper.dumps(report))
        print(type(report.candidate_obsoletions))
        print(list(report.candidate_obsoletions.keys()))
        dysostosis = report.candidate_obsoletions["MONDO:0800075"]
        self.assertIsNotNone(dysostosis)
        self.assertGreater(dysostosis.confidence, 1.0)
        self.assertGreater(len(dysostosis.lexical_pattern_matches), 0)


if __name__ == "__main__":
    unittest.main()
