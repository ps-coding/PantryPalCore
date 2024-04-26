import tkinter as tk
from tkinter import messagebox
import pandas as pd

data = pd.read_csv('RAW_recipes.csv').values.tolist()


def filter_by_ingredients(available_ingredients):
    can_make = []

    for recipe in data:
        recipe_ingredients = map(lambda x: x.strip("'"), recipe[10].strip('][').split(', '))

        if all(map(lambda x: x in available_ingredients, recipe_ingredients)):
            can_make.append(recipe)

    return can_make

def add_ingredient():
    ingredient = ingredient_entry.get()
    if ingredient:
        ingredients.append(ingredient)
        ingredients_listbox.insert(tk.END, ingredient)
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
        self.geometry("400x400")
        self.recipes = recipes
        label = tk.Label(self, text ="Recipes")
        label.pack()
        self.listbox = tk.Listbox(self)
        self.listbox.pack()
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
        self.geometry("400x400")
        label = tk.Label(self, text = recipe[0].upper())
        label.pack()
        timec = tk.Label(self, text = "Time: " + str((recipe[1]) / 1000) + " minutes")
        timec.pack()
        descriptionD = tk.Label(self, text = "INSTRUCTIONS TO MAKE")
        descriptionD.pack()
        steps = recipe[8].strip('][').split(', ')
        stepsList = tk.Listbox(self)
        stepsList.pack()
        descriptionI = tk.Label(self, text = "INGREDIENTS")
        descriptionI.pack()
        for step in steps:
            stepsList.insert(tk.END, step.strip("'"))
        ingredients = recipe[10].strip('][').split(', ')
        ingredientsList = tk.Listbox(self)
        ingredientsList.pack()
        for ingredient in ingredients:
            ingredientsList.insert(tk.END, ingredient.strip("'"))

ingredients = []


root = tk.Tk()
root.title("Meal Ingredients")

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
for ingredient in ['flour', 'salt', 'butter', 'sugar', 'oil']:
    ingredients.append(ingredient)
    ingredients_listbox.insert(tk.END, ingredient)

remove_button = tk.Button(root, text="Remove Ingredient", command=remove_ingredient)
remove_button.grid(row=1, column=2, padx=10, pady=5)
make_meal_button = tk.Button(root, text="Make Meal", command=make_meal)
make_meal_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)


root.rowconfigure(1, weight=1)
root.columnconfigure(1, weight=1)


root.mainloop()
