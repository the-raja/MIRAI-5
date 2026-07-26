"""ReasoningTrace module (Explainable AI Audit Log).

Formats every Decision object into a transparent, interview-worthy explainable reasoning trace:
Goal, Candidate Actions & Scores, Chosen Winner, Bulleted Reasons with tickmarks, and Confidence score.
Zero black-box decisions.
"""

from typing import List, Dict, Any
from pydantic import BaseModel, Field
import sys


class ReasoningTraceModel(BaseModel):
    decision_num: int = 412
    goal: str
    candidate_actions: List[str] = Field(default_factory=list)
    scores: Dict[str, float] = Field(default_factory=dict)
    winner: str
    reason_list: List[str] = Field(default_factory=list)
    confidence: float = 0.91


class ReasoningTrace:
    @staticmethod
    def format_trace_model(trace: ReasoningTraceModel, use_unicode: bool = True) -> str:
        """Formats ReasoningTraceModel into an interview-worthy, transparent explainable audit log."""
        tick = "✓ " if use_unicode else "[+] "
        lines: List[str] = []
        lines.append("=" * 50)
        lines.append(f"Decision #{trace.decision_num}\n")
        lines.append(f"Goal\n{trace.goal}\n")
        lines.append("Candidate Actions")

        for act, score in trace.scores.items():
            lines.append(f"{act:<14} {int(score)}")

        lines.append(f"\nChosen\n{trace.winner}\n")
        lines.append("Reasons")

        for r in trace.reason_list:
            clean_reason = r.replace("Goal Driver: ", "").replace("Working memory: ", "").replace(" (+25)", "").replace(" (+15)", "")
            if not clean_reason.startswith(tick) and not clean_reason.startswith("✓ ") and not clean_reason.startswith("[+] "):
                lines.append(f"{tick}{clean_reason}")
            else:
                lines.append(clean_reason)

        lines.append(f"\nConfidence\n{int(trace.confidence * 100)}%")
        lines.append("=" * 50)
        return "\n".join(lines)

    @staticmethod
    def print_trace(trace: ReasoningTraceModel) -> None:
        """Prints formatted reasoning trace safely handling Windows console encoding."""
        try:
            formatted = ReasoningTrace.format_trace_model(trace, use_unicode=True)
            sys.stdout.reconfigure(encoding='utf-8')
            print(formatted)
        except Exception:
            formatted = ReasoningTrace.format_trace_model(trace, use_unicode=False)
            print(formatted)
