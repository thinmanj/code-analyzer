"""Command-line interface for code-analyzer."""

import click
import json
import yaml
from pathlib import Path
from rich.console import Console
from rich.table import Table

from .analyzer import CodeAnalyzer
from .anonymizer import CodeAnonymizer
from .logseq_integration import LogseqDocGenerator
from .tickets_integration import TicketsManager
from .models import IssueSeverity
from .onboarding import OnboardingAnalyzer, format_onboarding_report

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """Code Analyzer - Deep source code analysis and documentation tool."""
    pass


@main.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--depth", type=click.Choice(["shallow", "medium", "deep"]), default="deep",
              help="Analysis depth")
@click.option("--logseq-graph", type=click.Path(), 
              help="Logseq graph path for documentation")
@click.option("--create-tickets", is_flag=True, 
              help="Create tickets for issues")
@click.option("--generate-docs", is_flag=True, 
              help="Generate Logseq documentation")
@click.option("--output", type=click.Path(), default=".code-analyzer",
              help="Output directory for analysis data")
@click.option("--config", type=click.Path(exists=True),
              help="Configuration file path")
@click.option("--plugins", type=click.Path(exists=True),
              help="Directory containing custom plugins")
@click.option("--code-library", type=click.Path(),
              help="Path to code library YAML file")
@click.option("--use-default-library", is_flag=True,
              help="Use built-in default code library")
@click.option("--onboarding", is_flag=True,
              help="Generate onboarding guide for new developers")
def analyze(project_path, depth, logseq_graph, create_tickets, generate_docs, output, config, plugins, code_library, use_default_library, onboarding):
    """Analyze a Python project."""
    console.print("[bold blue]🔍 Code Analyzer[/bold blue]")
    console.print(f"Project: {project_path}\n")
    
    # Load configuration
    cfg = {}
    if config:
        with open(config, 'r') as f:
            cfg = yaml.safe_load(f) or {}
    
    # Check for config file in project
    config_path = Path(project_path) / ".code-analyzer.yaml"
    if config_path.exists():
        with open(config_path, 'r') as f:
            cfg = yaml.safe_load(f) or {}
    
    # Apply config overrides
    if cfg:
        depth = cfg.get("analysis", {}).get("depth", depth)
        if not logseq_graph:
            logseq_graph = cfg.get("documentation", {}).get("logseq_graph")
        if not create_tickets and cfg.get("tickets", {}).get("enabled"):
            create_tickets = True
        if not generate_docs and cfg.get("documentation", {}).get("create_index"):
            generate_docs = True
    
    # Get plugin and library paths from config
    if not plugins:
        plugins = cfg.get("plugins", {}).get("directory")
    if not code_library:
        code_library = cfg.get("code_library", {}).get("path")
    if not use_default_library:
        use_default_library = cfg.get("code_library", {}).get("use_default", False)
    
    # Prepare paths
    plugin_dir = Path(plugins) if plugins else None
    library_path = Path(code_library) if code_library else None
    
    # Use default library if requested
    if use_default_library and not library_path:
        library_path = Path(".code-analyzer") / "default_library.yaml"  # Marker for default
    
    # Initialize analyzer
    ignore_patterns = cfg.get("analysis", {}).get("ignore_patterns")
    analyzer = CodeAnalyzer(
        project_path, 
        ignore_patterns=ignore_patterns,
        plugin_dir=plugin_dir,
        code_library_path=library_path
    )
    
    # Run analysis
    with console.status("[bold green]Analyzing code..."):
        result = analyzer.analyze(depth=depth)
    
    # Display summary
    _display_summary(result)
    
    # Save results
    output_dir = Path(project_path) / output
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate Logseq documentation BEFORE saving new analysis (so it can compare with previous)
    if generate_docs and logseq_graph:
        project_name = Path(project_path).name
        doc_gen = LogseqDocGenerator(logseq_graph)
        doc_gen.generate_documentation(result, project_name)
    
    # Save JSON report AFTER documentation (so resolved issue tracking works)
    json_file = output_dir / "analysis.json"
    with open(json_file, 'w') as f:
        json.dump(_result_to_dict(result), f, indent=2, default=str)
    console.print(f"\n💾 Saved analysis to: {json_file}")
    
    # Create tickets
    if create_tickets:
        project_name = Path(project_path).name
        tickets_mgr = TicketsManager(project_path)
        tickets_mgr.create_epic_and_tickets(result, project_name)
    
    # Generate onboarding report
    if onboarding:
        onboarding_analyzer = OnboardingAnalyzer(Path(project_path))
        insights = onboarding_analyzer.generate_insights(result.modules)
        onboarding_report = format_onboarding_report(insights)
        
        # Save onboarding report
        onboarding_file = output_dir / "ONBOARDING.md"
        with open(onboarding_file, 'w') as f:
            f.write(onboarding_report)
        console.print(f"\n📚 Saved onboarding guide to: {onboarding_file}")
        
        # Also print it to console
        console.print("\n" + "=" * 80)
        console.print(onboarding_report)
    
    console.print("\n[bold green]✅ Analysis complete![/bold green]")


@main.command()
@click.argument("project_path", type=click.Path(exists=True))
@click.option("--output", type=click.Path(), required=True,
              help="Output directory for anonymized code")
def anonymize(project_path, output):
    """Anonymize code for external analysis."""
    console.print("[bold blue]🔒 Code Anonymizer[/bold blue]\n")
    
    anonymizer = CodeAnonymizer()
    
    with console.status("[bold green]Anonymizing code..."):
        source_path = Path(project_path)
        output_path = Path(output)
        anonymizer.anonymize_project(source_path, output_path)
    
    # Create structure summary
    summary = anonymizer.create_structure_summary(source_path)
    summary_file = output_path / "STRUCTURE_SUMMARY.md"
    summary_file.write_text(summary)
    
    console.print(f"\n[bold green]✅ Anonymization complete![/bold green]")
    console.print(f"Output: {output_path}")
    console.print(f"\n[bold yellow]⚠️  Keep {output_path}/ANONYMIZATION_MAP.txt secure![/bold yellow]")


@main.command()
@click.argument("analysis_file", type=click.Path(exists=True))
@click.option("--severity", type=click.Choice(["critical", "high", "medium", "low"]),
              help="Filter by severity")
@click.option("--type", "issue_type", help="Filter by issue type")
def report(analysis_file, severity, issue_type):
    """Generate report from analysis results."""
    with open(analysis_file, 'r') as f:
        data = json.load(f)
    
    console.print("[bold blue]📊 Analysis Report[/bold blue]\n")
    
    # Display metrics
    metrics = data["metrics"]
    console.print("[bold]Code Metrics[/bold]")
    console.print(f"Files: {metrics['total_files']}")
    console.print(f"Lines: {metrics['total_lines']:,}")
    console.print(f"Classes: {metrics['total_classes']}")
    console.print(f"Functions: {metrics['total_functions']}")
    console.print(f"Average Complexity: {metrics['average_complexity']:.2f}")
    console.print()
    
    # Display issues table
    issues = data["issues"]
    
    if severity:
        issues = [i for i in issues if i["severity"] == severity]
    if issue_type:
        issues = [i for i in issues if i["type"] == issue_type]
    
    if issues:
        table = Table(title=f"Issues ({len(issues)})")
        table.add_column("Severity", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Title", style="white")
        table.add_column("Location", style="green")
        
        for issue in issues[:50]:  # Show first 50
            sev_color = {
                "critical": "red",
                "high": "orange1",
                "medium": "yellow",
                "low": "blue"
            }.get(issue["severity"], "white")
            
            table.add_row(
                f"[{sev_color}]{issue['severity'].upper()}[/{sev_color}]",
                issue["type"],
                issue["title"][:50],
                issue["location"]
            )
        
        console.print(table)
        
        if len(data["issues"]) > 50:
            console.print(f"\n... and {len(data['issues']) - 50} more issues")
    else:
        console.print("[yellow]No issues found matching criteria[/yellow]")


def _display_summary(result):
    """Display analysis summary."""
    console.print("\n[bold]Analysis Summary[/bold]")
    
    # Metrics table
    table = Table(show_header=False)
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Files Analyzed", str(result.metrics.total_files))
    table.add_row("Total Lines", f"{result.metrics.total_lines:,}")
    table.add_row("Classes", str(result.metrics.total_classes))
    table.add_row("Functions", str(result.metrics.total_functions))
    table.add_row("Issues Found", str(result.metrics.total_issues))
    table.add_row("Critical Sections", str(len(result.critical_sections)))
    table.add_row("Avg Complexity", f"{result.metrics.average_complexity:.2f}")
    table.add_row("Max Complexity", str(result.metrics.max_complexity))
    
    console.print(table)
    
    # Issues by severity
    if result.issues:
        console.print("\n[bold]Issues by Severity[/bold]")
        for severity in ["critical", "high", "medium", "low"]:
            count = result.metrics.issues_by_severity.get(severity, 0)
            if count > 0:
                color = {
                    "critical": "red",
                    "high": "orange1",
                    "medium": "yellow",
                    "low": "blue"
                }[severity]
                console.print(f"  [{color}]●[/{color}] {severity.upper()}: {count}")


def _result_to_dict(result):
    """Convert AnalysisResult to dictionary."""
    return {
        "project_path": result.project_path,
        "analysis_date": result.analysis_date.isoformat(),
        "metrics": {
            "total_files": result.metrics.total_files,
            "total_lines": result.metrics.total_lines,
            "total_classes": result.metrics.total_classes,
            "total_functions": result.metrics.total_functions,
            "total_issues": result.metrics.total_issues,
            "issues_by_severity": result.metrics.issues_by_severity,
            "issues_by_type": result.metrics.issues_by_type,
            "average_complexity": result.metrics.average_complexity,
            "max_complexity": result.metrics.max_complexity,
        },
        "issues": [issue.to_dict() for issue in result.issues],
        "critical_sections": [
            {
                "name": cs.name,
                "location": str(cs.location),
                "reason": cs.reason,
                "risk_level": cs.risk_level.value,
            }
            for cs in result.critical_sections
        ],
        "entry_points": result.entry_points,
        "dependency_graph": result.dependency_graph,
        "important_sections": [
            {
                "name": s.name,
                "location": str(s.location),
                "category": s.category,
                "importance": s.importance,
                "description": s.description,
                "pattern_type": getattr(s, 'pattern_type', None),
            }
            for s in result.important_sections
        ],
    }


if __name__ == "__main__":
    main()
