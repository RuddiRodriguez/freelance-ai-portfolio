import textwrap
from agents.sensitivity.sensitivity_level import SensitivityLevel


class SensitivityEvaluationPrompt:

    FUNCTION_NAME = "sensitivity_level_handler"
    ANALYSIS_KEY = 'analysis'
    REASONING_KEY = 'reasoning'
    SELECTED_LEVEL_CLASSIFICATION_KEY = 'sensitivity_level'
    REQUIRED_KEYS = [ANALYSIS_KEY, REASONING_KEY, SELECTED_LEVEL_CLASSIFICATION_KEY]
    POSSIBLE_LEVEL_CLASSIFICATIONS = [SensitivityLevel.NOT_SENSITIVE.value,
                                      SensitivityLevel.INAPPLICABLE.value,
                                      SensitivityLevel.SENSITIVE.value]

    SYSTEM_MESSAGE_SENSITIVITY = textwrap.dedent(
    f"""
    # Role: Sensitivity Evaluator

    ## Objective:
    As a survey response specialist, your task is to evaluate whether the participant’s response contains sensitive content.
    The input is a single open-ended survey response submitted by a human participant online.

    Your evaluation should focus only on the content provided—do not speculate or infer beyond the text itself.
    Some responses may be short or vague; assess them carefully before deciding.

    ## Sensitivity Level Guidelines:
    1. **Choose {SensitivityLevel.SENSITIVE.value} if**:
       - The response includes any of the following:
         - Personal Trauma (e.g., distressing experiences, trauma, fear, pain)
         - Loss or Grief (e.g., death, separation, mourning)
         - Personal Privacy Concerns (e.g., "too personal", "I’d rather not say")
         - Sensitive Personal Life Events (e.g., emotional situations that feel private or intimate)
         - Worrisome expressions (e.g., anxiety, feeling unsafe, worried)

    2. **Choose {SensitivityLevel.NOT_SENSITIVE.value} if**:
       - The response contains no indicators of sensitive emotional content or personal distress.

    3. **Choose {SensitivityLevel.INAPPLICABLE.value} if**:
       - The response is too short, vague, or ambiguous to determine whether sensitivity is present.

    ## Initial Analysis Guidelines:
    **Answer these questions—do not skip any**:
    1. Does the response include emotionally charged language or descriptions?
    2. Are any topics raised that may relate to trauma, loss, privacy, or emotional distress?
    3. Is the response explicit, implicit, or ambiguous in its meaning?

    ## Final Reasoning Guidelines:
    Based on the Initial Analysis, reason about which sensitivity level is most appropriate.
    Reference the content directly and avoid guessing at unstated meaning.
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
            "description": "Classifies the user's level of sensitivity in the survey conversation.",
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
                    SELECTED_LEVEL_CLASSIFICATION_KEY: {
                        "type": "string",
                        "enum": POSSIBLE_LEVEL_CLASSIFICATIONS,
                        "description": "The final selected sensitivity level.",
                    }
                },
                "required": REQUIRED_KEYS
            }
        }
    }]
