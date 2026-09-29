

import json
from prompts.engagement_prompt import EngagementEvaluationPrompt

class Classifier:
    def __init__(self, openai_client,model,context):
        self.openai_client = openai_client
        self.model = model
        self.context = context

    def build_conversation(self):
        messages = []
        messages.append({"role": "system", "content": EngagementEvaluationPrompt.SYSTEM_MESSAGE_ENGAGEMENT})
        context_str = "\n".join([f"Follow-up {i+1}:\nQ: {q}\nA: {a}" for i, (q, a) in enumerate(self.context)])


        input_as_str = EngagementEvaluationPrompt.USER_MESSAGE_TEMPLATE.format(
                thread_content=context_str
        )

        messages.append({"role": "user", "content": input_as_str})
        return messages



    def _get_prediction(self, messages):
        chat_response =  self.openai_client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=EngagementEvaluationPrompt.tools_thread ,
            tool_choice="required",
            temperature=0.5
        )
        assistant_message = chat_response.choices[0].message
        tool_call = assistant_message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        return arguments[EngagementEvaluationPrompt.SELECTED_ENGAGEMENT_LEVEL_KEY]



    def classify(self):
        messages = self.build_conversation()
        result  = self._get_prediction(messages)
        return result
