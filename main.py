from utility.RecipeGraph import RecipeGraph

graph = RecipeGraph()

graph.add_recipe({'Oil': 25}, {'Sulfuric Light Fuel': 25})
graph.add_recipe({'Oil': 25}, {'Sulfuric Naphtha': 10})
graph.add_recipe({'Oil': 25}, {'Sulfuric Gas': 30})
graph.add_recipe({'Oil': 50}, {'Sulfuric Heavy Fuel': 15})
graph.add_recipe({'Oil': 12}, {'Lubricant': 6})


graph.add_recipe({'Sulfuric Light Fuel': 3000, 'Hydrogen': 500}, {'Light Fuel': 3000, 'Hydrogen Sulfide': 250})
graph.add_recipe({'Sulfuric Naphtha': 3000, 'Hydrogen': 500}, {'Naphtha': 3000, 'Hydrogen Sulfide': 250})
graph.add_recipe({'Sulfuric Gas': 2000, 'Hydrogen': 250}, {'Refinery Gas': 2000, 'Hydrogen Sulfide': 125})
graph.add_recipe({'Sulfuric Heavy Fuel': 1000, 'Hydrogen': 250}, {'Heavy Fuel': 1000, 'Hydrogen Sulfide': 125})


graph.add_recipe({'Light Fuel': 1000, 'Hydrogen': 2000}, {'Lightly Hydro-Cracked Light Fuel': 800})
graph.add_recipe({'Light Fuel': 1000, 'Hydrogen': 4000}, {'Moderately Hydro-Cracked Light Fuel': 800})
graph.add_recipe({'Light Fuel': 1000, 'Hydrogen': 6000}, {'Severely Hydro-Cracked Light Fuel': 800})

graph.add_recipe({'Light Fuel': 1000, 'Steam': 1000}, {'Lightly Steam-Cracked Light Fuel': 800})
graph.add_recipe({'Light Fuel': 1000, 'Steam': 1000}, {'Moderately Steam-Cracked Light Fuel': 800})
graph.add_recipe({'Light Fuel': 1000, 'Steam': 1000}, {'Severely Steam-Cracked Light Fuel': 800})


graph.add_recipe({'Naphtha': 1000, 'Hydrogen': 2000}, {'Lightly Hydro-Cracked Naphtha': 800})
graph.add_recipe({'Naphtha': 1000, 'Hydrogen': 4000}, {'Moderately Hydro-Cracked Naphtha': 800})
graph.add_recipe({'Naphtha': 1000, 'Hydrogen': 6000}, {'Severely Hydro-Cracked Naphtha': 800})

graph.add_recipe({'Naphtha': 1000, 'Steam': 1000}, {'Lightly Steam-Cracked Naphtha': 800})
graph.add_recipe({'Naphtha': 1000, 'Steam': 1000}, {'Moderately Steam-Cracked Naphtha': 800})
graph.add_recipe({'Naphtha': 1000, 'Steam': 1000}, {'Severely Steam-Cracked Naphtha': 800})


graph.add_recipe({'Refinery Gas': 1000, 'Hydrogen': 2000}, {'Lightly Hydro-Cracked Refinery Gas': 800})
graph.add_recipe({'Refinery Gas': 1000, 'Hydrogen': 4000}, {'Moderately Hydro-Cracked Refinery Gas': 800})
graph.add_recipe({'Refinery Gas': 1000, 'Hydrogen': 6000}, {'Severely Hydro-Cracked Refinery Gas': 800})

graph.add_recipe({'Refinery Gas': 1000, 'Steam': 1000}, {'Lightly Steam-Cracked Refinery Gas': 800})
graph.add_recipe({'Refinery Gas': 1000, 'Steam': 1000}, {'Moderately Steam-Cracked Refinery Gas': 800})
graph.add_recipe({'Refinery Gas': 1000, 'Steam': 1000}, {'Severely Steam-Cracked Refinery Gas': 800})


graph.add_recipe({'Lightly Hydro-Cracked Light Fuel': 100}, {'Butane': 15})
graph.add_recipe({'Moderately Hydro-Cracked Light Fuel': 100}, {'Butane': 20})
graph.add_recipe({'Severely Hydro-Cracked Light Fuel': 200}, {'Butane': 25})
graph.add_recipe({'Refinery Gas': 50}, {'Butane': 3})
graph.add_recipe({'Lightly Hydro-Cracked Naphtha': 100}, {'Butane': 80})

graph.add_recipe({'Severely Steam-Cracked Naphtha': 1000}, {'Ethylene': 500})
graph.add_recipe({'Severely Steam-Cracked Refinery Gas': 1000}, {'Ethylene': 300})



mode = input("Available modes:\n1 for input/output\nPlease select a mode: ")
if mode == "1":
    input_component = input("Enter the input component: ")
    output_component = input("Enter the output component: ")
    if not graph.find_recipe(input_component, output_component):
        print(f"No path found from {input_component} to {output_component}")
        print("Exiting...")
        exit()

    paths = graph.get_paths(input_component, output_component)
    output_quantity = int(input("Enter the output quantity wanted: "))
    min_input, min_recipe = graph.get_most_efficient_recipe(paths, output_quantity)
    print(f"The quantity of raw material for the most efficient recipe found to produce {output_quantity} {output_component}:")
    for key, value in min_input.items():
        print(f"{value} {key}")
    print("Recipe is :")
    for component in reversed(min_recipe):
        print(component)

else:
    print("Mode not supported. Exiting...")