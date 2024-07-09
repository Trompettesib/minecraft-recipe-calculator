import typing

class Recipe:
    def __init__(self, inputs: typing.Dict[str, int], outputs: typing.Dict[str, int]):
        self.inputs = inputs
        self.outputs = outputs

    def __repr__(self):
        return f"Recipe(inputs={self.inputs}, outputs={self.outputs})"