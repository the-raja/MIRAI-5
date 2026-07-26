"""ThreatReportFormatter module.

Step 1: Formats and prints Threat Ranking console report:

====================================
Threat Ranking
====================================
Ultimate: 0.95
Healing:  0.91
Reload:   0.28
Retreat:  0.16
====================================
"""

from typing import List, Tuple, Dict, Any, Optional


class ThreatReportFormatter:
    @staticmethod
    def format_threat_report(ranked_threats: List[Tuple[str, float]]) -> str:
        """Formats ranked threat list into exact Step 1 console card string."""
        lines: List[str] = []
        lines.append("====================================")
        lines.append("Threat Ranking")
        lines.append("====================================")

        for act, score in ranked_threats:
            lines.append(f"{act:<10}: {score:.2f}")

        lines.append("====================================")
        return "\n".join(lines)

    @classmethod
    def print_threat_report(cls, ranked_threats: Optional[List[Tuple[str, float]]] = None) -> None:
        """Prints Threat Ranking report card to stdout."""
        threats = ranked_threats or [
            ("Ultimate", 0.95),
            ("Healing", 0.91),
            ("Reload", 0.28),
            ("Retreat", 0.16)
        ]
        print(cls.format_threat_report(threats))
