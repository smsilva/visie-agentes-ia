import time
import functools
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from enum import Enum
from pydantic import BaseModel
from typing import List, Callable
from rich import print
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.resources import Resource

_resource = Resource.create(
    {
        "service.name": "rpg-agent",
        "user": "rpg-agent-user@ciandt.com",
        "team": "cloud",
        "tenant": "flowteam"
    }
)
_exporter = OTLPMetricExporter()
_reader = PeriodicExportingMetricReader(_exporter, export_interval_millis=5000)
_provider = MeterProvider(resource=_resource, metric_readers=[_reader])
metrics.set_meter_provider(_provider)

_meter = metrics.get_meter("rpg-agent")
_characters_counter = _meter.create_counter(
    "rpg.characters.created",
    description="Número de personagens criados",
)
_teams_counter = _meter.create_counter(
    "rpg.teams.created",
    description="Número de times criados",
)
_character_duration = _meter.create_histogram(
    "rpg.character.generation.duration",
    unit="s",
    description="Tempo de geração de personagem",
)
_team_duration = _meter.create_histogram(
    "rpg.team.generation.duration",
    unit="s",
    description="Tempo de geração de time",
)


def record_metrics(counter, histogram, label_fn: Callable):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            t0 = time.perf_counter()
            result = fn(*args, **kwargs)
            labels = label_fn(*args, result=result, **kwargs)
            histogram.record(time.perf_counter() - t0, labels)
            counter.add(1, labels)
            return result
        return wrapper
    return decorator


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


@record_metrics(
    _characters_counter,
    _character_duration,
    lambda race, level, result=None: {"race": race.value, "level": level.value},
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

@record_metrics(
    _teams_counter,
    _team_duration,
    lambda instruction, result=None: {"size": str(len(result.characters))} if result else {},
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
    _provider.force_flush()
