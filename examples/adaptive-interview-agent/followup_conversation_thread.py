

import json
from prompts.thread_prompt import ThreadPrompt

class GenerateFollowupConversationThread:
    def __init__(self, conversation_plan_input,openai_client,model,context,plan):
        self.openai_client = openai_client
        self.conversation_plan_input = conversation_plan_input
        self.model = model
        self.context = context
        self.plan = plan

    def build_conversation(self):
        messages = []
        messages.append({"role": "system", "content": ThreadPrompt.SYSTEM_MESSAGE_FOLLOWUP})
        context_str = "\n".join([f"Follow-up {i+1}:\nQ: {q}\nA: {a}" for i, (q, a) in enumerate(self.context)])

        time_line = [ThreadPrompt.SURVEY_TIME_LINE_TEMPLATE.format(
                question_id='1',
                question_type='Unknown',
                question_text=qa.question_text,
                answer_text=qa.answer_text
            ) for qa in self.conversation_plan_input.list_questions_answers]

        time_line_str = "\n".join(time_line)

        last_question_answer_str = ThreadPrompt.SURVEY_TIME_LINE_TEMPLATE.format(
                question_id='1',
                question_type='Unknown',
                question_text=self.conversation_plan_input.last_question_answer.question_text,
                answer_text=self.conversation_plan_input.last_question_answer.answer_text
            )

        last_question_answer_str = last_question_answer_str.strip()

        objective_str = ", ".join(f"{key}: {value}" for key, value in self.plan)


        input_as_str = ThreadPrompt.USER_MESSAGE_THREAD.format(
            questions_answers=time_line_str,
            last_question_answer=last_question_answer_str,
            followup_conversation_plan=objective_str,
            thread_content=context_str
        )

        messages.append({"role": "user", "content": input_as_str})
        return messages



    def _get_prediction(self, messages):
        chat_response =  self.openai_client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=ThreadPrompt.tools_thread ,
            tool_choice="required",
            temperature=1
        )
        assistant_message = chat_response.choices[0].message
        tool_call = assistant_message.tool_calls[0]
        arguments = json.loads(tool_call.function.arguments)
        return arguments[ThreadPrompt.SELECTED_GENERATOR_KEY]



    def test(self):
        messages = self.build_conversation()
        result  = self._get_prediction(messages)
        return result
