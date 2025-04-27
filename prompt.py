import os
import requests

from dotenv import load_dotenv
from fastapi import status

from app.models.enums import Transmission, Fuel

load_dotenv()


def llm_interpreter(message: str) -> dict:
    # TODO: LLM integration
    return {
        "brand": "FIAT",
        "model": "PUNTO",
    }


def validate_transmission(transmission: str) -> str:
    try:
        return Transmission[transmission.upper()].value
    except KeyError:
        return None


def validate_fuel(fuel: str) -> str:
    try:
        return Fuel[fuel.upper()].value
    except KeyError:
        return None


def main():
    """
    Main function to interact with the user and fetch car data.
    """
    sentence = input("Qual carro está procurando? ")
    parameters = llm_interpreter(sentence)
    
    if 'transmission' in parameters:
        parameters['transmission'] = validate_transmission(parameters['transmission'])
    
    if 'fuel' in parameters:
        parameters['fuel'] = validate_fuel(parameters['fuel'])
    
    response = requests.get(f'{os.getenv("BASE_URL")}/cars', params=parameters)
    
    if response.status_code == status.HTTP_200_OK:
        print(response.json())
    else:
        print(f"Error: {response.status_code}")


if __name__ == '__main__':
    main()