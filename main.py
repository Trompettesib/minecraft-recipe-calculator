from utility.RecipeGraph import RecipeGraph
from utility.Recipe import Recipe
import typing

def add_recipe(graph: RecipeGraph, inputs: typing.Dict[str, int], outputs: typing.Dict[str, int]):
    recipe = Recipe(inputs, outputs)
    graph.add_recipe(recipe)

# Example
graph = RecipeGraph()

add_recipe(graph, {'Oil': 25}, {'Sulfuric Light Fuel': 25})
add_recipe(graph, {'Oil': 25}, {'Sulfuric Naphtha': 10})
add_recipe(graph, {'Oil': 25}, {'Sulfuric Gas': 30})
add_recipe(graph, {'Oil': 50}, {'Sulfuric Heavy Fuel': 15})
add_recipe(graph, {'Oil': 12}, {'Lubricant': 6})


add_recipe(graph, {'Sulfuric Light Fuel': 3000, 'Hydrogen': 500}, {'Light Fuel': 3000, 'Hydrogen Sulfide': 250})
add_recipe(graph, {'Sulfuric Naphtha': 3000, 'Hydrogen': 500}, {'Naphtha': 3000, 'Hydrogen Sulfide': 250})
add_recipe(graph, {'Sulfuric Gas': 2000, 'Hydrogen': 250}, {'Refinery Gas': 2000, 'Hydrogen Sulfide': 125})
add_recipe(graph, {'Sulfuric Heavy Fuel': 1000, 'Hydrogen': 250}, {'Heavy Fuel': 1000, 'Hydrogen Sulfide': 125})


add_recipe(graph, {'Light Fuel': 1000, 'Hydrogen': 2000}, {'Lightly Hydro-Cracked Light Fuel': 800})
add_recipe(graph, {'Light Fuel': 1000, 'Hydrogen': 4000}, {'Moderately Hydro-Cracked Light Fuel': 800})
add_recipe(graph, {'Light Fuel': 1000, 'Hydrogen': 6000}, {'Severely Hydro-Cracked Light Fuel': 800})

add_recipe(graph, {'Light Fuel': 1000, 'Steam': 1000}, {'Lightly Steam-Cracked Light Fuel': 800})
add_recipe(graph, {'Light Fuel': 1000, 'Steam': 1000}, {'Moderately Steam-Cracked Light Fuel': 800})
add_recipe(graph, {'Light Fuel': 1000, 'Steam': 1000}, {'Severely Steam-Cracked Light Fuel': 800})


add_recipe(graph, {'Lightly Hydro-Cracked Light Fuel': 100}, {'Butane': 15})
add_recipe(graph, {'Moderately Hydro-Cracked Light Fuel': 100}, {'Butane': 20})
add_recipe(graph, {'Severely Hydro-Cracked Light Fuel': 200}, {'Butane': 25})
add_recipe(graph, {'Refinery Gas': 50}, {'Butane': 3})
add_recipe(graph, {'Lightly Hydro-Cracked Naphtha': 100}, {'Butane': 80})
add_recipe(graph, {'Naphtha': 1000, 'Hydrogen': 2000}, {'Lightly Hydro-Cracked Naphtha': 800})
# add recipe for Lubricant with 12 Oil that produce 6 Lubricant


input = 'Oil'
output = 'Butane'

def find_recipe(graph: RecipeGraph, input: str, output: str) -> bool:
    if input not in graph.components:
        return None
    if output not in graph.components:
        return None

    # Research path from output to input
    visited = set()
    stack = [output]
    while stack:
        current = stack.pop()
        if current == input:
            return True
        if current in visited:
            continue
        visited.add(current)
        for recipe in graph.components[current].recipes:
            for input_name, _ in recipe.inputs.items():
                stack.append(input_name)
    return None


# print(find_recipe(graph, input, output))

# Get the different path from output to input
def get_paths(graph: RecipeGraph, input: str, output: str):
    if input not in graph.components:
        return None
    if output not in graph.components:
        return None

    # Research all paths from output to input
    visited = set()
    stack = [(output, [output])]
    paths = []
    while stack:
        current, path = stack.pop()
        if current == input:
            paths.append(path)
        visited.add(current)
        for recipe in graph.components[current].recipes:
            for input_name, _ in recipe.inputs.items():
                stack.append((input_name, path + [input_name]))
    return paths

paths = get_paths(graph, input, output)
# print(paths)

# Calculate the amount of input needed to produce the output quantity of a defined list of recipes:
def calculate_input(graph: RecipeGraph, entire_recipe: typing.List[str], output_quantity: int) -> dict:
    byproduct = {}
    quantity = output_quantity
    entire_recipe_copy = entire_recipe.copy()
    output = entire_recipe_copy.pop(0)
    while len(entire_recipe_copy) > 0:
        from_input = entire_recipe_copy.pop(0)
        for recipe in graph.components[output].recipes:
            if from_input in recipe.inputs:
                for input_name, input_quantity in recipe.inputs.items():
                    multiplier = quantity / recipe.outputs[output] if quantity % recipe.outputs[output] == 0 else quantity // recipe.outputs[output] + 1
                    byproduct[input_name] = (byproduct[input_name] if input_name in byproduct else 0) + input_quantity * multiplier
                quantity = recipe.inputs[from_input] * multiplier
                output = from_input
                break
    for key in list(byproduct.keys()):
        if graph.components[key].recipes != []:
            del byproduct[key]
    return byproduct

# print(calculate_input(graph, ['Butane', 'Lightly Hydro-Cracked Light Fuel', 'Light Fuel', 'Sulfuric Light Fuel', 'Oil'], 100))

# Get the most efficient recipe to produce the output quantity of a defined list of recipes:
def get_most_efficient_recipe(graph: RecipeGraph, recipes: typing.List[typing.List[str]], output_quantity: int) -> typing.Tuple[dict, typing.List[str]]:
    min_input = None
    min_recipe = None
    inputs = []

    for recipe in recipes:
        inputs.append((calculate_input(graph, recipe, output_quantity), recipe))
    min_input = inputs[0][0]
    min_recipe = inputs[0][1]

    for input, recipe in inputs:
        better = False
        for key in list(input.keys()):
            if min_input[key] <= input[key]:
                better = False
            if min_input[key] > input[key]:
                better = True
                break
        if better == True:
            min_input = input
            min_recipe = recipe

    return min_input, min_recipe

print(get_most_efficient_recipe(graph, paths, 100))