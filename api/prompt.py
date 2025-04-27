import json
import requests

from fastapi import status

from app.ai import llm_interpreter
from app.config.settings import BASE_URL


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

    response = requests.get(f'{BASE_URL}/cars', params=parameters)

    if response.status_code == status.HTTP_200_OK:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    else:
        print(f"Error when filtering cars: {response.json()}")


if __name__ == '__main__':
    main()