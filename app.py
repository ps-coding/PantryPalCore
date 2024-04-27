import tkinter as tk
from tkinter import messagebox
import pandas as pd

data = pd.read_csv('RAW_recipes.csv').values.tolist()


def filter_by_ingredients(available_ingredients):
    can_make = []

    for recipe in data:
        recipe_ingredients = map(lambda x: x.strip("'"),
                                 recipe[10].strip('][').split(', '))

        if all(map(lambda x: x in available_ingredients, recipe_ingredients)):
            can_make.append(recipe)

    return can_make


def add_ingredient():
    ingredient = ingredient_entry.get()
    if ingredient:
        ingredients.append(ingredient)
        ingredients_listbox.insert(tk.END, ingredient.upper())
        ingredient_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter an ingredient.")


def remove_ingredient():
    selected_index = ingredients_listbox.curselection()
    if selected_index:
        ingredients.pop(selected_index[0])
        ingredients_listbox.delete(selected_index)
    else:
        messagebox.showwarning("Warning", "Please select an ingredient to remove.")


def make_meal():
    if ingredients:
        Recipes(root, filter_by_ingredients(ingredients))
    else:
        messagebox.showwarning("Warning", "Please add ingredients first.")


class Recipes(tk.Toplevel):
    def __init__(self, master = None, recipes = []):
        super().__init__(master = master)
        self.title("Recipes")
        self.recipes = recipes
        label = tk.Label(self, text ="Recipes")
        label.pack()
        self.listbox = tk.Listbox(self)
        self.listbox.pack(expand = True)
        for recipe in self.recipes:
            self.listbox.insert(tk.END, recipe[0].upper())

        detailsButton = tk.Button(self, text = "Details", command = self.show_details)
        detailsButton.pack()

    def show_details(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            RecipeDetail(self, self.recipes[selected_index[0]])
        else:
            messagebox.showwarning("Warning", "Please select a recipe to view details.")

class RecipeDetail(tk.Toplevel):
    def __init__(self, master = None, recipe = None):
        super().__init__(master = master)
        self.title("Recipe Details")

        recipeName = tk.Label(self, text = recipe[0].upper())
        recipeName.pack()

        minutesLabel = tk.Label(self, text = "TIME: " + str(int((recipe[1]) / 3600)) + " MINUTES")
        minutesLabel.pack()

        if (isinstance(recipe[9], str)):
            contributorTitle = tk.Label(self, text="CONTRIBUTOR DESCRIPTION")
            contributorTitle.pack()

            contributorDescription = tk.Text(self, wrap=tk.WORD, height=3)
            contributorDescription.pack()
            contributorDescription.insert(tk.END, recipe[9].upper())
            contributorDescription.config(state=tk.DISABLED)

        stepsTitle = tk.Label(self, text = "INSTRUCTIONS TO MAKE")
        stepsTitle.pack()
        stepsList = tk.Listbox(self)
        stepsList.pack(expand = True, fill=tk.X)
        steps = recipe[8].strip('][').split(', ')
        for step in steps:
            stepsList.insert(tk.END, step.strip("'").upper())
        stepsList.config(state=tk.DISABLED)

        ingredientsTitle = tk.Label(self, text = "INGREDIENTS")
        ingredientsTitle.pack()
        ingredientsList = tk.Listbox(self)
        ingredientsList.pack(expand = True)
        ingredients = recipe[10].strip('][').split(', ')
        for ingredient in ingredients:
            ingredientsList.insert(tk.END, ingredient.strip("'").upper())
        ingredientsList.config(state=tk.DISABLED)


ingredients = []


root = tk.Tk()
root.title("Meal Ingredients".upper())

ingredient_label = tk.Label(root, text="Enter Ingredient:")
ingredient_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
ingredient_entry = tk.Entry(root)
ingredient_entry.grid(row=0, column=1, padx=10, pady=5)
ingredient_entry.bind("<Return>", (lambda event: add_ingredient()))
add_button = tk.Button(root, text="Add Ingredient", command=add_ingredient)
add_button.grid(row=0, column=2, padx=10, pady=5)


ingredients_label = tk.Label(root, text="Ingredients:")
ingredients_label.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
ingredients_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
ingredients_listbox.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")
for ingredient in ['water', 'salt', 'sugar', 'oil', 'butter', 'flour']:
    ingredients.append(ingredient)
    ingredients_listbox.insert(tk.END, ingredient.upper())

remove_button = tk.Button(root, text="Remove Ingredient", command=remove_ingredient)
remove_button.grid(row=1, column=2, padx=10, pady=5)
make_meal_button = tk.Button(root, text="Make Meal", command=make_meal)
make_meal_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)


root.rowconfigure(1, weight=1)
root.columnconfigure(1, weight=1)


root.mainloop()
