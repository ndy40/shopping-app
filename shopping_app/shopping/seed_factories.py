import random

import factory.django

from accounts.models import User
from accounts.seed_factories import UserFactory
from shopping.models import ShoppingList, ShoppingItem, ShoppingListStatus

# depends on account
deps = [
    "accounts",
]

FOOD_ITEMS = [
    "abiyuch",
    "acerola",
    "acorn",
    "agave",
    "agents",
    "agutuk",
    "alfalfa",
    "amaranth",
    "animal",
    "apache",
    "apple",
    "apples",
    "applesauce",
    "apricot",
    "apricots",
    "arrowhead",
    "arrowroot",
    "artichokes",
    "artificial",
    "arugula",
    "ascidians",
    "asparagus",
    "avocados",
    "baby",
    "babyfood",
    "bacon",
    "bagel",
    "bagels",
    "baking",
    "balls",
    "balsam-pear",
    "bamboo",
    "bananas",
    "bar",
    "barbecue",
    "barley",
    "bars",
    "basil",
    "bean",
    "beans",
    "bear",
    "beef",
    "beerwurst",
    "beet",
    "beets",
    "berry",
    "besan",
    "beverage",
    "beverages",
    "biscuits",
    "bison",
    "bits",
    "bitter",
    "blackberries",
    "blackberry",
    "blackeyes",
    "blend",
    "blueberries",
    "blueberry",
    "bockwurst",
    "bologna",
    "borage",
    "bowl",
    "boysenberries",
    "bran",
    "brand",
    "bratwurst",
    "braunschweiger",
    "bread",
    "breadfruit",
    "breakfast",
    "breast",
    "broadbeans",
    "broccoli",
    "broth",
    "brotwurst",
    "brussels",
    "buckwheat",
    "buffalo",
    "bulgur",
    "buns",
    "burdock",
    "burgers",
    "burrito",
    "butter",
    "butterbur",
    "butters",
    "cabbage",
    "cake",
    "candied",
    "candies",
    "capers",
    "carambola",
    "carbonated",
    "cardoon",
    "caribou",
    "carissa",
    "carne",
    "carob",
    "carob-flavor",
    "carrot",
    "carrots",
    "cassava",
    "catsup",
    "cattail",
    "cauliflower",
    "celeriac",
    "celery",
    "celtuce",
    "cereal",
    "cereals",
    "chard",
    "chayote",
    "cheese",
    "cheesecake",
    "cheesefurter",
    "cherimoya",
    "cherries",
    "chewing",
    "chicken",
    "chickpea",
    "chickpeas",
    "chicory",
    "chilchen",
    "child",
    "chili",
    "chips",
    "chiton",
    "chives",
    "chocolate",
    "chocolate-flavor",
    "chocolate-flavored",
    "chokecherries",
    "chorizo",
    "chrysanthemum",
    "cilantro",
    "cinnamon",
    "citronella",
    "citrus",
    "clam",
    "clementines",
    "cloudberries",
    "cockles",
    "cocktail",
    "cocoa",
    "coffee",
    "coffeecake",
    "collards",
    "commercially",
    "concentrate",
    "cone",
    "cones",
    "confectionery",
    "containing",
    "cookie",
    "cookies",
    "coriander",
    "corn",
    "corned",
    "cornmeal",
    "cornsalad",
    "cornstarch",
    "cotija",
    "couscous",
    "cowpeas",
    "crabapples",
    "cracker",
    "crackers",
    "cranberries",
    "cranberry",
    "cranberry-apple",
    "cranberry-apricot",
    "cranberry-grape",
    "cranberry-orange",
    "cream",
    "creams",
    "creamy",
    "cress",
    "croissants",
    "croutons",
    "crumbs",
    "crust",
    "crustaceans",
    "cucumber",
    "currants",
    "custard-apple",
    "custards",
    "dairy",
    "dandelion",
    "danish",
    "dates",
    "deer",
    "dessert",
    "desserts",
    "diabetes",
    "dill",
    "dinner",
    "dip",
    "dishes",
    "dock",
    "dogs",
    "dough",
    "doughnuts",
    "dove",
    "dressing",
    "drink",
    "drippings",
    "drumstick",
    "dry",
    "duck",
    "dulce",
    "durian",
    "dutch",
    "ear",
    "edamame",
    "egg",
    "eggnog",
    "eggnog-flavor",
    "eggplant",
    "eggs",
    "elderberries",
    "elk",
    "emu",
    "endive",
    "energy",
    "entrees",
    "epazote",
    "eppaw",
    "extender",
    "extract",
    "falafel",
    "fast",
    "fat",
    "fava",
    "feijoa",
    "fennel",
    "fern",
    "ferns",
    "fiddlehead",
    "figs",
    "fillets",
    "fillings",
    "fireweed",
    "fish",
    "flakes",
    "flan",
    "flavored",
    "flour",
    "flours",
    "flower",
    "flowers",
    "fluid",
    "focaccia",
    "foie",
    "food",
    "foods",
    "formula",
    "formulated",
    "frankfurter",
    "franks",
    "frijoles",
    "frog",
    "from",
    "frostings",
    "frozen",
    "fruit",
    "fruit-flavored",
    "frybread",
    "frying",
    "fungi",
    "garbanzo",
    "garlic",
    "gelatin",
    "gelatins",
    "germ",
    "ginger",
    "gluten",
    "goat",
    "goose",
    "gooseberries",
    "gourd",
    "grain",
    "gram",
    "granola",
    "grape",
    "grapefruit",
    "grapes",
    "gras",
    "grass",
    "gravy",
    "green",
    "greens",
    "groats",
    "ground",
    "groundcherries",
    "grouse",
    "guacamole",
    "guanabana",
    "guava",
    "guavas",
    "guinea",
    "gum",
    "gums",
    "ham",
    "hazelnut",
    "hazelnuts",
    "headcheese",
    "hearts",
    "hen",
    "hibiscus",
    "hips",
    "hominy",
    "honey",
    "horned",
    "horseradish",
    "household",
    "huckleberries",
    "hummus",
    "hush",
    "hyacinth",
    "hyacinth-beans",
    "hydrogenated",
    "hydrolyzed",
    "ice",
    "imitation",
    "incaparina",
    "industrial",
    "isolate",
    "jackfruit",
    "jams",
    "java-plum",
    "jellies",
    "jellyfish",
    "jerusalem-artichokes",
    "jicama",
    "juice",
    "jujube",
    "jute",
    "kale",
    "kanpyo",
    "keikitos",
    "kielbasa",
    "kiwano",
    "kiwifruit",
    "knackwurst",
    "kohlrabi",
    "kumquats",
    "lamb",
    "lambs",
    "lambsquarters",
    "lard",
    "lasagna",
    "lean",
    "leavening",
    "leaves",
    "lebanon",
    "leche",
    "leeks",
    "legs",
    "lemon",
    "lemonade",
    "lemonade-flavor",
    "lemons",
    "lentils",
    "lettuce",
    "lima",
    "lime",
    "limeade",
    "limes",
    "link",
    "links",
    "lion",
    "litchis",
    "liver",
    "liverwurst",
    "loaf",
    "loganberries",
    "loin",
    "longans",
    "loquats",
    "lotus",
    "lulo",
    "lunch",
    "luncheon",
    "lupins",
    "luxury",
    "macaroni",
    "made",
    "malabar",
    "malt",
    "malted",
    "mammy-apple",
    "mango",
    "mangos",
    "mangosteen",
    "maraschino",
    "margarine",
    "margarine-like",
    "marmalade",
    "mashu",
    "mayonnaise",
    "meal",
    "meat",
    "meatballs",
    "meatloaf",
    "melon",
    "melons",
    "milk",
    "millet",
    "miso",
    "mixed",
    "mocha",
    "molasses",
    "mollusks",
    "moose",
    "mortadella",
    "mothbeans",
    "mother's",
    "mountain",
    "mouse",
    "muffin",
    "muffins",
    "mulberries",
    "mung",
    "mungo",
    "mush",
    "mushrooms",
    "mustard",
    "mutton",
    "nance",
    "naranjilla",
    "natto",
    "navajo",
    "nectar",
    "nectarines",
    "nettles",
    "new",
    "noodles",
    "nopales",
    "novelties",
    "nutritional",
    "nuts",
    "oat",
    "oats",
    "octopus",
    "oheloberries",
    "oil",
    "oil-butter",
    "okara",
    "okra",
    "olive",
    "olives",
    "onion",
    "onions",
    "oopah",
    "orange",
    "orange-flavor",
    "orange-grapefruit",
    "oranges",
    "ostrich",
    "oven-roasted",
    "palm",
    "pancakes",
    "papad",
    "papaya",
    "papayas",
    "parfait",
    "parmesan",
    "parsley",
    "parsnips",
    "passion-fruit",
    "pasta",
    "pastrami",
    "pastries",
    "pastry",
    "pate",
    "patties",
    "patty",
    "pea",
    "peach",
    "peaches",
    "peanut",
    "peanuts",
    "pear",
    "pears",
    "peas",
    "pectin",
    "peel",
    "people",
    "pepeao",
    "pepper",
    "peppered",
    "peppermint",
    "pepperoni",
    "peppers",
    "persimmons",
    "pheasant",
    "phyllo",
    "pickle",
    "pickles",
    "picnic",
    "pie",
    "pigeon",
    "pigeonpeas",
    "piki",
    "pimento",
    "pimiento",
    "pineapple",
    "pinon",
    "pitanga",
    "pizza",
    "plain",
    "plantains",
    "plums",
    "pockets",
    "pokeberry",
    "pomegranate",
    "pomegranates",
    "popcorn",
    "pork",
    "potato",
    "potatoes",
    "potsticker",
    "poultry",
    "powder",
    "prairie",
    "prepared",
    "preserves",
    "pretzels",
    "prickly",
    "product",
    "products",
    "protein",
    "prune",
    "prunes",
    "pudding",
    "puddings",
    "puff",
    "puffs",
    "pulled",
    "pulp",
    "pummelo",
    "pumpkin",
    "punch",
    "punch-flavor",
    "puppies",
    "puree",
    "purslane",
    "quail",
    "quarters",
    "queso",
    "quinces",
    "quinoa",
    "raab",
    "radicchio",
    "radish",
    "radishes",
    "raisins",
    "rambutan",
    "raspberries",
    "ravioli",
    "ready-to-drink",
    "ready-to-eat",
    "red",
    "reddi",
    "reduced",
    "refried",
    "relish",
    "rennin",
    "replacement",
    "restaurant",
    "rhubarb",
    "rice",
    "rings",
    "roast",
    "rojos",
    "roll",
    "rolls",
    "root",
    "roots",
    "rose",
    "rose-apples",
    "roselle",
    "rosemary",
    "rowal",
    "ruffed",
    "rutabagas",
    "rye",
    "salad",
    "salami",
    "salmon",
    "salmonberries",
    "salsify",
    "salt",
    "sandwich",
    "sapodilla",
    "sapote",
    "sauce",
    "sauerkraut",
    "sausage",
    "school",
    "scrapple",
    "sea",
    "seal",
    "seasoning",
    "seaweed",
    "seeds",
    "semolina",
    "sesbania",
    "shake",
    "shakes",
    "shallots",
    "shell",
    "shells",
    "sherbet",
    "shoots",
    "shortening",
    "shoyu",
    "side",
    "smelt",
    "smoked",
    "smoothie",
    "snack",
    "snacks",
    "sorghum",
    "souffle",
    "soup",
    "sourdock",
    "soursop",
    "soy",
    "soybean",
    "soybeans",
    "soyburgers",
    "soymilk",
    "spaghetti",
    "spanish",
    "spearmint",
    "spelt",
    "spices",
    "spinach",
    "split",
    "spread",
    "sprouts",
    "squab",
    "squash",
    "squirrel",
    "steelhead",
    "stew",
    "stew/soup",
    "sticks",
    "stinging",
    "strawberries",
    "strawberry-flavor",
    "strudel",
    "stuffing",
    "substitute",
    "substitutes",
    "succotash",
    "sugar",
    "sugar-apples",
    "sugars",
    "supplement",
    "swamp",
    "sweet",
    "sweetener",
    "sweeteners",
    "swisswurst",
    "syrup",
    "syrups",
    "taco",
    "tamales",
    "tamari",
    "tamarind",
    "tamarinds",
    "tangerine",
    "tangerines",
    "tannier",
    "tapioca",
    "taquitos",
    "taro",
    "tart",
    "tea",
    "teff",
    "tempeh",
    "tenders",
    "tennis",
    "thigh",
    "thuringer",
    "thyme",
    "toast",
    "toaster",
    "toddler",
    "tofu",
    "tomatillos",
    "tomato",
    "tomatoes",
    "topping",
    "toppings",
    "tortellini",
    "tortilla",
    "tortillas",
    "tostada",
    "triticale",
    "trout",
    "tuber",
    "tunicate",
    "tunughnak",
    "turkey",
    "turnip",
    "turnips",
    "turnover",
    "turtle",
    "twists",
    "vanilla",
    "veal",
    "vegetable",
    "vegetable-oil",
    "vegetables",
    "vegetarian",
    "veggie",
    "venison",
    "vermicelli",
    "vinegar",
    "vinespinach",
    "vital",
    "volteados",
    "waffle",
    "waffles",
    "walrus",
    "wasabi",
    "water",
    "waterchestnuts",
    "watercress",
    "watermelon",
    "waxgourd",
    "weed",
    "wheat",
    "whey",
    "whiskey",
    "whole",
    "wild",
    "willow",
    "wine",
    "winged",
    "wocas",
    "wonton",
    "wrappers",
    "yachtwurst",
    "yam",
    "yambean",
    "yardlong",
    "yautia",
    "yeast",
    "yellow",
    "yogurt",
    "yogurts",
    "zealand",
    "zwieback",
]


class ShoppingListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShoppingList

    status = ShoppingListStatus.DRAFT
    owner = factory.SubFactory(UserFactory)


class ShoppingItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ShoppingItem

    name = factory.LazyFunction(lambda: random.choice(FOOD_ITEMS))
    shopping_list = factory.SubFactory(ShoppingListFactory)


def run(_, *args, **kwargs):
    for user in User.objects.all():
        print(f"Generating list for user - {user.get_full_name()}")
        shopping_list = ShoppingListFactory(owner=user)
        ShoppingItemFactory(shopping_list=shopping_list)
