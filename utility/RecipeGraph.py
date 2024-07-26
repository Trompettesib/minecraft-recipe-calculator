from utility.Recipe import Recipe
from utility.Component import Component
import typing


class RecipeGraph:
    def __init__(self):
        self.components = {}

    def add_component(self, name: str):
        if name not in self.components:
            self.components[name] = Component(name)

    def __add_recipe(self, recipe: Recipe):
        for output in recipe.outputs:
            self.add_component(output)
            self.components[output].add_recipe(recipe)
        for input in recipe.inputs:
            self.add_component(input)

    def add_recipe(self, inputs: typing.Dict[str, int], outputs: typing.Dict[str, int]):
        recipe = Recipe(inputs, outputs)
        self.__add_recipe(recipe)

    def __repr__(self):
        return f"RecipeGraph(components={self.components})"

    def find_recipe(self, input: str, output: str) -> bool:
        if input not in self.components:
            return None
        if output not in self.components:
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
            for recipe in self.components[current].recipes:
                for input_name, _ in recipe.inputs.items():
                    stack.append(input_name)
        return None

    # Get the different path from output to input
    def get_paths(self, input: str, output: str):
        if input not in self.components:
            return None
        if output not in self.components:
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
            for recipe in self.components[current].recipes:
                for input_name, _ in recipe.inputs.items():
                    stack.append((input_name, path + [input_name]))
        return paths

    # Calculate the amount of input needed to produce the output quantity of a defined list of recipes:
    def calculate_input(
        self, entire_recipe: typing.List[str], output_quantity: int
    ) -> dict:
        byproduct = {}
        quantity = output_quantity
        entire_recipe_copy = entire_recipe.copy()
        output = entire_recipe_copy.pop(0)
        while len(entire_recipe_copy) > 0:
            from_input = entire_recipe_copy.pop(0)
            for recipe in self.components[output].recipes:
                if from_input in recipe.inputs:
                    for input_name, input_quantity in recipe.inputs.items():
                        multiplier = (
                            quantity / recipe.outputs[output]
                            if quantity % recipe.outputs[output] == 0
                            else quantity // recipe.outputs[output] + 1
                        )
                        byproduct[input_name] = (
                            byproduct[input_name] if input_name in byproduct else 0
                        ) + input_quantity * multiplier
                    quantity = recipe.inputs[from_input] * multiplier
                    output = from_input
                    break
        for key in list(byproduct.keys()):
            if self.components[key].recipes != [] and key != entire_recipe[-1]:
                del byproduct[key]
        return byproduct

    # Get the most efficient recipe to produce the output quantity of a defined list of recipes:
    def get_most_efficient_recipe(
        self, recipes: typing.List[typing.List[str]], output_quantity: int
    ) -> dict:
        min_global_ressources_input = None
        min_global_ressources_recipe = None
        min_input_ressource_input = None
        min_input_ressource_recipe = None
        inputs = []

        for recipe in recipes:
            inputs.append((self.calculate_input(recipe, output_quantity), recipe))

        # print(inputs)
        min_global_ressources_input = inputs[0][0]
        min_global_ressources_recipe = inputs[0][1]
        min_input_ressource_input = inputs[0][0]
        min_input_ressource_recipe = inputs[0][1]

        for input, recipe in inputs:
            better_global_ressources = False
            better_input_ressources = False

            # Compare total resource usage
            if sum(input.values()) < sum(min_global_ressources_input.values()):
                better_global_ressources = True

            # Compare input resource usage
            if input[recipe[-1]] < min_input_ressource_input[recipe[-1]]:
                better_input_ressources = True

            if better_global_ressources == True:
                min_global_ressources_input = input
                min_global_ressources_recipe = recipe
            if better_input_ressources == True:
                min_input_ressource_input = input
                min_input_ressource_recipe = recipe

        return {
            "global_ressources": {
                "min_input": min_global_ressources_input,
                "min_recipe": min_global_ressources_recipe,
            },
            "input_ressource": {
                "min_input": min_input_ressource_input,
                "min_recipe": min_input_ressource_recipe,
            },
        }
