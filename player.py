import math

import typeguard


class Player:
    @typeguard.typechecked
    def __init__(self, filepath: str) -> None:
        self.filepath: str = filepath
        self.name: str = ""
        self.raw_data: list[str] = []
        self.ability_scores: dict[str, int] = {}
        self.skill_modifiers: dict[str, int] = {}
        self.load_player_from_DND_Beyond_pdf()

    @typeguard.typechecked
    def load_player_from_DND_Beyond_pdf(self) -> None:
        with open(f"Players/{self.filepath}.pdf", "rb+") as file:
            binary_data = file.read().split("\n".encode("utf-8"))

        self.raw_data = []
        for line in binary_data:
            try:
                self.raw_data.append(line.decode("utf-8"))
            except UnicodeDecodeError:
                continue

        # Why DND Beyond, why?
        self.name = self.raw_data[self.raw_data.index("/T(CharacterName)") + 6][3:].split(")")[0]

        self.ability_scores["strength"] = self.parseAbilityScore("STRmod")
        self.ability_scores["dexterity"] = self.parseAbilityScore("DEXmod ")
        self.ability_scores["constitution"] = self.parseAbilityScore("CONmod")
        self.ability_scores["intelligence"] = self.parseAbilityScore("INTmod")
        self.ability_scores["wisdom"] = self.parseAbilityScore("WISmod")
        self.ability_scores["charisma"] = self.parseAbilityScore("CHamod")

        self.skill_modifiers["strengthSave"] = self.parseSaveModifier("Strength")
        self.skill_modifiers["athletics"] = self.parseSkillModifier("Athletics")

        self.skill_modifiers["dexteritySave"] = self.parseSaveModifier("Dexterity")
        self.skill_modifiers["acrobatics"] = self.parseSkillModifier("Acrobatics")
        self.skill_modifiers["sleightOfHand"] = self.parseSkillModifier("SleightofHand")
        self.skill_modifiers["stealth"] = self.parseSkillModifier("Stealth ")

        self.skill_modifiers["constitutionSave"] = self.parseSaveModifier("Constitution")

        self.skill_modifiers["intelligenceSave"] = self.parseSaveModifier("Intelligence")
        self.skill_modifiers["arcana"] = self.parseSkillModifier("Arcana")
        self.skill_modifiers["history"] = self.parseSkillModifier("History")
        self.skill_modifiers["investigation"] = self.parseSkillModifier("Investigation")
        self.skill_modifiers["nature"] = self.parseSkillModifier("Nature")
        self.skill_modifiers["religion"] = self.parseSkillModifier("Religion")

        self.skill_modifiers["wisdomSave"] = self.parseSaveModifier("Wisdom")
        self.skill_modifiers["animalHandling"] = self.parseSkillModifier("Animal")
        self.skill_modifiers["insight"] = self.parseSkillModifier("Insight")
        self.skill_modifiers["medicine"] = self.parseSkillModifier("Medicine")
        self.skill_modifiers["perception"] = self.parseSkillModifier("Perception")
        self.skill_modifiers["survival"] = self.parseSkillModifier("Survival")

        self.skill_modifiers["charismaSave"] = self.parseSaveModifier("Charisma")
        self.skill_modifiers["deception"] = self.parseSkillModifier("Deception")
        self.skill_modifiers["intimidation"] = self.parseSkillModifier("Intimidation")
        self.skill_modifiers["performance"] = self.parseSkillModifier("Performance")
        self.skill_modifiers["persuasion"] = self.parseSkillModifier("Persuasion")

    @ typeguard.typechecked
    def parseAbilityScore(self, ability_score: str):
        return int(self.raw_data[self.raw_data.index("/T(" + ability_score + ")") + 36][1:].split(")")[0])

    @typeguard.typechecked
    def parseSkillModifier(self, skill: str):
        return int(self.raw_data[self.raw_data.index("/T(" + skill + ")") + 36][1:].split(")")[0])

    @typeguard.typechecked
    def parseSaveModifier(self, save: str):
        return int(self.raw_data[self.raw_data.index("/T(ST " + save + ")") + 36][1:].split(")")[0])
    
    @typeguard.typechecked
    def get_ability_score(self, ability: str, as_string: bool = False) -> any:
        score = self.ability_scores[ability]
        return str(score) if as_string else score

    @typeguard.typechecked
    def score_to_modifier(self, score: int) -> int:
        return math.floor((score - 10) / 2)

    @typeguard.typechecked
    def get_data(self, player_id) -> dict:
        stats: dict[str, int] = {ability: self.score_to_modifier(score) for ability, score in self.ability_scores.items()}
        stats.update({skill: modifier for skill, modifier in self.skill_modifiers.items()})
        return {"id": player_id, "name": self.name, "stats": stats}
