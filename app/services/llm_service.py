from openai import AsyncOpenAI, OpenAI
import os
import json
import uuid

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ToneManager:

    @staticmethod
    def create_signature( source_text: str) -> dict:
        """
            Generate tone signature using OpenAI
        """
        prompt = f"""
        Analyze the provided text and extract the Tone of Voice characteristics.
        Return JSON with these fields:
        - tone (e.g., professional, friendly)
        - language_style (e.g., technical, conversational) 
        - formality_level (0.0-1.0)
        - address_style (e.g., first-person, formal)
        - emotional_appeal (e.g., trust, excitement)
        The goal is to derive a consistent tone of voice from existing corporate communications that serves as the "signature" of the brand

        TEXT:
        {source_text}
        """

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[{
                "role": "user",
                "content": prompt
            }],
            response_format={"type": "json_object"},
            temperature=0.7
        )

        result = json.loads(response.choices[0].message.content)
        return {
            **result,
            "id": str(uuid.uuid4()),
            "source_text": source_text
        }

    @staticmethod
    def generate_text(signature: dict, user_prompt: str) -> str:
        """
            Generate text using signature
        """
        system_message = f"""
        Use the following guidelines to generate the response:
        - Tone: {signature['tone']}
        - Style: {signature['language_style']}
        - Formality: {signature['formality_level']}/1.0
        - Address: {signature['address_style']}
        - Emotional appeal: {signature['emotional_appeal']}
        """

        response = client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8
        )

        return response.choices[0].message.content