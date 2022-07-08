import requests

from typing import List
from bs4 import BeautifulSoup
import threading
lock = threading.Lock()
from models import IngredientResponse
response_dict = {}


WIKIPEDIA_SEARCH_TEMPLATE = "https://he.wikipedia.org/wiki/{ingredient}"
WIKIPEDIA_NOT_FOUND_TEMPLATE = "https://he.m.wikipedia.org/w/index.php?search={ingredient}&title=מיוחד%3Aחיפוש&ns0=1"
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

    if text.find('p') is None:
        return None

    ingredient_description = (text.find('p').get_text())

    ingredient = ingredient + '/' if ingredient_description.strip() == "האם התכוונתם ל..." else ingredient

    found = ingredient_description != "" and ingredient_description.strip() != "האם התכוונתם ל..."

    return IngredientResponse(
        ingredient=ingredient,
        found=found,
        description=ingredient_description if found else "",
    )


def create_ingredients_list_response(ingredient_responses: List[IngredientResponse]) -> dict:

    for ingredient_response in ingredient_responses:
        lock.acquire()
        try:
            response_dict[ingredient_response.ingredient] = ingredient_response.to_dict()
        finally:
            # Always called, even if exception is raised in try block
            lock.release()
        print(ingredient_response.ingredient)
    return response_dict


def search_ingredient_not_found(ingredient: str) -> list:
    response = requests.get(WIKIPEDIA_NOT_FOUND_TEMPLATE.format(ingredient=ingredient))
    if response.status_code != HTTP_SUCCESS:
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    root_class = soup.findAll(class_="mw-search-result-heading")
    length = 4 if len(root_class) > 4 else len(root_class)
    ing_option_list = []

    for i in range(length):
        ing_option_list.append(root_class[i].find('a').get_text())
    return ing_option_list
