
from openai import OpenAI

from app import app, Constants

client = OpenAI(api_key=app.config.get(Constants.TOGETHER_AI_API_KEY),
                base_url='https://api.together.xyz',
                )


class LLMService:

    @staticmethod
    def get_response(prompt: str) -> str:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",

                    "content": prompt
                }
            ],
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            temperature=0.9,
            top_p=0.9,
            max_tokens=1024)
        print(chat_completion)

        return chat_completion.choices[0].message.content
