import os
import asyncio

from sanic import Sanic
from sanic.response import json

from logic import search_ingredient_in_wikipedia, create_ingredients_list_response, search_ingredient_not_found
import concurrent.futures

PORT = os.environ.get('PORT', 8000)
HOST = "0.0.0.0"

app = Sanic("product_scanner")
all_ingredient_responses = []

ingredients_to_query = {}


@app.post('/get_ingredients')
async def test(request):
    """
post function for web scrapping api , using threading to achieve faster web scrapping,
 get list of ingredient and return the json of IngredientResponse objects which contained description if found
 for each  ingredient
    :param request:list[str]
    :return:dict[IngredientResponse]
    """
    ingredients_to_query = request.json  # array of string

    loop = asyncio.get_event_loop()

    # thread pool in length of the request array of string
    executor = concurrent.futures.ThreadPoolExecutor(
        len(ingredients_to_query),
    )

    # list comprehension which create the ingredients array
    all_ingredient_responses = [
        loop.run_in_executor(executor, ingredient_to_dict, ingredient)
        # execute concurrency ingredient_to_dict function
        for ingredient in ingredients_to_query
    ]

    completed, pending = await asyncio.wait(all_ingredient_responses)
    results = [t.result() for t in completed]
    print("array length" + str(len(all_ingredient_responses)))

    return json(create_ingredients_list_response(results))


def ingredient_to_dict(ingredient):
    """
function that return IngredientResponse object which contain the ingredient data
    :param ingredient: str
    :return:ingredient_repose: IngredientResponse
    """
    print(ingredient)
    ingredient_repose = search_ingredient_in_wikipedia(ingredient)  # get the text from WIKIPEDIA if there is
    # white list to remove / charter from specific case for ingredient that doesnt have any page
    # or any other special charter
    whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ אבגדהוזחטיכלמנסעפצקרשתךףםןץ')

    if ingredient_repose is None:
        return None
    if not ingredient_repose.found:
        # get the ingredient options to select list
        ingredient_repose.maybe = search_ingredient_not_found(ingredient_repose.ingredient)
        # remove special charters
        ingredient_repose.ingredient = ''.join(filter(whitelist.__contains__, ingredient_repose.ingredient))
    print(ingredient_repose.description)
    return ingredient_repose


if __name__ == '__main__':
    print('enter')
    event_loop = asyncio.get_event_loop()  # Get the current event loop
    try:
        event_loop.run_until_complete(
            app.run(port=PORT, host=HOST))  # Run until the future (an instance of Future) has completed
    finally:
        event_loop.close()  # Close the event loop
