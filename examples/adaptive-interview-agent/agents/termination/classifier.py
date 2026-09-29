import json
from prompts.termination_prompt import ConversationFlowJudgmentPrompt

class FlowDecisionClassifier:
    def __init__(self, openai_client, model, engagement_level, sensitivity_level,sufficiency_level,context):
        self.openai_client = openai_client
        self.model = model
        self.engagement_level = engagement_level
        self.sensitivity_level = sensitivity_level

        self.sufficiency_level = sufficiency_level
        self.context = context

    def build_conversation(self):
        messages = []
        messages.append({
            "role": "system",
            "content": ConversationFlowJudgmentPrompt.SYSTEM_MESSAGE_FLOW_DECISION
        })
        context_str = "\n".join([f"Follow-up {i+1}:\nQ: {q}\nA: {a}" for i, (q, a) in enumerate(self.context)])

        input_str = ConversationFlowJudgmentPrompt.USER_MESSAGE_TEMPLATE.format(
            sensitivity_level=self.sensitivity_level,
            engagement_level=self.engagement_level,
            sufficiency_level=self.sufficiency_level,
            thread_content = context_str
        )

        messages.append({
            "role": "user",
            "content": input_str
        })
        return messages

    def _get_prediction(self, messages):
        chat_response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=ConversationFlowJudgmentPrompt.tools_thread,
            tool_choice="required",
            temperature=0.2
        )
        assistant_message = chat_response.choices[0].message
        tool_call = assistant_message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        return arguments[ConversationFlowJudgmentPrompt.DECISION_KEY]

    def classify(self):
        messages = self.build_conversation()
        result = self._get_prediction(messages)
        return result
