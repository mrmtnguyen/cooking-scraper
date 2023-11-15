# mypy: allow-untyped-defs

from ._abstract import AbstractScraper


class CookTalk(AbstractScraper):
    @classmethod
    def host(cls):
        return "cook-talk.com"

    def author(self):
        author_element = self.soup.find("div", {"class": "article-content"}).find(
            "a", {"href": lambda x: x and "recipe_author" in x}
        )
        return author_element.get_text() if author_element else None

    def title(self):
        return self.schema.title()

    def category(self):
        article_meta = self.soup.find("div", {"class": "article-meta"})
        category_element = article_meta.find("small", {"class": "meta-category"})
        return category_element.find("a").get_text()

    def image(self):
        return self.schema.image()

    def ingredients(self):
        return self.schema.ingredients()

    def instructions(self):
        return self.schema.instructions()

    def description(self):
        return self.schema.description()
