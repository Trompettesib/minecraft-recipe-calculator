from utility.Recipe import Recipe

class Component:
    def __init__(self, name: str):
        self.name = name
        self.recipes = []

    def add_recipe(self, recipe: Recipe):
        self.recipes.append(recipe)

    def __repr__(self):
        return f"Component(name={self.name}, recipes={self.recipes})"
