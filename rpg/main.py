from agno.agent import Agent
from agno.models.openai import OpenAIChat
from enum import Enum
from pydantic import BaseModel
from typing import List
from rich import print


class CharacterLevel(Enum):
    LOW = "baixo"
    MEDIUM = "médio"
    HIGH = "alto"


class Race(Enum):
    HUMAN = "Humano"
    ELF = "Elfo"
    DWARF = "Anão"
    ORC = "Orc"
    TIEFLING = "Tiefling"
    LIZARDFOLK = "Lizardfolk"
    DRAGONBORN = "Dragonborn"
    HALFLING = "Halfling"


class Character(BaseModel):
    name: str
    bio: str
    race: Race
    class_: str
    level: CharacterLevel
    health: int
    mana: int
    strength: int
    dexterity: int
    constitution: int
    intelligence: int
    wisdom: int
    charisma: int


class Team(BaseModel):
    characters: List[Character] = []
    def add_character(self, Race, CharacterLevel):
        response = character_generator.run(f"Gere um personagem {Race.value} de nível {CharacterLevel.value}")
        self.characters.append(response.content)


character_generator = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    name="rpg-character-generator",
    instructions="""
        Você é um gerador de personagens de RPG.
        Seu objetivo é criar personagens únicos e interessantes com base nas instruções fornecidas pelo usuário.
    """,
    output_schema=Character,
    debug_mode=False,
)


if __name__ == "__main__":
    team = Team()
    team.add_character(Race.HUMAN, CharacterLevel.MEDIUM)
    team.add_character(Race.ELF, CharacterLevel.MEDIUM)
    team.add_character(Race.DWARF, CharacterLevel.MEDIUM)

    print(team.model_dump_json(indent=2))
