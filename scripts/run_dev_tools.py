"""MIRAI v2 — Phase 16 Developer Tools & Visualization Suite Demonstrator Runner.

Executes Developer Visualization Suite inspectors and outputs summary of all 6 developer inspection tools.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.developer_tools.cognitive_graph import CognitiveGraphTracker
from backend.developer_tools.memory_inspector import MemoryInspector
from backend.developer_tools.planner_inspector import PlannerInspector
from backend.developer_tools.replay_viewer import ReplayViewer
from backend.developer_tools.benchmark_dashboard import BenchmarkDashboard


def run_dev_tools_demo() -> None:
    graph_tracker = CognitiveGraphTracker()
    planner_inspector = PlannerInspector()
    replay_viewer = ReplayViewer()
    benchmark_dashboard = BenchmarkDashboard()

    print("\n")
    print("====================================")
    print("MIRAI v2 Developer Tools & Visualization Suite")
    print("====================================")

    # 1. Live Cognitive Graph
    graph_state = graph_tracker.get_live_graph_state(frame_index=24)
    print("\n1. Live Cognitive Graph State:")
    for node in graph_state["nodes"]:
        print(f"   [{node['status']}] {node['label']:<12} -> {node['details']}")

    # 2. Memory Inspector
    memories = MemoryInspector.inspect_all_memories()
    print("\n2. Memory Inspector Snapshot:")
    print(f"   Working Memory:  {memories['working_memory']['active_items']} items active")
    print(f"   Episodic Memory: {memories['episodic_memory']['total_episodes']} total episodes stored")
    print(f"   Semantic Memory: {memories['semantic_memory']['knowledge_nodes']} knowledge graph nodes")
    print(f"   Vector Memory:   {memories['vector_memory']['active_experiences']} active experiences (Top Hit: {memories['vector_memory']['top_similarity_hit']})")

    # 3. Planner Inspector
    plan_data = planner_inspector.get_planner_inspection_data()
    print("\n3. Planner Inspector:")
    print(f"   Goal: {plan_data['current_goal']}")
    print(f"   Execution Progress: {plan_data['execution_progress_pct']}%")

    # 4. Replay Viewer
    frame_data = replay_viewer.get_frame_state(frame_index=24)
    print("\n4. Replay Viewer Frame Debugger (Frame 24):")
    print(f"   Target Action: {frame_data['plan']['active_step']}")
    print(f"   Fused Prediction: {frame_data['predictions']['fused_prediction']}")
    print(f"   Audit Reasoning: {frame_data['reasoning']}")

    # 5. Benchmark Dashboard
    bench_data = benchmark_dashboard.get_benchmark_dashboard_data()
    print("\n5. Benchmark KPI Dashboard:")
    print(f"   Win Rate: {bench_data['win_rate_pct']}% | Latency: {bench_data['avg_latency_ms']} ms | Accuracy: {bench_data['prediction_accuracy_pct']}%")
    print("====================================\n")


if __name__ == "__main__":
    run_dev_tools_demo()
