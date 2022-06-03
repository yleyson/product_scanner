import requests

from typing import List
from bs4 import BeautifulSoup

from models import IngredientResponse


WIKIPEDIA_SEARCH_TEMPLATE = "https://he.wikipedia.org/wiki/{ingredient}"
HTTP_SUCCESS = 200


def search_ingredient_in_wikipedia(ingredient: str) -> IngredientResponse:
    response = requests.get(WIKIPEDIA_SEARCH_TEMPLATE.format(ingredient=ingredient))

    if response.status_code != HTTP_SUCCESS:
        return IngredientResponse(
            ingredient=ingredient,
            found=False
        )

    soup = BeautifulSoup(response.content, 'html.parser')

    text = soup.find(class_="mw-parser-output")

    ingredient_description = (text.find('p').get_text())

    found = ingredient_description != ""

    return IngredientResponse(
        ingredient=ingredient,
        found=found,
        description=ingredient_description,
    )


def create_ingredients_list_response(ingredient_responses: List[IngredientResponse]) -> dict:
    response = {}
    for ingredient_response in ingredient_responses:
        response[ingredient_response.ingredient] = ingredient_response.to_dict()

    return response
