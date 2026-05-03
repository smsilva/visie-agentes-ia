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


def create_character(race: Race, level: CharacterLevel) -> str:
    """
    Gera um personagem de RPG com a raça e nível especificados.
    """
    response = character_generator.run(f"Gere um personagem {race.value} de nível {level.value}")
    return response.content.model_dump_json()


team_generator = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    name="rpg-team-generator",
    tools=[create_character],
    instructions="""
        Você é um gerador de times de RPG.
        Com base na instrução do usuário, decida a composição do time e use a tool create_character
        para criar cada personagem. Monte o time completo antes de retornar.
    """,
    output_schema=Team,
    debug_mode=True,
)

def create_team(instruction: str) -> Team:
    """
    Gera um time de RPG com base na instrução fornecida.
    """
    response = team_generator.run(instruction)
    return response.content


if __name__ == "__main__":
    heroes = create_team("monte um time com 2 heróis")
    vilains = create_team("monte um time com 2 vilões")
    print(heroes.model_dump_json(indent=2))
    print(vilains.model_dump_json(indent=2))
