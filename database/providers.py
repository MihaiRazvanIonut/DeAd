from faker.providers import BaseProvider


class CustomProvider(BaseProvider):
    def prisoner_item(self):
        prisoner_items = [
            "toothbrush", "soap", "shampoo", "toothpaste", "towel", "book", "magazine",
            "letter", "photograph", "stationery", "pen", "pencil", "envelope", "stamps",
            "food package", "snacks", "candy", "chips", "instant noodles", "socks",
            "undershirt", "underwear", "razor", "deodorant", "playing cards",
            "puzzle book", "crossword puzzle", "coloring book", "colored pencils",
            "radio", "MP3 player", "headphones", "batteries", "glasses", "vitamins",
            "medications", "exercise book", "prayer book", "rosary", "kosher meal",
            "halal meal", "allergy-free snacks"
        ]
        return self.random_element(prisoner_items)

    def visit_purpose(self):
        options = [
            "contact", "non_contact", "family", "legal", "professional",
            "special", "educational", "community", "media", "official"
        ]
        return self.random_element(options)

    def crime(self):
        crimes = [
            "theft", "burglary", "robbery", "assault", "murder", "arson",
            "fraud", "embezzlement", "vandalism", "drug trafficking",
            "possession of illegal substances", "money laundering", "kidnapping",
            "domestic violence", "identity theft", "shoplifting", "dui",
            "public intoxication", "disorderly conduct", "bribery",
            "blackmail", "cybercrime", "human trafficking", "illegal gambling",
            "tax evasion", "homicide", "manslaughter", "extortion",
            "hate crime", "perjury", "stalking", "trespassing",
            "smuggling", "forgery", "counterfeiting", "espionage"
        ]
        return self.random_element(crimes)

    def crud_operation(self):
        crud_operations = [
            "create", "update", "delete"
        ]
        return self.random_element(crud_operations)
