"""Offline behavior checks; these do not evaluate any language model."""

import unittest

from demo import ScriptedClient, load_sample
from workflow import run_interview


class WorkflowTests(unittest.TestCase):
    def run_case(self, client, answer="A fictional answer", max_turns=3):
        return run_interview(client, "fixture", load_sample(), lambda question: answer, max_turns)

    def test_agent_stop_prevents_another_followup(self):
        client = ScriptedClient()
        result = self.run_case(client)
        self.assertEqual(result["stop_reason"], "agent_decision")
        self.assertEqual(client.calls.count("thread_up_handler"), 1)

    def test_participant_can_stop(self):
        result = self.run_case(ScriptedClient(stop_after=99), answer="/stop")
        self.assertEqual(result["stop_reason"], "participant_stop")
        self.assertEqual(len(result["conversation"]), 1)

    def test_sensitive_content_stops_even_if_judge_wants_to_continue(self):
        client = ScriptedClient(stop_after=99, sensitive=True)
        result = self.run_case(client)
        self.assertEqual(result["stop_reason"], "sensitive_content")
        self.assertNotIn("thread_up_handler", client.calls)

    def test_turn_limit_prevents_unbounded_followups(self):
        client = ScriptedClient(stop_after=99)
        result = self.run_case(client, max_turns=2)
        self.assertEqual(result["stop_reason"], "turn_limit")
        self.assertEqual(client.calls.count("thread_up_handler"), 2)

    def test_unknown_decision_is_not_treated_as_continue(self):
        with self.assertRaises(ValueError):
            self.run_case(ScriptedClient(decision="invalid"))


if __name__ == "__main__":
    unittest.main()
