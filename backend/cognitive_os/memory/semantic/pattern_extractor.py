"""PatternExtractor module.

Extracts statistical domain knowledge (Knowledge objects) across multiple historical Episode records.
Creates distilled features and habits without black-box ML.
"""

from typing import List, Dict, Any
from collections import Counter
from backend.cognitive_os.memory.episodic.episode import Episode
from backend.cognitive_os.memory.semantic.knowledge import Knowledge


class PatternExtractor:
    def extract_knowledge_from_episodes(self, episodes: List[Episode]) -> List[Knowledge]:
        """Extracts distilled statistical Knowledge objects from a collection of episodes."""
        if not episodes:
            return []

        total_battles = len(episodes)
        extracted: List[Knowledge] = []

        # 1. Preferred Dodge Analysis
        dodge_counts: Counter = Counter()
        for ep in episodes:
            dodge = ep.player_profile.preferred_dodge or ep.battle_summary.preferred_dodge
            if dodge and dodge != "Unknown":
                dodge_counts[dodge] += 1

        if dodge_counts:
            top_dodge, count = dodge_counts.most_common(1)[0]
            dodge_ratio = round(count / total_battles, 2)
            confidence = min(0.99, round(0.5 + (dodge_ratio * 0.4) + (min(total_battles, 20) / 40.0), 2))
            extracted.append(
                Knowledge(
                    id=f"kn_dodge_{top_dodge.lower()}",
                    type="PreferredDodge",
                    confidence=confidence,
                    evidence_count=total_battles,
                    description=f"Player prefers dodging {top_dodge} ({int(dodge_ratio*100)}% of battles)",
                    metadata={"preferred_dodge": top_dodge, "ratio": dodge_ratio}
                )
            )

        # 2. Reload Habit Analysis
        total_reloads = sum(ep.battle_summary.reload_count for ep in episodes)
        avg_reloads = round(total_reloads / total_battles, 1)
        reload_confidence = min(0.98, round(0.6 + (min(total_battles, 20) / 50.0), 2))
        extracted.append(
            Knowledge(
                id="kn_reload_habit",
                type="PlayerReloadHabit",
                confidence=reload_confidence,
                evidence_count=total_battles,
                description=f"Player averages {avg_reloads} reloads per battle",
                metadata={"avg_reloads_per_battle": avg_reloads}
            )
        )

        # 3. Preferred Weapon Analysis
        weapon_counts: Counter = Counter()
        for ep in episodes:
            wep = ep.player_profile.most_used_weapon or ep.battle_summary.most_used_weapon
            if wep and wep != "Unknown":
                weapon_counts[wep] += 1

        if weapon_counts:
            top_wep, count = weapon_counts.most_common(1)[0]
            wep_ratio = round(count / total_battles, 2)
            wep_confidence = min(0.95, round(0.55 + (wep_ratio * 0.35), 2))
            extracted.append(
                Knowledge(
                    id=f"kn_wep_{top_wep.lower()}",
                    type="PreferredWeapon",
                    confidence=wep_confidence,
                    evidence_count=total_battles,
                    description=f"Player prefers using {top_wep} ({int(wep_ratio*100)}% of battles)",
                    metadata={"preferred_weapon": top_wep, "ratio": wep_ratio}
                )
            )

        # 4. Engagement Distance & Aggression Analysis
        avg_dist = round(sum(ep.battle_summary.average_distance for ep in episodes) / total_battles, 1)
        avg_aggression = round(sum(ep.battle_summary.aggression_score for ep in episodes) / total_battles, 2)

        extracted.append(
            Knowledge(
                id="kn_engagement_range",
                type="EngagementRange",
                confidence=0.90,
                evidence_count=total_battles,
                description=f"Player prefers engagement distance of ~{avg_dist}m (Aggression: {avg_aggression})",
                metadata={"avg_distance_meters": avg_dist, "aggression_score": avg_aggression}
            )
        )

        return extracted
