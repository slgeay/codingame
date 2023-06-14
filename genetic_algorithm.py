from __future__ import annotations
import ast

import subprocess
from math import ceil
from multiprocessing import Pool
from multiprocessing.pool import AsyncResult
from os import cpu_count, mkdir, scandir
from os.path import isdir
from random import randint, random, randrange, sample, uniform
from re import match
from shutil import rmtree
from typing import Generic, List, Optional, Tuple, TypeVar
from uuid import uuid4

from ai import WEIGHTS_COUNT, clamp, Spring2023AntsAI
from numpy.random import choice

CHROMOSOME_SIZE = WEIGHTS_COUNT
POPULATION_SIZE = 50

ELITE_RATIO = 0.2
CHROMOSOME_MUTATE_RATIO = 0.9
GENE_MUTATE_RATIO = 0.1
CROSSOVER_RATIO = 0.1
PREVIOUS_SCORE_RATIO = 1

GENERATIONS_MAX = 10000

POOL_SIZE = cpu_count() // 2
ROUNDS_PER_GENERATION = 50


def unzip(zipped) -> Tuple:
    return tuple(zip(*zipped))


def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


def generic_arg(cls, i: int):
    return cls.__orig_bases__[0].__args__[i]


class Gene:
    def __init__(self):
        pass

    @classmethod
    def random(cls, previous: Optional[Gene] = None) -> Gene:
        pass

    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return str(self)

    def copy(self) -> Gene:
        pass

    def crossover(
        self, weight: float, inv_weight: float, gene_2: Gene
    ) -> Tuple[Gene, Gene]:
        pass

    def mutate(self, previous: Optional[Gene] = None) -> None:
        pass


G = TypeVar("G", bound=Gene)


class Chromosome(Generic[G]):
    generation: int
    id: str
    genes: List[G]

    @classmethod
    def _G(cls) -> type[G]:
        return generic_arg(cls, 0)

    def __init__(self, generation: int, genes: List[G], id: Optional[str] = None):
        self.generation = generation
        self.id = id or str(uuid4())
        self.genes = [gene.copy() for gene in genes]  # type: ignore

    @classmethod
    def random(cls, generation: int, size: int) -> Chromosome:
        gene = None
        genes = []
        for _ in range(size):
            gene = cls._G().random(gene)
            genes.append(gene)

        return cls(generation=generation, genes=genes)  # type: ignore

    def __str__(self) -> str:
        return f"({self.generation})<{';'.join([str(gene) for gene in self.genes])}>"

    def __repr__(self) -> str:
        return str(self)

    def run(self, round: int):
        return str(self.genes[round])

    def copy(self) -> Chromosome:
        print(f"Copying {self.generation:05}_{self.id}")
        return self.__class__(
            generation=self.generation,
            id=self.id,
            genes=[gene.copy() for gene in self.genes],  # type: ignore
        )

    def crossover(
        self, generation: int, parent_2: Chromosome
    ) -> Tuple[Chromosome, Chromosome]:
        weight = uniform(0.02, 0.98)
        inv_weight = 1 - weight
        child_1_genes, child_2_genes = unzip(
            [
                gene_1.crossover(weight, inv_weight, gene_2)
                for gene_1, gene_2 in zip(self.genes, parent_2.genes)
            ]
        )

        return (
            self.__class__(generation=generation, genes=child_1_genes),
            self.__class__(generation=generation, genes=child_2_genes),
        )

    def mutate(self, gene_mutate_ratio) -> None:
        for i in sample(
            range(len(self.genes)), ceil(len(self.genes) * gene_mutate_ratio)
        ):
            self.genes[i].mutate(self.genes[i - 1] if i > 0 else None)


C = TypeVar("C", bound=Chromosome)


class Population(Generic[C]):
    generation: int
    chromosomes: List[C] = []

    @classmethod
    def _C(cls) -> type[C]:
        return generic_arg(cls, 0)

    def __init__(self, generation, chromosomes):
        self.generation = generation
        self.chromosomes = chromosomes

    @classmethod
    def random(cls, population_size: int, chromozome_size: int) -> Population:
        return cls(
            generation=0,
            chromosomes=[
                cls._C().random(0, chromozome_size) for _ in range(population_size)
            ],
        )

    def __str__(self) -> str:
        return f"\nGeneration {self.generation}:\n" + "\n".join(
            [str(chromosome) for chromosome in self.chromosomes]
        )

    def __repr__(self) -> str:
        return str(self)

    def copy(self) -> Population:
        return self.__class__(
            generation=self.generation,
            chromosomes=[chromosome.copy() for chromosome in self.chromosomes],
        )


P = TypeVar("P", bound=Population)


class GeneticAlgorithm(Generic[P]):
    chromosome_size: int
    population_size: int
    generations_max: float
    elite_ratio: float
    chromosome_mutate_ratio: float
    gene_mutate_ratio: float
    crossover_ratio: float
    population: P
    scores: List[float]

    @classmethod
    def _P(cls) -> type[P]:
        return generic_arg(cls, 0)

    def __init__(
        self,
        chromosome_size: int = CHROMOSOME_SIZE,
        population_size: int = POPULATION_SIZE,
        generations_max: float = GENERATIONS_MAX,
        elite_ratio: float = ELITE_RATIO,
        chromosome_mutate_ratio: float = CHROMOSOME_MUTATE_RATIO,
        gene_mutate_ratio: float = GENE_MUTATE_RATIO,
        crossover_ratio: float = CROSSOVER_RATIO,
    ):
        self.chromosome_size = chromosome_size
        self.population_size = population_size
        self.generations_max = generations_max
        self.elite_ratio = elite_ratio
        self.chromosome_mutate_ratio = chromosome_mutate_ratio
        self.gene_mutate_ratio = gene_mutate_ratio
        self.crossover_ratio = crossover_ratio

    def run(self):
        self.initialize()
        generation = 0
        for generation in range(self.generations_max + 1):
            self.select()
            self.reproduce_and_mutate(generation + 1)

            best: C = self.population.chromosomes[0]
            print(
                f"Generation {generation:05}: {best.generation}_{best.id} ({self.scores[0]})"
            )
            print(str(self.scores))

            with open(f".bests/{generation:05}_{best.id}.txt", "w") as f:
                f.write(str(best))

    def initialize(self) -> None:
        print("initialize")
        chromosomes: List[C] = []  # type: ignore
        if isdir(".bests"):
            for filename in scandir(".bests"):
                if filename.is_file():
                    with open(filename, "r") as f:
                        chromosomes.append(self._P()._C().from_str(0, f.read()))

        print(f"Read {len(chromosomes)} chromosomes")

        for _ in range(len(chromosomes), self.population_size):
            chromosomes.append(self._P()._C().random(0, self.chromosome_size))

        print(f"First generation: {len(chromosomes)} chromosomes")

        self.population = self._P()(0, chromosomes)
        print("initialization done")

    def select(self) -> None:
        self.compute_fitness()

    def compute_fitness(self) -> None:
        self.scores = [
            self.get_score(chromosome) for chromosome in self.population.chromosomes
        ]

    def get_score(self, chromosome: C) -> float:
        pass

    def sort(
        self, scores: List[float], chromosomes: List[C]
    ) -> Tuple[List[float], List[C]]:
        return unzip(  # type: ignore
            sorted(
                zip(scores, chromosomes),
                key=lambda z: z[0],
                reverse=True,
            )
        )

    def normalize(self, scores: List[float]) -> List[float]:
        lower_score = min(scores)
        total = sum([score - lower_score for score in scores])
        return (
            [(score - lower_score) / total for score in scores]
            if total != 0
            else [1 / len(scores)] * len(scores)
        )

    def reproduce_and_mutate(self, generation: int) -> None:
        self.scores, self.population.chromosomes = self.sort(self.scores, self.population.chromosomes)  # type: ignore

        self.chromosome_mutate_ratio = generation / self.generations_max
        self.crossover_ratio = 1 - generation / self.generations_max

        elite_size = ceil(self.population_size * self.elite_ratio)
        new_chromosomes = [
            chromosome.copy() for chromosome in self.population.chromosomes[:elite_size]
        ]

        scores = self.normalize(self.scores)
        pool_size = self.population_size - elite_size
        parents = choice(
            self.population.chromosomes,
            size=pool_size if pool_size % 2 == 0 else pool_size + 1,
            p=scores,
        )

        for parent_1, parent_2 in pairwise(parents):
            if random() <= self.crossover_ratio:
                child_1, child_2 = parent_1.crossover(generation, parent_2)
            else:
                child_1 = parent_1.copy()
                child_2 = parent_2.copy()

            if random() <= self.chromosome_mutate_ratio:
                child_1.mutate(self.gene_mutate_ratio)
                child_1.generation = generation
            if random() <= self.chromosome_mutate_ratio:
                child_2.mutate(self.gene_mutate_ratio)
                child_2.generation = generation

            new_chromosomes.append(child_1)
            if len(new_chromosomes) < self.population_size:
                new_chromosomes.append(child_2)

        self.population = self._P()(generation, new_chromosomes)


JAR = "..\\SpringChallenge2023\\target\\spring-2023-ants-1.0-SNAPSHOT.jar;..\\SpringChallenge2023\\target\\lib\\*"
MAIN = "MySpring2023Main"
AI = "..\\cg-23-spring\\ai.py"
PREFIX = "..\\cg-23-spring\\"
GENE_MIN = -500
GENE_MAX = 500


class Spring2023AntsGene(Gene):
    synapse_weight: float

    def __init__(self, synapse_weight: Optional[float] = None):
        self.synapse_weight = round(clamp(
            self._random() if synapse_weight is None else synapse_weight,
            GENE_MIN,
            GENE_MAX,
        ),5)

    @classmethod
    def random(cls, _: Optional[Gene] = None) -> Spring2023AntsGene:
        return cls(cls._random())

    @classmethod
    def _random(cls) -> int:
        return sample([uniform(GENE_MIN, GENE_MAX), uniform(-1, 1), 0], 1, counts=[2, 2, 6])[0]

    def __str__(self) -> str:
        return str(self.synapse_weight)

    @classmethod
    def from_str(cls, c: str) -> Spring2023AntsGene:
        return cls(float(c))

    def copy(self) -> Spring2023AntsGene:
        return self.__class__(synapse_weight=self.synapse_weight)

    def crossover(
        self, w1: float, w2: float, gene_2: Gene
    ) -> Tuple[Spring2023AntsGene, Spring2023AntsGene]:
        assert gene_2 is None or isinstance(gene_2, self.__class__)
        return self.__class__(
            w1 * self.synapse_weight + w2 * gene_2.synapse_weight,
        ), self.__class__(
            w2 * self.synapse_weight + w1 * gene_2.synapse_weight,
        )

    def mutate(self, _: Optional[Gene] = None) -> None:
        delta = max(0.5, abs(self.synapse_weight) * 0.1)
        self.synapse_weight = uniform(self.synapse_weight - delta, self.synapse_weight + delta)


class Spring2023AntsChromosome(Chromosome[Spring2023AntsGene]):
    last_score: float = 1200

    def __init__(self, generation: int, genes: List[G], id: Optional[str] = None):
        super().__init__(generation, genes, id)  # type: ignore
        self.last_score = 1200

    def set_last_score(self, score: float):
        self.last_score = score

    def get_last_score(self) -> float:
        return self.last_score

    def __str__(self) -> str:
        return ",".join([str(gene) for gene in self.genes])

    def get_file_name(self) -> str:
        return f".chromosomes/{self.generation:05}_{self.id}.txt"

    def encode(self) -> None:
        with open(self.get_file_name(), "wt") as f:
            f.write(str(self))

    @classmethod
    def from_str(cls, generation: int, string: str) -> Spring2023AntsChromosome:
        return cls(generation, [Spring2023AntsGene(gene) for gene in Spring2023AntsAI.read_weights(string)])  # type: ignore

    def copy(self) -> Spring2023AntsChromosome:
        print(f"Copying {self.generation:05}_{self.id}")
        self_copy = self.__class__(
            generation=self.generation,
            id=self.id,
            genes=[gene.copy() for gene in self.genes],  # type: ignore
        )
        self_copy.set_last_score(self.get_last_score() * PREVIOUS_SCORE_RATIO)
        return self_copy


class Spring2023AntsPopulation(Population[Spring2023AntsChromosome]):
    def encode(self) -> None:
        for chromosome in self.chromosomes:
            chromosome.encode()


def update_elo(rating1, rating2, score1, score2, K=32):
    # calculate expected scores
    expected1 = 1 / (1 + 10 ** ((rating2 - rating1) / 400))
    expected2 = 1 / (1 + 10 ** ((rating1 - rating2) / 400))

    # update ratings
    new_rating1 = rating1 + K * (score1 - expected1)
    new_rating2 = rating2 + K * (score2 - expected2)

    return new_rating1, new_rating2


class Spring2023AntsGeneticAlgorithm(GeneticAlgorithm[Spring2023AntsPopulation]):
    def __init__(self):
        super().__init__()
        rmtree(".chromosomes", ignore_errors=True)
        mkdir(".chromosomes")

    def compute_fitness(self) -> None:
        self.population.encode()
        population_size = len(self.population.chromosomes)
        scores = []

        for i in range(population_size):
            scores.append(self.population.chromosomes[i].get_last_score())

        # print(scores)
        pool = Pool(POOL_SIZE)

        results: List[Tuple[int, int, AsyncResult]] = []

        for _ in range(ROUNDS_PER_GENERATION):
            bracket = pairwise(sample(range(population_size), population_size))

            for player_1, player_2 in bracket:
                results.append(
                    (
                        player_1,
                        player_2,
                        pool.apply_async(
                            self.launch_duel,
                            (
                                self.population.chromosomes[player_1],
                                self.population.chromosomes[player_2],
                            ),
                        ),
                    )
                )

        for player_1, player_2, res in results:
            result = res.get()
            assert result[0] != -1 and result[1] != -1, result
            # print(self.population.chromosomes[player_1].id, self.population.chromosomes[player_2].id)
            # print(result)
            if result[0] == result[1]:
                r0 = 0.5
            else:
                r0 = (0.8 if result[0] > result[1] else 0) + 0.2 * result[0] / (result[0] + result[1])
            # print(scores[player_1], scores[player_2], r0, 1 - r0)
            scores[player_1], scores[player_2] = update_elo(
                scores[player_1], scores[player_2], r0, 1 - r0
            )
            # print(scores[player_1], scores[player_2])
            print(".", end="", flush=True)

        # print(scores)
        print("\n", end="", flush=True)

        for i in range(population_size):
            self.population.chromosomes[i].set_last_score(scores[i])

        self.scores = [round(score, 2) for score in scores]

    def launch_duel(
        self,
        chromosome_1: Spring2023AntsChromosome,
        chromosome_2: Spring2023AntsChromosome,
    ) -> Tuple[int, int]:
        for _ in range(3):
            try:
                result = subprocess.run(
                    [
                        "java",
                        "-cp",
                        JAR,
                        MAIN,
                        AI,
                        PREFIX + chromosome_1.get_file_name(),
                        AI,
                        PREFIX + chromosome_2.get_file_name(),
                    ],
                    stdout=subprocess.PIPE,
                )

                scores = ast.literal_eval(
                    result.stdout.decode("utf-8").replace("=", ":")
                )
                return scores[0], scores[1]
            except BaseException as err:
                print(f"Unexpected {err=}, {type(err)=}")

        return (0, 0)
