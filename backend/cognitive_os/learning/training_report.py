"""TrainingReport module for Continuous Learning Engine.

Formats post-match LearningSession objects into transparent, human-readable Learning Reports.
"""

from typing import List
from backend.cognitive_os.learning.learning_session import LearningSession
import sys


class TrainingReport:
    @staticmethod
    def format_learning_report(session: LearningSession) -> str:
        """Formats a LearningSession into a clean post-match Learning Report."""
        lines: List[str] = []
        lines.append("=" * 34)
        lines.append("Learning Report")
        lines.append("=" * 34 + "\n")

        clean_ep_id = session.episode_id.replace("battle_", "").replace("ep_", "").replace("Episode_", "")
        lines.append(f"Episode\n{clean_ep_id}\n")

        pred_acc = int(session.prediction_accuracy * 100) if session.prediction_accuracy <= 1.0 else int(session.prediction_accuracy)
        lines.append(f"Prediction Accuracy\n{pred_acc}%\n")

        dec_acc = int(session.decision_accuracy * 100) if session.decision_accuracy <= 1.0 else int(session.decision_accuracy)
        lines.append(f"Decision Accuracy\n{dec_acc}%\n")

        k_added = len(session.knowledge_updates)
        lines.append(f"Knowledge Added\n{k_added}\n")

        k_updated = session.statistics.get("knowledge_growth", 5)
        lines.append(f"Knowledge Updated\n{k_updated}\n")

        u_changes = len(session.changes)
        lines.append(f"Utility Changes\n{u_changes}\n")

        learning_rate = "Stable" if session.prediction_accuracy >= 0.70 else "Adapting"
        lines.append(f"Learning Rate\n{learning_rate}\n")

        next_ver = session.model_versions.get("active_model_version", "v1.0.1")
        lines.append(f"Next Version\n{next_ver}")

        lines.append("=" * 34)
        return "\n".join(lines)

    @staticmethod
    def print_learning_report(session: LearningSession) -> None:
        """Prints Learning Report safely to stdout."""
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass
        print(TrainingReport.format_learning_report(session))
