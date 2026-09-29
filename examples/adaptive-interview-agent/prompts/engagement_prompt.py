import textwrap
from agents.engagement.engagement_level import EngagementLevel


class EngagementEvaluationPrompt:

    FUNCTION_NAME = "engagement_level_handler"
    ANALYSIS_KEY = 'analysis'
    REASONING_KEY = 'reasoning'
    SELECTED_ENGAGEMENT_LEVEL_KEY = 'engagement_level'
    POSSIBLE_LEVEL_CLASSIFICATIONS = [EngagementLevel.LOW.value,
                                      EngagementLevel.MEDIUM.value,
                                      EngagementLevel.HIGH.value,
                                      EngagementLevel.NEUTRAL.value]
    REQUIRED_KEYS = [ANALYSIS_KEY, REASONING_KEY, SELECTED_ENGAGEMENT_LEVEL_KEY]

    SYSTEM_MESSAGE_ENGAGEMENT = textwrap.dedent(
    """
    # Role: Engagement Level Evaluator

    ## Objective:
    As a survey interaction specialist, your task is to evaluate the level of engagement shown by a participant based on the full conversation thread.
    This thread contains all interactions between the participant and the survey system.

    Your evaluation should be observational and grounded in the participant’s behavior. Engagement styles can differ—focus only on what is evident in the thread.
    Do not speculate beyond what is observable.

    ## Initial Analysis Guidelines:
    **Answer these questions—do not skip any**:
    1. How would you describe the participant's tone, energy, and consistency across the thread?
    2. Does the participant show signs of effort, attention, or emotional investment?
    3. Are there any patterns of engagement, disengagement, or fluctuation over time?

    ## Final Reasoning Guidelines:
    Based on the Initial Analysis, reason about which level is the most appropriate.
    Link your classification directly to the observed behavior in the thread.
    Do not overinterpret ambiguous or limited content.
    """
).strip()


    USER_MESSAGE_TEMPLATE = textwrap.dedent(
        """
        # Thread Content:

        {thread_content}
        """
    ).strip()

    tools_thread = [{
        "type": "function",
        "function": {
            "name": FUNCTION_NAME,
            "description": "Classifies the user's engagement level in the survey conversation.",
            "parameters": {
                "type": "object",
                "properties": {
                    ANALYSIS_KEY: {
                        "type": "string",
                        "description": "Based on the Initial Analysis Guidelines.",
                    },
                    REASONING_KEY: {
                        "type": "string",
                        "description": "Based on the Final Reasoning Guidelines.",
                    },
                    SELECTED_ENGAGEMENT_LEVEL_KEY: {
                        "type": "string",
                        "enum": ["high", "neutral", "low"],
                        "description": "The final selected engagement level.",
                    }
                },
                "required": REQUIRED_KEYS
            }
        }
    }]
