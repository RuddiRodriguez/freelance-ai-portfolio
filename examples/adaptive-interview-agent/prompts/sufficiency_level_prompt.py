
import textwrap
from agents.sufficiency.sufficiency_level import SufficiencyLevel

class SufficiencyLevelPrompt:

    FUNCTION_NAME = "sufficiency_level_handler"
    ANALYSIS_KEY = 'initial_analysis'
    REASONING_KEY = 'reasoning'
    SELECTED_LEVEL_CLASSIFICATION_KEY = 'sufficiency_level'
    REQUIRED_KEYS = [ANALYSIS_KEY, REASONING_KEY, SELECTED_LEVEL_CLASSIFICATION_KEY]
    POSSIBLE_LEVEL_CLASSIFICATIONS = [SufficiencyLevel.INSUFFICIENT.value,
                                      SufficiencyLevel.SOMEWHAT_INSUFFICIENT.value,
                                      SufficiencyLevel.MODERATE.value,
                                      SufficiencyLevel.SOMEWHAT_SUFFICIENT.value,
                                      SufficiencyLevel.SUFFICIENT.value]

    SYSTEM_MESSAGE = textwrap.dedent(
    f"""
    # Role: Sufficiency Analysis

    ## Objective:
    As a market research expert, your task is to evaluate the sufficiency level of a Response to a given Question.
    You will assess the clarity and completeness of the Response, and make your judgment based on that.
    The Question is from an online survey, and the Response is from a human who submitted this Response on their computer.

    Your evaluation should be inclusive and open-minded, respecting the diverse ways in which respondents may express their thoughts and opinions.
    Responses can be lazy and vague, it is OK, be lenient and don't look for tiny details.
    Some questions may contain phrases like "provide lots of details".
    Ignore these phrases, as real respondents are unlikely to provide extensive information.
    People tend to be brief and to the point in their responses.


    ## Evaluation Guidelines:
    1. **Choose {SufficiencyLevel.INSUFFICIENT.value} if**:
    - The Response is completely off topic.
    - The response is extremely lacking.

    2. **Choose {SufficiencyLevel.SOMEWHAT_INSUFFICIENT.value} if**:
    - The Response addresses the Question with a single detail.

    3. **Choose {SufficiencyLevel.MODERATE.value} if**:
    - The Response addresses the Question with two details.

    4. **Choose {SufficiencyLevel.SOMEWHAT_SUFFICIENT.value} if**:
    - The Response addresses the Question with three details.

    5. **Choose {SufficiencyLevel.SUFFICIENT.value} if**:
    - The Response addresses the Question with four or more details.

    ## Initial Analysis Guidelines:
    **Answer these questions, don't skip any**:
    1. Is the Response implicit or explicit?
    2. Does the Response address the Question?
    3. How many unique details are in the Response?

    ## Final Reasoning Guidelines:
    Based on the Initial Analysis, reason about which level is the most appropriate.
    """).strip()



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
            "description": "Classifies the user's level of sufficiency in the survey conversation.",
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
                        "description": "The final selected sufficiency level.",
                    }
                },
                "required": REQUIRED_KEYS
            }
        }
    }]
