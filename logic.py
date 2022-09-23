import requests

from typing import List
from bs4 import BeautifulSoup
import threading

lock = threading.Lock()
from models import IngredientResponse

# WIKIPEDIA url page with the current ingredient
WIKIPEDIA_SEARCH_TEMPLATE = "https://he.wikipedia.org/wiki/{ingredient}"
# WIKIPEDIA search url page with the current ingredient that doesnt have any page
WIKIPEDIA_NOT_FOUND_TEMPLATE = "https://he.m.wikipedia.org/w/index.php?search={ingredient}&title=מיוחד%3Aחיפוש&ns0=1"
HTTP_SUCCESS = 200


def search_ingredient_in_wikipedia(ingredient: str) -> IngredientResponse:
    """
web scrapping function
    :param ingredient:str
    :return: IngredientResponse object
    """
    # requests WIKIPEDIA page for the ingredient
    response = requests.get(WIKIPEDIA_SEARCH_TEMPLATE.format(ingredient=ingredient))

    if response.status_code != HTTP_SUCCESS:
        return IngredientResponse(
            ingredient=ingredient,
            found=False
        )
    # get the html of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    # get the class which contained the first paragraph
    text = soup.find(class_="mw-parser-output")

    if text.find('p') is None:
        print('None')
        return None
    # get the text of the first paragraph
    ingredient_description = (text.find('p').get_text())
    # specific case for ingredient that doesnt have any page and need to add /
    # for later use in search_ingredient_not_found function
    ingredient = ingredient + '/' if ingredient_description.strip() == "האם התכוונתם ל..." else ingredient
    # boolean variable to detect if ingredient found or not
    found = ingredient_description != "" and ingredient_description.strip() != "האם התכוונתם ל..."

    print(ingredient)

    return IngredientResponse(
        ingredient=ingredient,
        found=found,
        description=ingredient_description if found else "",
    )


def create_ingredients_list_response(ingredient_responses: List[IngredientResponse]) -> dict:
    """
function that return dictionary with all the ingredient objects
    :param ingredient_responses: List[IngredientResponse]
    :return: response_dict:IngredientResponse dictionary
    """
    response_dict = {}
    # loop throw ingredient_responses array of ingredient objects
    for ingredient_response in ingredient_responses:
        if ingredient_response is not None:
            response_dict[ingredient_response.ingredient] = ingredient_response.to_dict()
    return response_dict


def search_ingredient_not_found(ingredient: str) -> list:
    """
function for ingredient that doesnt have any description,
loop throw html root_class in the WIKIPEDIA search page,
to get the ingredient options to select text , maximum of 4 options to select
    :param ingredient: str
    :return: list : str
    """
    # WIKIPEDIA search url page with the current ingredient that doesnt have any page
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
