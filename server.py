import os
import asyncio
import re

from sanic import Sanic
from sanic.response import json

from logic import search_ingredient_in_wikipedia, create_ingredients_list_response, search_ingredient_not_found
import concurrent.futures
import threading

PORT = os.environ.get('PORT', 8000)
HOST = "0.0.0.0"

app = Sanic("product_scanner")
all_ingredient_responses = []

ingredients_to_query = {}


@app.post('/get_ingredients')
async def test(request):
    ingredients_to_query = request.json

    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(
        len(ingredients_to_query),
    )

    all_ingredient_responses = [
        loop.run_in_executor(executor, ingredient_to_dict2, ingredient)
        for ingredient in ingredients_to_query
    ]



    completed,pending = await asyncio.wait(all_ingredient_responses)
    results = [t.result() for t in completed]
    print("array length" + str(len(all_ingredient_responses)))

    return json(create_ingredients_list_response(results))


def ingredient_to_dict(ingredients_to_query):
    for ingredient in ingredients_to_query:
        ingredient_repose = search_ingredient_in_wikipedia(ingredient)
        if ingredient_repose is None:
            return None
        if not ingredient_repose.found:
            ingredient_repose.maybe = search_ingredient_not_found(ingredient_repose.ingredient)
        all_ingredient_responses.append(ingredient_repose)


def ingredient_to_dict2(ingredient):
    print(ingredient)
    ingredient_repose = search_ingredient_in_wikipedia(ingredient)
    if ingredient_repose is None:
        return None
    if not ingredient_repose.found:
        ingredient_repose.maybe = search_ingredient_not_found(ingredient_repose.ingredient)
    print(ingredient_repose.description)
    ingredient_repose.ingredient=re.sub("[/\W]+", '', ingredient_repose.ingredient)
    return ingredient_repose


if __name__ == '__main__':
    print('enter')
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(app.run(port=PORT, host=HOST))
    finally:
        event_loop.close()
