from sanic import Sanic
from sanic.response import json

from logic import search_ingredient_in_wikipedia, create_ingredients_list_response


app = Sanic("product_scanner")


@app.post('/get_ingredients')
async def test(request):

    ingredients_to_query = request.json

    all_ingredient_responses = []

    for ingredient in ingredients_to_query:
        ingredient_repose = search_ingredient_in_wikipedia(ingredient)
        print(ingredient_repose)
        all_ingredient_responses.append(search_ingredient_in_wikipedia(ingredient))

    return json(create_ingredients_list_response(all_ingredient_responses))


if __name__ == '__main__':
    app.run()
