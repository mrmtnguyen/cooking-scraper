# mypy: disallow_untyped_defs=False
# IF things in this file continue get messy (I'd say 300+ lines) it may be time to
# find a package that parses https://schema.org/Recipe properly (or create one ourselves).

from collections import defaultdict
import json

import html5lib

from ._exceptions import SchemaOrgException
from ._utils import get_minutes, get_yields, normalize_string


class Extractor:
    def __init__(self, page_data):
        self.tree = html5lib.parse(page_data)

    @property
    def linked_data(self):
        for element in self.tree.findall(
            path=".//script[@type='application/ld+json']",
            namespaces={"": "http://www.w3.org/1999/xhtml"},
        ):
            try:
                yield json.loads(element.text, strict=False)
            except Exception:
                pass

    @property
    def microdata(self):
        yield from self.tree.findall(
            path=".//*[@itemscope]",
            namespaces={"": "http://www.w3.org/1999/xhtml"},
        )


def chunked_text(node):
    if node.text:
        yield node.text
    if isinstance(node.tag, str) and node.tag.endswith("}br"):
        yield "\n"
    for child in node:
        prev = None
        for chunk in chunked_text(child):
            if chunk == prev == "\n":
                continue
            yield chunk
            prev = chunk
    if node.tail:
        if node.tail[0].isspace():
            trimmed = node.tail.lstrip()
            if trimmed and not trimmed[0] == ",":
                yield " "
            yield trimmed
        else:
            yield node.tail


class SchemaOrg:
    def __init__(self, page_data, raw=False):
        if raw:
            self.format = "raw"
            self.data = page_data
            return
        self.format = None
        self.data = {}

        extractor = Extractor(page_data)
        for element in extractor.linked_data:
            if isinstance(element, dict) and "@graph" in element:
                graph_nodes = element["@graph"]
            elif isinstance(element, list):
                graph_nodes = element
            else:
                graph_nodes = [element]
            for node in graph_nodes:
                node_type = str().join(node.get("@type", [])).lower()
                if node_type == "recipe":
                    self.data = node
                    return

        microdata = defaultdict(list)
        for element in extractor.microdata:
            if "recipe" in element.attrib["itemtype"].lower():
                for node in element.findall(
                    path=".//html:*[@itemprop]",
                    namespaces={"html": "http://www.w3.org/1999/xhtml"},
                ):
                    name = node.attrib["itemprop"]
                    if "content" in node.attrib:
                        value = node.attrib["content"]
                    else:
                        value = str().join(chunked_text(node)).strip()
                    microdata[name].append(value)

        # Flatten the value list for microdata properties that only appear once
        for key, values in microdata.items():
            if len(values) == 1:
                microdata[key] = values[0]

        self.data = microdata

    def language(self):
        return self.data.get("inLanguage") or self.data.get("language")

    def title(self):
        return normalize_string(self.data.get("name"))

    def category(self):
        category = self.data.get("recipeCategory")
        if isinstance(category, list):
            return ",".join(category)
        return category

    def author(self):
        author = self.data.get("author") or self.data.get("Author")
        if (
            author
            and isinstance(author, list)
            and len(author) >= 1
            and isinstance(author[0], dict)
        ):
            author = author[0]
        if author and isinstance(author, dict):
            author = author.get("name")
        return author

    def total_time(self):
        print(self.data)
        if not (self.data.keys() & {"totalTime", "prepTime", "cookTime"}):
            raise SchemaOrgException("Cooking time information not found in SchemaOrg")

        def get_key_and_minutes(k):
            source = self.data.get(k)
            # Workaround: strictly speaking schema.org does not provide for minValue (and maxValue) properties on objects of type Duration; they are however present on objects with type QuantitativeValue
            # Refs:
            #  - https://schema.org/Duration
            #  - https://schema.org/QuantitativeValue
            if type(source) == dict and "minValue" in source:
                source = source["minValue"]
            return get_minutes(source, return_zero_on_not_found=True)

        total_time = get_key_and_minutes("totalTime")
        if not total_time:
            times = list(map(get_key_and_minutes, ["prepTime", "cookTime"]))
            total_time = sum(times)
        return total_time

    def cook_time(self):
        if not (self.data.keys() & {"cookTime"}):
            raise SchemaOrgException("Cooktime information not found in SchemaOrg")
        return get_minutes(self.data.get("cookTime"), return_zero_on_not_found=True)

    def prep_time(self):
        if not (self.data.keys() & {"prepTime"}):
            raise SchemaOrgException("Preptime information not found in SchemaOrg")
        return get_minutes(self.data.get("prepTime"), return_zero_on_not_found=True)

    def yields(self):
        yield_data = self.data.get("recipeYield") or self.data.get("yield")
        if yield_data and isinstance(yield_data, list):
            yield_data = yield_data[0]
        recipe_yield = str(yield_data)
        return get_yields(recipe_yield)

    def image(self):
        image = self.data.get("image")

        if image is None:
            raise SchemaOrgException("Image not found in SchemaOrg")

        if isinstance(image, list):
            # Could contain a dict
            image = image[0]

        if isinstance(image, dict):
            image = image.get("url")

        if "http://" not in image and "https://" not in image:
            # some sites give image path relative to the domain
            # in cases like this handle image url with class methods or og link
            image = ""

        return image

    def ingredients(self):
        ingredients = (
            self.data.get("recipeIngredient") or self.data.get("ingredients") or []
        )
        return [
            normalize_string(ingredient) for ingredient in ingredients if ingredient
        ]

    def nutrients(self):
        nutrients = self.data.get("nutrition", {})

        # Some recipes contain null or numbers which breaks normalize_string()
        # We'll ignore null and convert numbers to a string, like Schema validator does
        for key, val in nutrients.copy().items():
            if val is None:
                del nutrients[key]
            elif type(val) in [int, float]:
                nutrients[key] = str(val)

        return {
            normalize_string(nutrient): normalize_string(value)
            for nutrient, value in nutrients.items()
            if nutrient != "@type" and value is not None
        }

    def _extract_howto_instructions_text(self, schema_item):
        instructions_gist = []
        if type(schema_item) is str:
            instructions_gist.append(schema_item)
        elif schema_item.get("@type") == "HowToStep":
            if schema_item.get("name", False):
                # some sites have duplicated name and text properties (1:1)
                # others have name same as text but truncated to X chars.
                # ignore name in these cases and add the name value only if it's different from the text
                if not schema_item.get("text").startswith(
                    schema_item.get("name").rstrip(".")
                ):
                    instructions_gist.append(schema_item.get("name"))
            instructions_gist.append(schema_item.get("text"))
        elif schema_item.get("@type") == "HowToSection":
            name = schema_item.get("name") or schema_item.get("Name")
            if name is not None:
                instructions_gist.append(name)
            for item in schema_item.get("itemListElement"):
                instructions_gist += self._extract_howto_instructions_text(item)
        return instructions_gist

    def instructions(self):
        instructions = self.data.get("recipeInstructions") or ""

        if isinstance(instructions, list):
            instructions_gist = []
            for schema_instruction_item in instructions:
                instructions_gist += self._extract_howto_instructions_text(
                    schema_instruction_item
                )

            return "\n".join(
                normalize_string(instruction) for instruction in instructions_gist
            )

        return instructions

    def ratings(self):
        ratings = self.data.get("aggregateRating")
        if ratings is None:
            raise SchemaOrgException("No ratings data in SchemaOrg.")

        if isinstance(ratings, dict):
            ratings = ratings.get("ratingValue")

        if ratings is None:
            raise SchemaOrgException("No ratingValue in SchemaOrg.")

        return round(float(ratings), 2)

    def cuisine(self):
        cuisine = self.data.get("recipeCuisine")
        if cuisine is None:
            raise SchemaOrgException("No cuisine data in SchemaOrg.")
        elif isinstance(cuisine, list):
            return ",".join(cuisine)
        return cuisine

    def description(self):
        description = self.data.get("description")
        if description is None:
            raise SchemaOrgException("No description data in SchemaOrg.")
        return normalize_string(description)
