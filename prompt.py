import json
import requests

from fastapi import status
from openai import OpenAI
from typing import Optional

from app.models.enums import Transmission, Fuel
from app.settings import BASE_URL, OPEN_AI_API_KEY


def llm_interpreter(sentence: str) -> dict:
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
        return json.loads(response.choices[0].message.content)
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


def main():
    """
    Main function to interact with the user and fetch car data.
    """
    brand = input("Qual marca e modelo do carro que você está buscando? ")
    year = input("Qual ano do carro? ")
    price = input("Qual o preço máximo que você está disposto a pagar? ")
    other_info = input("Mais algum detalhe para sua busca (câmbio, motor, cor, etc)? ")

    parameters = llm_interpreter(
        f"""
        Busque um carro com os seguintes detalhes:
        Marca/Modelo: {brand}
        Ano: {year}
        Preço: {price}
        Outros detalhes: {other_info}
        """
    )

    if 'transmission' in parameters:
        parameters['transmission'] = validate_transmission(parameters['transmission'])
    
    if 'fuel' in parameters:
        parameters['fuel'] = validate_fuel(parameters['fuel'])
    
    response = requests.get(f'{BASE_URL}/cars', params=parameters)
    
    if response.status_code == status.HTTP_200_OK:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Error: {response.status_code}")


if __name__ == '__main__':
    main()