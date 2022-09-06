from ._abstract import AbstractScraper


class OwenHan(AbstractScraper):
    @classmethod
    def host(cls):
        return "owen-han.com"

    def author(self):
        return "Owen Han"

    def title(self):
        return self.soup.find("h1", {"class": "entry-title"}).text

    def image(self):
        return self.soup.find("link", {"rel": "image_src"})["href"]

    def ingredients(self):
        return [x for x in map(lambda x: x.text, self.soup.select("ul > li"))]

    def instructions(self):
        return [x for x in map(lambda x: x.text, self.soup.select("ol > li"))]
