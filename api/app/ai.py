import json

from openai import OpenAI
from typing import Optional

from app.models.enums import Transmission, Fuel
from app.config.settings import OPEN_AI_API_KEY


def llm_interpreter(sentence: str) -> dict:
    """
    This function uses OpenAI's API to interpret a given sentence and extract car filters.

    Args:
        sentence (str): The input sentence containing car search details.

    Returns:
        dict: A dictionary containing the extracted filters.
    """
    prompt = f"""
    Voce é um agente que ajuda a buscar veículos em um banco de dados.
    Dado o texto abaixo, extraia os possíveis filtros e retorne em formato JSON:

    {{
        "brand": str | null,
        "model": str | null,
        "year": int | null,
        "engine": str | null,
        "fuel": str | null, // "FLEX", "GASOLINE", "HYBRID", "ELECTRIC" or "DIESEL"
        "color": str | null,
        "mileage": int | null,
        "doors": int | null,
        "transmission": str | null, // "MANUAL", "AUTOMATIC" or "CVT"
        "price": float | null,
    }}

    Texto: "{sentence}"
    """
    client = OpenAI(api_key=OPEN_AI_API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": sentence}
            ],
            response_format={"type": "json_object"},
        )
        parameters = json.loads(response.choices[0].message.content)

        if 'transmission' in parameters:
            parameters['transmission'] = validate_transmission(parameters['transmission'])
        if 'fuel' in parameters:
            parameters['fuel'] = validate_fuel(parameters['fuel'])

        return parameters
    except Exception as e:
        print(f"Error when calling Open AI: {e}")
        return {}


def validate_transmission(transmission: Optional[str] = None) -> str:
    try:
        return Transmission[transmission.upper()].value
    except (KeyError, AttributeError):
        return None


def validate_fuel(fuel: Optional[str] = None) -> str:
    try:
        return Fuel[fuel.upper()].value
    except (KeyError, AttributeError):
        return None