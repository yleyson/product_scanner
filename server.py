import os

from sanic import Sanic
from sanic.response import json

from logic import search_ingredient_in_wikipedia, create_ingredients_list_response, search_ingredient_not_found
import concurrent.futures
from concurrent.futures import wait
import threading

lock = threading.Lock()
PORT = os.environ.get('PORT', 8000)
HOST = "0.0.0.0"

app = Sanic("product_scanner")

all_ingredient_responses = []

ingredients_to_query={}
@app.post('/get_ingredients')
async def test(request):
    ingredients_to_query = request.json
    print(ingredients_to_query)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(ingredient_to_dict,ingredients_to_query)
        print('Waiting...')
    print(all_ingredient_responses)
    return json(create_ingredients_list_response(all_ingredient_responses))


def ingredient_to_dict(ingredient):
        ingredient_repose = search_ingredient_in_wikipedia(ingredient)
        if ingredient_repose is None:
            return
        if not ingredient_repose.found:
            ingredient_repose.maybe = search_ingredient_not_found(ingredient_repose.ingredient)
        print(ingredient_repose)
        all_ingredient_responses.append(ingredient_repose)


if __name__ == '__main__':
    app.run(port=PORT, host=HOST)
