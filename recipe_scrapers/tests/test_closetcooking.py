import os
import unittest

from recipe_scrapers.closetcooking import ClosetCooking


class TestClosetCooking(unittest.TestCase):
    def setUp(self):
        # tests are run from tests.py
        with open(os.path.join(
            os.getcwd(),
            'recipe_scrapers',
            'tests',
            'test_data',
            'closetcooking.testhtml'
        )) as file_opened:
            self.harvester_class = ClosetCooking(file_opened, test=True)

    def test_host(self):
        self.assertEqual(
            'closetcooking.com',
            self.harvester_class.host()
        )

    def test_title(self):
        self.assertEqual(
            self.harvester_class.title(),
            'Jalapeno Popper Skillet Chicken'
        )

    def test_total_time(self):
        self.assertEqual(
            20,
            self.harvester_class.total_time()
        )

    def test_ingredients(self):
        self.assertListEqual(
            [
                '1 tablespoon oil',
                '1 pound chicken, boneless and skinless, diced',
                'salt and pepper to taste',
                '1 small onion, diced',
                '2 jalapenos, sliced or diced',
                '2 cloves garlic, chopped',
                '1 cup chicken broth',
                '4 ounces cream cheese, softened',
                '1 cup cheddar cheese, shredded'
            ],
            self.harvester_class.ingredients()
        )

    def test_instructions(self):
        return self.assertEqual(
            'Heat the oil in a pan over medium-high heat, add the chicken (seasoned with salt and pepper) and cook until lightly golden brown.\nAdd the onions and jalapenos and cook until tender, about a minute before adding the garlic and cooking another minute.\nAdd the chicken broth and deglaze the skillet by scraping the brown bits up off of the bottom of the pan as the broth sizzles.\nAdd the cheese and cook until it has melted and the sauce is nice and smooth',
            self.harvester_class.instructions()
        )
