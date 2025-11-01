"""Performance hotspot identification."""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from .models import ModuleInfo, FunctionInfo


@dataclass
class PerformanceHotspot:
    """Identified performance concern."""
    location: str
    pattern: str
    severity: str  # 'high', 'medium', 'low'
    description: str
    suggestion: str


class PerformanceAnalyzer:
    """Identifies performance hotspots through static analysis."""
    
    # Known slow patterns
    SLOW_PATTERNS = {
        'nested_loops': ('Nested loops detected', 'Consider flattening loops or using list comprehensions'),
        'string_concat': ('String concatenation in loop', 'Use join() or StringIO for better performance'),
        'list_append_loop': ('List append in tight loop', 'Consider list comprehension or preallocating'),
        'deep_recursion': ('Deep recursion possible', 'Consider iterative approach or memoization'),
        'inefficient_search': ('Linear search pattern', 'Use dict/set for O(1) lookups'),
    }
    
    def analyze_performance(self, modules: List[ModuleInfo]) -> List[PerformanceHotspot]:
        """Analyze modules for performance hotspots."""
        hotspots = []
        
        for module in modules:
            # Analyze functions
            for func in module.functions:
                hotspots.extend(self._analyze_function(func, module.name))
            
            # Analyze methods
            for cls in module.classes:
                for method in cls.methods:
                    hotspots.extend(self._analyze_function(method, f"{module.name}.{cls.name}"))
        
        return hotspots
    
    def _analyze_function(self, func: FunctionInfo, context: str) -> List[PerformanceHotspot]:
        """Analyze single function for performance issues."""
        hotspots = []
        location = f"{context}.{func.name}"
        
        # High complexity indicates potential performance issues
        if func.complexity > 20:
            hotspots.append(PerformanceHotspot(
                location=location,
                pattern='high_complexity',
                severity='high',
                description=f'Very high complexity ({func.complexity}) suggests nested logic',
                suggestion='Refactor to reduce branching and improve performance'
            ))
        
        # Check function name for clues
        func_lower = func.name.lower()
        
        if 'recursive' in func_lower or func_lower.startswith('_rec'):
            hotspots.append(PerformanceHotspot(
                location=location,
                pattern='deep_recursion',
                severity='medium',
                description=self.SLOW_PATTERNS['deep_recursion'][0],
                suggestion=self.SLOW_PATTERNS['deep_recursion'][1]
            ))
        
        if 'search' in func_lower or 'find' in func_lower:
            hotspots.append(PerformanceHotspot(
                location=location,
                pattern='inefficient_search',
                severity='medium',
                description=self.SLOW_PATTERNS['inefficient_search'][0],
                suggestion=self.SLOW_PATTERNS['inefficient_search'][1]
            ))
        
        # Check for nested loops (complexity > 10 is a rough indicator)
        if func.complexity > 10:
            hotspots.append(PerformanceHotspot(
                location=location,
                pattern='nested_loops',
                severity='high' if func.complexity > 15 else 'medium',
                description=self.SLOW_PATTERNS['nested_loops'][0],
                suggestion=self.SLOW_PATTERNS['nested_loops'][1]
            ))
        
        return hotspots


def format_performance_report(modules: List[ModuleInfo]) -> str:
    """Format performance analysis report."""
    analyzer = PerformanceAnalyzer()
    hotspots = analyzer.analyze_performance(modules)
    
    if not hotspots:
        return ""
    
    output = []
    output.append("# ⚡ PERFORMANCE HOTSPOTS")
    output.append("=" * 80)
    output.append("")
    
    output.append(f"**Total Hotspots Identified**: {len(hotspots)}")
    output.append("")
    
    # Group by severity
    by_severity = {'high': [], 'medium': [], 'low': []}
    for h in hotspots:
        by_severity[h.severity].append(h)
    
    # High severity first
    for severity in ['high', 'medium', 'low']:
        items = by_severity[severity]
        if not items:
            continue
        
        emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[severity]
        output.append(f"## {emoji} {severity.title()} Priority ({len(items)} items)")
        output.append("")
        
        for hotspot in items[:10]:  # Limit per severity
            output.append(f"### `{hotspot.location}`")
            output.append(f"**Pattern**: {hotspot.pattern}")
            output.append(f"**Issue**: {hotspot.description}")
            output.append(f"**Suggestion**: {hotspot.suggestion}")
            output.append("")
    
    # General recommendations
    output.append("## 💡 General Performance Tips")
    output.append("")
    output.append("1. **Profile before optimizing**: Use `cProfile` to find real bottlenecks")
    output.append("2. **Use appropriate data structures**: dict/set for lookups, deque for queues")
    output.append("3. **Lazy evaluation**: Use generators for large datasets")
    output.append("4. **Caching**: Use `@lru_cache` for expensive repeated calls")
    output.append("5. **Vectorization**: Use numpy/pandas for numerical operations")
    output.append("")
    
    return "\n".join(output)
