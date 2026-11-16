import json

from groq import Groq
from pydantic import ValidationError

from prompts import CAREER_ADVISOR_PROMPT
from models import CareerAdvice


def get_career_advice(client: Groq, user_profile: str) -> CareerAdvice:

    prompt = CAREER_ADVISOR_PROMPT.format(
        user_profile=user_profile
    )

    try:

        response = client.chat.completions.create(
            model = "openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        raw_response = response.choices[0].message.content

        data = json.loads(raw_response)

        career_advice = CareerAdvice.model_validate(data)

        return career_advice

    except json.JSONDecodeError as e:

        raise ValueError(
            "The AI returned an invalid JSON response."
        ) from e

    except ValidationError as e:

        raise ValueError(
            "The AI response did not match the expected format."
        ) from e

    except Exception as e:

        raise RuntimeError(
            f"Unable to generate career advice: {str(e)}"
        ) from e