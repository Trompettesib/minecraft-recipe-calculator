from utility.Recipe import Recipe
from utility.Component import Component

class RecipeGraph:
    def __init__(self):
        self.components = {}

    def add_component(self, name: str):
        if name not in self.components:
            self.components[name] = Component(name)

    def add_recipe(self, recipe: Recipe):
        for output in recipe.outputs:
            self.add_component(output)
            self.components[output].add_recipe(recipe)
        for input in recipe.inputs:
            self.add_component(input)

    def __repr__(self):
        return f"RecipeGraph(components={self.components})"
