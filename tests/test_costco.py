# mypy: allow-untyped-defs

from recipe_scrapers.costco import Costco
from tests import ScraperTest


class TestCostcoScraper(ScraperTest):
    scraper_class = Costco

    def test_host(self):
        self.assertEqual("costco.com", self.harvester_class.host())

    def test_title(self):
        self.assertEqual(
            "Chicken Salad with Red Grapes, Walnuts and Blue Cheese",
            self.harvester_class.title(),
        )

    def test_author(self):
        self.assertEqual("Costco Connection", self.harvester_class.author())

    def test_image(self):
        self.assertEqual(
            "https://mobilecontent.costco.com/live/resource/img/static-us-connection-march-23/03_23_FTT_ChickenSaladRedGrapesWalnutsBlueCheese.jpg",
            self.harvester_class.image(),
        )

    def test_ingredients(self):
        ingredients_list = [
            "6 cups rotisserie chicken, shredded",
            "3 cups red seedless grapes, halved lengthwise",
            "2 celery ribs (about 1 cup), thinly sliced",
            "1 cup walnuts, toasted and chopped",
            "½ cup blue cheese, crumbled",
            "2 cups mayonnaise",
            "2 Tbsp sherry vinegar",
            "1 Tbsp fresh thyme leaves",
            "2 tsp lemon zest",
            "½ tsp garlic powder",
            "½ tsp kosher salt, or to taste",
        ]
        self.assertEqual(ingredients_list, self.harvester_class.ingredients())

    def test_instructions(self):
        instructions_text = (
            "/nCombine chicken, grapes, celery, walnuts and blue cheese in a large mixing bowl./nIn a medium-size mixing bowl, blend mayonnaise, sherry vinegar, thyme, lemon zest, garlic powder and salt./nFold the dressing into the chicken-grape mixture and combine well. Adjust seasonings as desired. Serve in Bibb lettuce cups or as a sandwich filling. Makes 6 servings."
        )
        self.assertEqual(instructions_text, self.harvester_class.instructions())
