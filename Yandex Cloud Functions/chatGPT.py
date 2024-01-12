import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")
)

async def get_analysis(message):

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poetic assistant, skilled in saying Hello in different languages."},
            {"role": "user", "content": message}
        ]
    )

    return completion.choices[0].message.content
