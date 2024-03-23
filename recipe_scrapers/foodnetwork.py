from ._abstract import AbstractScraper


class FoodNetwork(AbstractScraper):
    @classmethod
    def host(cls):
        return "foodnetwork.co.uk"


    def description(self):
        return self.schema.description()
