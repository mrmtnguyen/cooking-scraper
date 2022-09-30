# mypy: disallow_untyped_defs=False
from ._abstract import AbstractScraper
from ._exceptions import SchemaOrgException


class Lecker(AbstractScraper):
    @classmethod
    def host(cls):
        return "lecker.de"

    def author(self):
        return self.schema.author()

    def title(self):
        try:
            return self.schema.title()
        except TypeError:
            return self.soup.find('header', {'class': 'article-header article-header--article'}).find('h1').get_text()

    def category(self):
        return self.schema.category()

    def prep_time(self):
        return self.schema.prep_time()

    def cook_time(self):
        return self.schema.cook_time()

    def total_time(self):
        try:
            return self.schema.total_time()
        except SchemaOrgException:
            return 0

    def yields(self):
        return self.schema.yields()

    def image(self):
        return self.schema.image()

    def ingredients(self):
        return self.schema.ingredients()

    def instructions(self):
        if self.schema.instructions():
            return self.schema.instructions()
        else:
            divs = self.soup.find_all('div', {'class': 'js-quizToggle'})
            for d in divs:
                if d.find('span', 'article__shifted-jump-label'):
                    return d.get_text()

    def ratings(self):
        return self.schema.ratings()

    def nutrients(self):
        return self.schema.nutrients()

    def cuisine(self):
        try:
            return self.schema.cuisine()
        except SchemaOrgException:
            return None

    def description(self):
        return self.schema.description()
