"""Attention Engine module.

Intakes ObservationSet data, ranks observations/events by saliency priority, and isolates focus targets.
Contains NO decisions — only saliency scoring and target ranking.
"""

from typing import Optional, List, Dict
from backend.cognitive_os.perception.observation import ObservationSet
from backend.cognitive_os.attention.salience import AttentionState, SalienceEvent
from backend.cognitive_os.event_bus.event_bus import EventBus
from backend.cognitive_os.event_bus.events import Event


class AttentionEngine:
    # Rule-based saliency priority matrix
    SALIENCY_PRIORITY_MAP: Dict[str, float] = {
        "ProjectileIncoming": 95.0,
        "PlayerReloading": 90.0,
        "BossHit": 80.0,
        "PlayerEnteredCover": 70.0,
        "PlayerVisible": 50.0,
        "PlayerRunning": 20.0,
    }

    def __init__(self, event_bus: Optional[EventBus] = None) -> None:
        self.event_bus = event_bus
        if self.event_bus:
            self.event_bus.subscribe("OBSERVATION_SET", self._on_observation_set)

    def _on_observation_set(self, event: Event) -> None:
        if isinstance(event.payload, ObservationSet):
            self.process_observations(event.payload)

    def process_observations(self, obs_set: ObservationSet) -> AttentionState:
        """Processes ObservationSet and produces a prioritized AttentionState."""
        salient_events: List[SalienceEvent] = []
        priority_targets: List[str] = []
        primary_target_id: Optional[str] = None

        # 1. Rank flagged observations by saliency map
        for flag_name, flag_value in obs_set.flags.items():
            if flag_value:
                priority = self.SALIENCY_PRIORITY_MAP.get(flag_name, 10.0)
                salient_events.append(
                    SalienceEvent(
                        event_id=f"evt_{flag_name}",
                        saliency_score=priority,
                        reason=f"Flag {flag_name} active",
                        timestamp=obs_set.timestamp
                    )
                )

        # 2. Sort salient events descending by saliency score
        salient_events.sort(key=lambda ev: ev.saliency_score, reverse=True)

        # 3. Extract priority targets from observations
        for obs in obs_set.observations:
            if obs.type == "PLAYER_OBSERVATION":
                target_id = obs.source
                priority_targets.append(target_id)

                # Assign primary target (closest / highest priority)
                if primary_target_id is None:
                    primary_target_id = target_id

        att_state = AttentionState(
            timestamp=obs_set.timestamp,
            primary_target_id=primary_target_id,
            priority_targets=priority_targets,
            salient_events=salient_events,
            focus_score=1.0 if salient_events else 0.5
        )

        if self.event_bus:
            event = Event(
                event_type="ATTENTION_STATE",
                timestamp=obs_set.timestamp,
                source="AttentionEngine",
                payload=att_state
            )
            self.event_bus.publish(event)

        return att_state
