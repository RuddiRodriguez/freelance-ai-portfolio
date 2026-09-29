"""Offline walkthrough with scripted responses: no model calls, no API key."""

import json
from pathlib import Path
from types import SimpleNamespace

from workflow import run_interview


class ScriptedClient:
    """Test double matching only the response shape used by these modules."""

    def __init__(self, stop_after=2, sensitive=False, decision=None):
        self.chat = SimpleNamespace(completions=self)
        self.round = 0
        self.stop_after = stop_after
        self.sensitive = sensitive
        self.decision = decision
        self.calls = []

    def create(self, *, tools, messages, **options):
        function = tools[0]["function"]
        self.calls.append(function["name"])
        if function["name"] == "engagement_level_handler":
            self.round += 1
        values = {
            "analysis": "Scripted fixture, not an AI assessment.",
            "initial_analysis": "Scripted fixture, not an AI assessment.",
            "reasoning": "Fixed values demonstrate the control flow only.",
            "engagement_level": "High",
            "sensitivity_level": "Sensitive" if self.sensitive else "NotSensitive",
            "sufficiency_level": "Sufficient" if self.round >= self.stop_after else "Moderate",
            "conversation_decision": self.decision or (
                "terminate_conversation" if self.round >= self.stop_after
                else "continue_conversation"
            ),
            "follow_up": "Which part of finding a saved note would you improve first?",
        }
        arguments = {key: values[key] for key in function["parameters"]["properties"]}
        response = SimpleNamespace(function=SimpleNamespace(arguments=json.dumps(arguments)))
        return SimpleNamespace(choices=[SimpleNamespace(
            message=SimpleNamespace(tool_calls=[response])
        )])


def load_sample():
    return json.loads(Path(__file__).with_name("sample.json").read_text())


if __name__ == "__main__":
    sample = load_sample()
    client = ScriptedClient()
    result = run_interview(
        client, "offline-scripted-fixture", sample,
        lambda question: sample["scripted_followup_answer"],
    )
    print(json.dumps({"mode": "offline-scripted-demo", **result}, indent=2))
