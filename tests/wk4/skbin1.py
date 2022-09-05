def get_ingredients(drink_name: str):
    """This function find out and return how much each ingredient will be used
    in this drink from the given drink name.
    :param drink_name: A string which tells what is the drink's name
    :return: The two lists of base ingredients and syrup ingredients
    """

    split_drink_name = drink_name.split()
    needed_base_ingredients = [0, 0, 0]
    needed_base_name = ["coffee", "tea", "milk"]
    needed_syrup_ingredients = [0, 0, 0, 0]
    needed_syrup_name = ["caramel", "brown sugar", "strawberry", "lychee"]

    if "plain" in drink_name:
        needed_base_ingredients[needed_base_name.index(split_drink_name[-1])] += 30

    else:

        if "milk tea" in drink_name:

            if len(split_drink_name) > 2:
                cost = 10
                needed_syrup_ingredients[
                    needed_syrup_name.index(" ".join(split_drink_name[:-2]))
                ] += cost

            else:
                cost = 15
            needed_base_ingredients[1] += cost
            needed_base_ingredients[2] += cost

        elif "latte" in drink_name:

            if len(split_drink_name) >= 2:
                cost = 10
                needed_syrup_ingredients[
                    needed_syrup_name.index(" ".join(split_drink_name[:-1]))
                ] += cost

            else:
                cost = 15
            needed_base_ingredients[0] += cost
            needed_base_ingredients[2] += cost

        else:
            needed_base_ingredients[needed_base_name.index(split_drink_name[-1])] += 20
            needed_syrup_ingredients[
                needed_syrup_name.index(" ".join(split_drink_name[:-1]))
            ] += 10

    return needed_base_ingredients, needed_syrup_ingredients


def check_stock(
    base_stock: list, syrup_stock: list, base_needed: list, syrup_needed: list
) -> bool:
    """This function will check If the stock is enough to serve the selected
    drink, return True. Otherwise,
    return False.
    :param base_stock: Amount of base's ingredients that we have.
    :param syrup_stock: Amount of syrup's ingredients that we have.
    :param base_needed: Amount of base's ingredients that we need to make
    a drink.
    :param syrup_needed: Amount of syrup's ingredients that we need to make
    a drink.
    """

    return all(
        base_stock[index] >= base_needed[index] for index in range(len(base_stock))
    ) and all(
        syrup_stock[index] >= syrup_needed[index] for index in range(len(syrup_stock))
    )


def update_stock(
    base_stock: list, syrup_stock: list, base_needed: list, syrup_needed: list
) -> None:
    """This function update the stock after using the needed ingredients to
    serve the selected menu
    :param base_stock: Amount of base's ingredients that we have.
    :param syrup_stock: Amount of syrup's ingredients that we have.
    :param base_needed: Amount of base's ingredients that we need to
    make a drink.
    :param syrup_needed: Amount of syrup's ingredients that we need to
    make a drink.
    """

    for ingredient in range(len(base_stock)):
        base_stock[ingredient] -= base_needed[ingredient]

    for ingredient in range(len(syrup_stock)):
        syrup_stock[ingredient] -= syrup_needed[ingredient]


def get_price(drink_name) -> int:
    """This function will find out and return the price of the selected
    drink from the given drink name.
    :param drink_name: A string which tells what is the drink's name.
    :return: A price for the drink name.
    """

    price = 0
    if "latte" in drink_name or "milk tea" in drink_name and "plain" not in drink_name:
        price += 35

    else:
        price += 25

    if (
        "caramel" in drink_name
        or "brown sugar" in drink_name
        or "strawberry" in drink_name
        or "lychee" in drink_name
    ):
        price += 5

    return price


menus = [
    "plain coffee",
    "caramel coffee",
    "brown sugar coffee",
    "latte",
    "caramel latte",
    "brown sugar latte",
    "plain tea",
    "brown sugar tea",
    "strawberry tea",
    "lychee tea",
    "milk tea",
    "caramel milk tea",
    "brown sugar milk tea",
    "plain milk",
    "caramel milk",
    "brown sugar milk",
    "strawberry milk",
]
current_base_stocks = [50, 50, 100]
current_syrup_stocks = [20, 20, 20, 20]

print("Drink menu:")

for menu_number in range(len(menus)):
    print(f"{menu_number + 1}.{menus[menu_number]}")

print("=====================")

print("At the beginning, here are ingredient stocks...")
print(
    f"coffee: {current_base_stocks[0]}, tea: {current_base_stocks[1]}, "
    f"milk: {current_base_stocks[2]}\n"
    f"caramel: {current_syrup_stocks[0]}, brown sugar: "
    f"{current_syrup_stocks[1]}, strawberry: "
    f"{current_syrup_stocks[2]}, lychee: {current_syrup_stocks[3]}"
)

print("=====================")

drink_index = int(input("Enter drink index: "))
needed_base_ingredient, needed_syrup_ingredient = get_ingredients(
    menus[drink_index - 1]
)
update_stock(
    current_base_stocks,
    current_syrup_stocks,
    needed_base_ingredient,
    needed_syrup_ingredient,
)
print(f">>> You order {menus[drink_index - 1]}")

print("=====================")

print("Needed ingredients:")
print(
    f"coffee: {needed_base_ingredient[0]}, tea: {needed_base_ingredient[1]}, "
    f"milk: {needed_base_ingredient[2]}\n"
    f"caramel: {needed_syrup_ingredient[0]}, brown sugar: "
    f"{needed_syrup_ingredient[1]}, strawberry: "
    f"{needed_syrup_ingredient[2]}, lychee: {needed_syrup_ingredient[3]}\n"
    f"After order, update ingredient stocks...\n"
    f"coffee: {current_base_stocks[0]}, tea: {current_base_stocks[1]}, "
    f"milk: {current_base_stocks[2]}\n"
    f"caramel: {current_syrup_stocks[0]}, brown sugar: "
    f"{current_syrup_stocks[1]}, strawberry: "
    f"{current_syrup_stocks[2]}, lychee: {current_syrup_stocks[3]}"
)

print("=====================")

print(
    f"Your order is successful. Price of your drink = "
    f"{get_price(menus[drink_index - 1])} "
)
print(f"Revenue : {get_price(menus[drink_index - 1])} Baht")
