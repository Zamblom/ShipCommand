import math


class Player:
    def __init__(self, player_id: str) -> None:
        self._player_id: str = player_id

        self._name: str = ""
        self._raw_data: list[str] = []
        self._ability_scores: dict[str, int] = {}
        self._skill_modifiers: dict[str, int] = {}
        self._load_player_from_DND_Beyond_pdf()

    def _load_player_from_DND_Beyond_pdf(self) -> None:
        with open(f"Players/{self._player_id}.pdf", "rb+") as file:
            binary_data = file.read().split("\n".encode("utf-8"))

        self.raw_data = []
        for line in binary_data:
            try:
                self.raw_data.append(line.decode("utf-8"))
            except UnicodeDecodeError:
                continue

        # Why DND Beyond, why?
        self.name = self.raw_data[self.raw_data.index("/T(CharacterName)") + 6][3:].split(")")[0]

        self._ability_scores["strength"] = self._parse_value("STRmod", "abilityScore")
        self._ability_scores["dexterity"] = self._parse_value("DEXmod ", "abilityScore")
        self._ability_scores["constitution"] = self._parse_value("CONmod", "abilityScore")
        self._ability_scores["intelligence"] = self._parse_value("INTmod", "abilityScore")
        self._ability_scores["wisdom"] = self._parse_value("WISmod", "abilityScore")
        self._ability_scores["charisma"] = self._parse_value("CHamod", "abilityScore")

        self._skill_modifiers["strengthSave"] = self._parse_value("Strength", "saveModifier")
        self._skill_modifiers["athletics"] = self._parse_value("Athletics", "skillModifier")

        self._skill_modifiers["dexteritySave"] = self._parse_value("Dexterity", "saveModifier")
        self._skill_modifiers["acrobatics"] = self._parse_value("Acrobatics", "skillModifier")
        self._skill_modifiers["sleightOfHand"] = self._parse_value("SleightofHand", "skillModifier")
        self._skill_modifiers["stealth"] = self._parse_value("Stealth ", "skillModifier")

        self._skill_modifiers["constitutionSave"] = self._parse_value("Constitution", "saveModifier")

        self._skill_modifiers["intelligenceSave"] = self._parse_value("Intelligence", "saveModifier")
        self._skill_modifiers["arcana"] = self._parse_value("Arcana", "skillModifier")
        self._skill_modifiers["history"] = self._parse_value("History", "skillModifier")
        self._skill_modifiers["investigation"] = self._parse_value("Investigation", "skillModifier")
        self._skill_modifiers["nature"] = self._parse_value("Nature", "skillModifier")
        self._skill_modifiers["religion"] = self._parse_value("Religion", "skillModifier")

        self._skill_modifiers["wisdomSave"] = self._parse_value("Wisdom", "saveModifier")
        self._skill_modifiers["animalHandling"] = self._parse_value("Animal", "skillModifier")
        self._skill_modifiers["insight"] = self._parse_value("Insight", "skillModifier")
        self._skill_modifiers["medicine"] = self._parse_value("Medicine", "skillModifier")
        self._skill_modifiers["perception"] = self._parse_value("Perception", "skillModifier")
        self._skill_modifiers["survival"] = self._parse_value("Survival", "skillModifier")

        self._skill_modifiers["charismaSave"] = self._parse_value("Charisma", "saveModifier")
        self._skill_modifiers["deception"] = self._parse_value("Deception", "skillModifier")
        self._skill_modifiers["intimidation"] = self._parse_value("Intimidation", "skillModifier")
        self._skill_modifiers["performance"] = self._parse_value("Performance", "skillModifier")
        self._skill_modifiers["persuasion"] = self._parse_value("Persuasion", "skillModifier")

    def _parse_value(self, name: str, value_type: str) -> int:
        match value_type:
            case "abilityScore":
                return int(self.raw_data[self.raw_data.index(f"/T({name})") + 36][1:].split(")")[0])
            case "skillModifier":
                return int(self.raw_data[self.raw_data.index(f"/T({name})") + 36][1:].split(")")[0])
            case "saveModifier":
                return int(self.raw_data[self.raw_data.index(f"/T(ST {name})") + 36][1:].split(")")[0])
            case _:
                raise TypeError(f"value_type [{value_type}] is not in [abilityScore, skillModifier, saveModifier]")

    def get_data(self) -> dict[str, str | dict[str, int]]:
        stats: dict[str, int] = {ability: score_to_modifier(score) for ability, score in self._ability_scores.items()}
        stats.update({skill: modifier for skill, modifier in self._skill_modifiers.items()})
        return {"id": self._player_id, "name": self._name, "stats": stats}



def score_to_modifier(score: int) -> int:
    return math.floor((score - 10) / 2)
