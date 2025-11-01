"""Tests for Phase 2 onboarding features."""

import unittest
from pathlib import Path
from code_analyzer.models import ModuleInfo, FunctionInfo, ClassInfo, Issue, IssueSeverity
from code_analyzer.architecture_diagrams import ArchitectureDiagramGenerator, format_architecture_diagrams
from code_analyzer.troubleshooting import TroubleshootingPlaybook, format_troubleshooting_playbook
from code_analyzer.glossary import GlossaryGenerator, format_glossary
from code_analyzer.edge_cases import EdgeCaseAnalyzer, format_edge_cases


class TestArchitectureDiagrams(unittest.TestCase):
    """Test architecture diagram generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = ArchitectureDiagramGenerator()
        
        # Create sample modules
        self.modules = [
            ModuleInfo(
                name="api",
                file_path="/test/api.py",
                lines_of_code=100,
                imports=["flask", "models"],
                classes=[],
                functions=[
                    FunctionInfo(name="handle_request", complexity=5, parameters=["req"], returns="Response", docstring="Handle API request")
                ]
            ),
            ModuleInfo(
                name="models",
                file_path="/test/models.py",
                lines_of_code=200,
                imports=["sqlalchemy"],
                classes=[
                    ClassInfo(name="User", methods=[], line_start=1, line_end=50, docstring="User model")
                ],
                functions=[]
            ),
            ModuleInfo(
                name="utils",
                file_path="/test/utils.py",
                lines_of_code=50,
                imports=[],
                classes=[],
                functions=[
                    FunctionInfo(name="format_date", complexity=2, parameters=["date"], returns="str", docstring="")
                ]
            )
        ]
    
    def test_categorize_modules(self):
        """Test module categorization into layers."""
        layers = self.generator._categorize_modules(self.modules)
        
        self.assertIn("api", layers["presentation"])
        self.assertIn("models", layers["domain"])
        self.assertIn("utils", layers["utilities"])
    
    def test_generate_layered_architecture(self):
        """Test layered architecture diagram generation."""
        diagram = self.generator.generate_layered_architecture(self.modules)
        
        self.assertIsInstance(diagram, list)
        self.assertTrue(len(diagram) > 0)
        self.assertIn("LAYERED ARCHITECTURE", diagram[0])
    
    def test_format_architecture_diagrams(self):
        """Test formatting of architecture diagrams."""
        output = format_architecture_diagrams(self.modules)
        
        self.assertIn("ARCHITECTURE DIAGRAMS", output)
        self.assertIn("LAYERED ARCHITECTURE", output)
        self.assertIn("🖥️", output)  # Presentation layer emoji


class TestTroubleshootingPlaybook(unittest.TestCase):
    """Test troubleshooting playbook generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.playbook = TroubleshootingPlaybook()
        
        # Create sample issues
        self.issues = [
            Issue(
                type="complexity",
                severity=IssueSeverity.HIGH,
                title="High complexity",
                description="Function has cyclomatic complexity of 25",
                location="test.py:10",
                recommendation="Refactor",
                code_snippet=None
            ),
            Issue(
                type="unused",
                severity=IssueSeverity.MEDIUM,
                title="Unused import",
                description="Import 'os' is unused",
                location="test.py:1",
                recommendation="Remove import",
                code_snippet=None
            ),
            Issue(
                type="security",
                severity=IssueSeverity.CRITICAL,
                title="SQL injection",
                description="Potential SQL injection vulnerability",
                location="db.py:42",
                recommendation="Use parameterized queries",
                code_snippet=None
            )
        ]
    
    def test_categorize_issues(self):
        """Test issue categorization."""
        categories = self.playbook._categorize_issues(self.issues)
        
        self.assertIn("high_complexity", categories)
        self.assertIn("unused_code", categories)
        self.assertIn("security", categories)
        
        self.assertEqual(len(categories["high_complexity"]), 1)
        self.assertEqual(len(categories["security"]), 1)
    
    def test_format_troubleshooting_playbook(self):
        """Test playbook formatting."""
        output = format_troubleshooting_playbook(self.issues)
        
        self.assertIn("TROUBLESHOOTING PLAYBOOK", output)
        self.assertIn("High Complexity Functions", output)
        self.assertIn("Security Issues", output)
    
    def test_empty_issues(self):
        """Test with no issues."""
        output = format_troubleshooting_playbook([])
        
        self.assertEqual(output, "")


class TestGlossaryGenerator(unittest.TestCase):
    """Test glossary generation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = GlossaryGenerator()
        
        # Create sample modules
        self.modules = [
            ModuleInfo(
                name="api_handler",
                file_path="/test/api_handler.py",
                lines_of_code=100,
                imports=["flask", "api"],
                classes=[
                    ClassInfo(
                        name="RequestHandler",
                        methods=[],
                        line_start=1,
                        line_end=50,
                        docstring="Handles incoming HTTP requests"
                    )
                ],
                functions=[
                    FunctionInfo(
                        name="parse_json",
                        complexity=3,
                        parameters=["data"],
                        returns="dict",
                        docstring="Parse JSON data from request"
                    )
                ]
            )
        ]
    
    def test_extract_domain_terms(self):
        """Test extraction of domain terms."""
        terms = self.generator._extract_domain_terms(self.modules)
        
        self.assertIn("request handler", terms)
        self.assertIn("parse json", terms)
    
    def test_find_tech_terms(self):
        """Test finding technical terms."""
        terms = self.generator._find_tech_terms(self.modules)
        
        self.assertIn("api", terms)
    
    def test_camel_to_words(self):
        """Test CamelCase conversion."""
        result = self.generator._camel_to_words("RequestHandler")
        self.assertEqual(result, "Request Handler")
    
    def test_snake_to_words(self):
        """Test snake_case conversion."""
        result = self.generator._snake_to_words("parse_json")
        self.assertEqual(result, "parse json")
    
    def test_format_glossary(self):
        """Test glossary formatting."""
        output = format_glossary(self.modules, "test-project")
        
        self.assertIn("GLOSSARY & KEY CONCEPTS", output)
        self.assertIn("##", output)  # Should have section headers


class TestEdgeCaseAnalyzer(unittest.TestCase):
    """Test edge case analysis."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = EdgeCaseAnalyzer()
        
        # Create sample modules
        self.modules = [
            ModuleInfo(
                name="validator",
                file_path="/test/validator.py",
                lines_of_code=100,
                imports=[],
                classes=[],
                functions=[
                    FunctionInfo(
                        name="validate_input",
                        complexity=5,
                        parameters=["data"],
                        returns="bool",
                        docstring="Validates input data. Returns False for empty or None values."
                    ),
                    FunctionInfo(
                        name="check_bounds",
                        complexity=3,
                        parameters=["value", "min_val", "max_val"],
                        returns="bool",
                        docstring="Checks if value is within min and max boundaries."
                    )
                ]
            )
        ]
    
    def test_analyze_function(self):
        """Test function analysis for edge cases."""
        func = self.modules[0].functions[0]
        cases = self.analyzer._analyze_function(func, self.modules[0])
        
        self.assertTrue(len(cases) > 0)
        
        # Should detect "empty" and "None" handling
        categories = [c[0] for c in cases]
        self.assertIn("empty_input", categories)
        self.assertIn("null_values", categories)
    
    def test_analyze_edge_cases(self):
        """Test full edge case analysis."""
        edge_cases = self.analyzer.analyze_edge_cases(self.modules)
        
        self.assertIsInstance(edge_cases, dict)
    
    def test_format_edge_cases(self):
        """Test edge cases formatting."""
        output = format_edge_cases(self.modules)
        
        self.assertIn("EDGE CASES", output)
        self.assertIn("BOUNDARY CONDITIONS", output)
    
    def test_generate_recommendations(self):
        """Test recommendation generation."""
        recommendations = self.analyzer.generate_recommendations(self.modules)
        
        self.assertIsInstance(recommendations, list)


if __name__ == "__main__":
    unittest.main()
