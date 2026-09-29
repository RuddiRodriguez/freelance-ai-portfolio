"""Small public runner around the research prototype's specialist agents."""

from types import SimpleNamespace

from agents.engagement.classifier import Classifier as EngagementClassifier
from agents.sensitivity.classifier import Classifier as SensitivityClassifier
from agents.sufficiency.classifier import Classifier as SufficiencyClassifier
from agents.termination.classifier import FlowDecisionClassifier
from followup_conversation_thread import GenerateFollowupConversationThread


def run_interview(client, model, sample, read_answer, max_turns=3):
    """Assess each answer, then stop or ask one follow-up; return an audit record.

    The caller supplies a compatible chat-completions client. No credentials,
    private workbook, prompt registry or network connection are configured here.
    """
    if max_turns < 0:
        raise ValueError("max_turns must be zero or greater")
    context = [(sample["question"], sample["answer"])]
    data = SimpleNamespace(
        list_questions_answers=[SimpleNamespace(**item) for item in sample["timeline"]],
        last_question_answer=SimpleNamespace(
            question_text=sample["question"], answer_text=sample["answer"]
        ),
    )
    events = []
    for turn in range(max_turns + 1):
        engagement = EngagementClassifier(client, model, context).classify()
        sensitivity = SensitivityClassifier(client, model, context).classify()
        sufficiency = SufficiencyClassifier(client, model, context).classify()
        decision = FlowDecisionClassifier(
            client, model, engagement, sensitivity, sufficiency, context
        ).classify()
        if decision not in {"terminate_conversation", "continue_conversation"}:
            raise ValueError("Unrecognized conversation decision")
        events.append({
            "turn": turn, "engagement": engagement, "sensitivity": sensitivity,
            "sufficiency": sufficiency, "decision": decision,
        })
        if sensitivity == "Sensitive":
            reason = "sensitive_content"
            break
        if decision == "terminate_conversation":
            reason = "agent_decision"
            break
        if turn == max_turns:
            reason = "turn_limit"
            break

        question = GenerateFollowupConversationThread(
            data, client, model, context, list(sample["plan"].items())
        ).test()
        answer = read_answer(question)
        if answer is None or answer.strip().lower() in {"/stop", "stop", "quit", "exit"}:
            reason = "participant_stop"
            break
        context.append((question, answer))
    return {"stop_reason": reason, "conversation": context, "assessments": events}
