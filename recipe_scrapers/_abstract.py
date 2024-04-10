# mypy: disallow_untyped_defs=False
import inspect
from collections import OrderedDict
from typing import Dict, List, Optional, Tuple, Union
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from recipe_scrapers.settings import settings

from ._grouping_utils import IngredientGroup
from ._schemaorg import SchemaOrg

# Some sites close their content for 'bots', so user-agent must be supplied
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0"
}


class AbstractScraper:
    page_data: Union[str, bytes]

    def __init__(
        self,
        url: Union[str, None],
        proxies: Optional[
            Dict[str, str]
        ] = None,  # allows us to specify optional proxy server
        timeout: Optional[
            Union[float, Tuple[float, float], Tuple[float, None]]
        ] = None,  # allows us to specify optional timeout for request
        wild_mode: Optional[bool] = False,
        html: Union[str, bytes, None] = None,
    ):
        if html:
            self.page_data = html
            self.url = url
        else:
            assert url is not None, "url required for fetching recipe data"
            resp = requests.get(
                url,
                headers=HEADERS,
                proxies=proxies,
                timeout=timeout,
            )
            self.page_data = resp.content
            self.url = resp.url

        self.wild_mode = wild_mode
        self.soup = BeautifulSoup(self.page_data, "html.parser")
        self.schema = SchemaOrg(self.page_data)

        # attach the plugins as instructed in settings.PLUGINS
        if not hasattr(self.__class__, "plugins_initialized"):
            for name, _ in inspect.getmembers(self, inspect.ismethod):
                current_method = getattr(self.__class__, name)
                for plugin in reversed(settings.PLUGINS):
                    if plugin.should_run(self.host(), name):
                        current_method = plugin.run(current_method)
                setattr(self.__class__, name, current_method)
            setattr(self.__class__, "plugins_initialized", True)

    @classmethod
    def host(cls) -> str:
        """Host domain of the recipe URL."""
        raise NotImplementedError("This should be implemented.")

    def canonical_url(self):
        """Canonical or original URL of the recipe."""
        canonical_link = self.soup.find("link", {"rel": "canonical", "href": True})
        if canonical_link:
            return urljoin(self.url, canonical_link["href"])
        return self.url

    def title(self):
        """Title of the recipe."""
        raise NotImplementedError("This should be implemented.")

    def category(self):
        """Category of the recipe."""
        raise NotImplementedError("This should be implemented.")

    def total_time(self):
        """Total time needed to prepare and cook the recipe in minutes."""
        raise NotImplementedError("This should be implemented.")

    def cook_time(self):
        """Cooking time in minutes."""
        raise NotImplementedError("This should be implemented.")

    def prep_time(self):
        """Preparation time in minutes."""
        raise NotImplementedError("This should be implemented.")

    def cooking_method(self):
        """The method of cooking the recipe"""
        raise NotImplementedError("This should be implemented.")

    def keywords(self):
        """Keywords or tags used to describe the recipe"""
        raise NotImplementedError("This should be implemented.")

    def yields(self):
        """Total servings or items in the recipe."""
        raise NotImplementedError("This should be implemented.")

    def image(self):
        """An image URL for the recipe."""
        raise NotImplementedError("This should be implemented.")

    def nutrients(self):
        """Nutrients of the recipe."""
        raise NotImplementedError("This should be implemented.")

    def language(self):
        """Language the recipe is written in."""
        candidate_languages = OrderedDict()
        html = self.soup.find("html", {"lang": True})
        candidate_languages[html.get("lang")] = True

        # Deprecated: check for a meta http-equiv header
        # See: https://www.w3.org/International/questions/qa-http-and-lang
        meta_language = self.soup.find(
            "meta",
            {
                "http-equiv": lambda x: x and x.lower() == "content-language",
                "content": True,
            },
        )
        if meta_language:
            language = meta_language.get("content").split(",", 1)[0]
            if language:
                candidate_languages[language] = True

        # If other languages exist, remove 'en' commonly generated by HTML editors
        if len(candidate_languages) > 1:
            candidate_languages.pop("en", None)

        # Return the first candidate language
        return candidate_languages.popitem(last=False)[0]

    def ingredients(self):
        """Ingredients of the recipe."""
        raise NotImplementedError("This should be implemented.")

    def ingredient_groups(self) -> List[IngredientGroup]:
        """List of ingredient groups."""
        return [IngredientGroup(purpose=None, ingredients=self.ingredients())]

    def instructions(self) -> str:
        """Instructions to prepare the recipe."""
        raise NotImplementedError("This should be implemented.")

    def instructions_list(self) -> List[str]:
        """Instructions to prepare the recipe as a list."""
        return [
            instruction
            for instruction in self.instructions().split("\n")
            if instruction
        ]

    def ratings(self):
        """Ratings of the recipe."""
        raise NotImplementedError("This should be implemented.")

    def author(self):
        """Author of the recipe."""
        raise NotImplementedError("This should be implemented.")

    def cuisine(self):
        """Cuisine of the recipe."""
        raise NotImplementedError("This should be implemented.")

    def description(self):
        """Description of the recipe."""
        raise NotImplementedError("This should be implemented.")

    def reviews(self):
        """Reviews of the recipe."""
        raise NotImplementedError("This should be implemented.")

    def equipment(self):
        """Equipment needed for the recipe."""
        raise NotImplementedError("This should be implemented.")

    def links(self):
        """Links found in the recipe."""
        invalid_href = {"#", ""}
        links_html = self.soup.findAll("a", href=True)

        return [link.attrs for link in links_html if link["href"] not in invalid_href]

    def site_name(self):
        """Name of the website."""
        meta = self.soup.find("meta", property="og:site_name")
        return meta.get("content") if meta else None

    def to_json(self):
        """Recipe information in JSON format."""
        json_dict = {}
        public_method_names = [
            method
            for method in dir(self)
            if callable(getattr(self, method))
            if not method.startswith("_") and method not in ["soup", "links", "to_json"]
        ]
        for method in public_method_names:
            try:
                if method == "ingredient_groups":
                    json_dict[method] = [i.__dict__ for i in getattr(self, method)()]
                else:
                    json_dict[method] = getattr(self, method)()
            except Exception:
                pass
        return json_dict
