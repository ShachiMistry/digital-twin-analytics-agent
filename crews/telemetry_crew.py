# crews/telemetry_crew.py
from __future__ import annotations

from dataclasses import asdict

# Sketch imports; adjust to installed CrewAI version
from crewai import Agent, Crew, Task, Process

from domain.models import WorkflowState
from crews.tasks import PipelineTasks


class TelemetryPipelineCrew:
    def __init__(self) -> None:
        self.pipeline = PipelineTasks()

        self.telemetry_agent = Agent(
            role="Telemetry Analyst",
            goal="Convert raw telemetry into machine-health features",
            backstory="Specialist in signal conditioning and feature extraction.",
            verbose=True,
        )

        self.phase_agent = Agent(
            role="Phase Detection Specialist",
            goal="Identify current asset operating phase",
            backstory="Expert in process-state classification.",
            verbose=True,
        )

        self.baseline_agent = Agent(
            role="Golden Run Comparator",
            goal="Compare current behavior with known-good baseline",
            backstory="Expert in baseline matching and drift detection.",
            verbose=True,
        )

        self.risk_agent = Agent(
            role="Risk Analyst",
            goal="Estimate anomaly severity and near-term failure risk",
            backstory="Reliability engineer focused on operational forecasting.",
            verbose=True,
        )

        self.safety_agent = Agent(
            role="Safety Supervisor",
            goal="Check rule violations and safety constraints",
            backstory="Guardian of safe operating boundaries.",
            verbose=True,
        )

    def run(self, state: WorkflowState) -> WorkflowState:
        # In practice, these Tasks can invoke tools or callbacks.
        # Here we keep the orchestration clear and let Python services do the work.

        self.pipeline.run_telemetry_mining(state)
        self.pipeline.run_phase_detection(state)
        self.pipeline.run_golden_run_comparison(state)
        self.pipeline.run_risk_assessment(state)
        self.pipeline.run_safety_evaluation(state)

        return state

    def summarize_for_reasoning(self, state: WorkflowState) -> dict:
        return {
            "features": asdict(state.features) if state.features else None,
            "phase": asdict(state.phase) if state.phase else None,
            "baseline": asdict(state.baseline) if state.baseline else None,
            "risk": asdict(state.risk) if state.risk else None,
            "safety": asdict(state.safety) if state.safety else None,
        }