import random
import sys

def describe_country(country):
    descriptions = {
        "USA": [
            "Land of the free, home of the brave, and the place where deep-fried butter is a thing.",
            "Where everything is bigger, including the portion sizes and the dreams.",
            "The country that put a man on the moon but still struggles with the metric system."
        ],
        "France": [
            "The land of baguettes, berets, and an impressive ability to strike.",
            "Where wine flows like water and cheese is a national treasure.",
            "Home to the Eiffel Tower and the world's most stylish shrugs."
        ],
        "Japan": [
            "Where vending machines sell everything, including your next existential crisis.",
            "The land of sushi, samurai, and toilets smarter than most people.",
            "Where tradition and technology coexist in perfect harmony, like tea ceremonies and robots."
        ],
        "Australia": [
            "Where everything is trying to kill you, but the beaches make it worth it.",
            "The land of kangaroos, koalas, and people who casually call you 'mate.'",
            "Where 'shrimp on the barbie' is a myth, but Vegemite is very real."
        ],
        "Italy": [
            "The land of pasta, pizza, and people who talk with their hands.",
            "Where every meal feels like a celebration and every street looks like a postcard.",
            "Home to ancient ruins and modern fashionistas."
        ],
        "Nigeria": [
            "The land of jollof rice wars and the most vibrant parties you'll ever attend.",
            "Where the traffic is legendary, but so is the resilience of the people.",
            "Home to Nollywood, where drama never takes a day off."
        ],
        "Ghana": [
            "The land of kente cloth, rich history, and the friendliest smiles.",
            "Where the jollof rice debate gets serious, but the hospitality is unmatched.",
            "Home to beautiful beaches, historic castles, and the heart of West African culture."
        ],
        "Prod": [
            "Production is where everything works, except when it doesn't.",
        ],
        "Dev": [
            "Development is where everything is broken, but that's expected.",
        ],
        "Staging": [
            "Staging is where everything works until someone actually tests it."
        ],
        "Jamiaca": [
            "Home to the heart of Caribian and regge music.",
            "Home to Bob Marley and the most laid-back vibes.",
            "Where the beaches are beautiful and the food is spicy."
        ]
    }

    if country in descriptions:
        return random.choice(descriptions[country])
    else:
        return f"Sorry, I don't have a funny description for {country} yet. Maybe you can make one up!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python country.py <country>")
        sys.exit(1)

    country = sys.argv[1]
    print(describe_country(country))