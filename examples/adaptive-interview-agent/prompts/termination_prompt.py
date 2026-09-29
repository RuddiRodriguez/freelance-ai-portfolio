import textwrap


class ConversationFlowJudgmentPrompt:

    FUNCTION_NAME = "conversation_flow_decision_handler"
    ANALYSIS_KEY = 'analysis'
    REASONING_KEY = 'reasoning'
    DECISION_KEY = 'conversation_decision'
    REQUIRED_KEYS = [ANALYSIS_KEY, REASONING_KEY, DECISION_KEY]
    POSSIBLE_DECISIONS = ["terminate_conversation", "continue_conversation"]

    SYSTEM_MESSAGE_FLOW_DECISION = textwrap.dedent(
    """
    # Role: Conversation Flow Judge

    ## Objective:
    Your task is to decide whether the conversation with a survey participant should be terminated or allowed to continue.
    You are given three inputs:
    - The participant's **engagement level**
    - The participant's **sensitivity level**
    - The participant's **sufficiency level**
    - The full conversation thread

    Your decision must be based only on these inputs. Do not speculate beyond what these values imply.

    ## Initial Analysis Guidelines:
    **Answer these questions — do not skip any**:
    1. What is the sensitivity level and what does it suggest about emotional boundaries?
    2. What is the engagement level and what does it suggest about the participant's willingness to continue?
    3. What is the sufficiency level and what does it suggest about the depth or clarity of the participant's response?
    4. Does the conversation thread indicate any signs of distress, discomfort, or disengagement from the participant?
    5. Does the conversation thread achieve partially or fully the survey's objectives?

    ## Final Reasoning Guidelines:
    Based on your analysis, reason whether continuing or terminating the conversation is the most respectful and effective option.
    Focus on balancing participant well-being, willingness to engage, and the usefulness of the response.
    """
).strip()


    USER_MESSAGE_TEMPLATE = textwrap.dedent(
        """
        # Participant Interaction Summary:

        Sensitivity Level: {sensitivity_level}
        Engagement Level: {engagement_level}
        Sufficiency Level: {sufficiency_level}

        # Thread Content:

        {thread_content}

        """
    ).strip()

    tools_thread = [{
        "type": "function",
        "function": {
            "name": FUNCTION_NAME,
            "description": "Decides whether the conversation should be continued or terminated based on sensitivity and engagement levels.",
            "parameters": {
                "type": "object",
                "properties": {
                    ANALYSIS_KEY: {
                        "type": "string",
                        "description": "Analysis based on the sensitivity and engagement levels.",
                    },
                    REASONING_KEY: {
                        "type": "string",
                        "description": "Justification for the final decision.",
                    },
                    DECISION_KEY: {
                        "type": "string",
                        "enum": POSSIBLE_DECISIONS,
                        "description": "Final decision: either terminate or continue the conversation.",
                    }
                },
                "required": REQUIRED_KEYS
            }
        }
    }]
