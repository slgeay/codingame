from __future__ import annotations

from math import ceil
from multiprocessing import Pool
from multiprocessing.pool import AsyncResult
from os import sched_getaffinity
from random import randint, random, sample, uniform
import subprocess
from time import time
from typing import Generic, List, Optional, Tuple, TypeVar

from numpy.random import choice

CHROMOSOME_SIZE = 10#36315
POPULATION_SIZE = 100
GENERATION_SIZE = 10

ELITE_RATIO = 0.1
CHROMOSOME_MUTATE_RATIO = 0.001
GENE_MUTATE_RATIO = 0.1

POOL_SIZE = 3


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
    genes: List[G]

    @classmethod
    def _G(cls) -> type[G]:
        return generic_arg(cls, 0)

    def __init__(self, generation: int, genes: List[G]):
        self.genes = [gene.copy() for gene in genes]  # type: ignore
        self.generation = generation

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
        return self.__class__(
            generation=self.generation,
            genes=[gene.copy() for gene in self.genes],  # type: ignore
        )

    def crossover(
        self, generation: int, parent_2: Chromosome
    ) -> Tuple[Chromosome, Chromosome]:
        weight = uniform(0.1, 0.9)
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
        for i in sample(range(len(self.genes)), ceil(len(self.genes) * gene_mutate_ratio)):
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
    generation_size: int
    elite_ratio: float
    chromosome_mutate_ratio: float
    gene_mutate_ratio: float
    populations: List[P]
    scores: List[List[float]]

    @classmethod
    def _P(cls) -> type[P]:
        return generic_arg(cls, 0)

    def __init__(
        self,
        chromosome_size: int = CHROMOSOME_SIZE,
        population_size: int = POPULATION_SIZE,
        generation_size: int = GENERATION_SIZE,
        elite_ratio: float = ELITE_RATIO,
        chromosome_mutate_ratio: float = CHROMOSOME_MUTATE_RATIO,
        gene_mutate_ratio: float = GENE_MUTATE_RATIO,
    ):
        self.chromosome_size = chromosome_size
        self.population_size = population_size
        self.generation_size = generation_size
        self.elite_ratio = elite_ratio
        self.chromosome_mutate_ratio = chromosome_mutate_ratio
        self.gene_mutate_ratio = gene_mutate_ratio
        self.populations = []
        self.scores = []

    def run(self):
        self.initialize()
        for generation in range(1, self.generation_size + 1):
            self.select()
            self.reproduce_and_mutate(generation)
        print(self.populations[-1].chromosomes[0])

    def initialize(self) -> None:
        self.populations = [
            self._P().random(self.population_size, self.chromosome_size)  # type: ignore
        ]

    def select(self) -> None:
        self.compute_fitness()

    def compute_fitness(self) -> None:
        self.scores.append(
            [
                self.get_score(chromosome)
                for chromosome in self.populations[-1].chromosomes
            ]
        )

    def get_score(self, chromosome: C) -> float:
        pass

    def sort(self, scores: List[float], population: P) -> Tuple[List[float], List[C]]:
        return unzip(  # type: ignore
            sorted(
                zip(scores, population.chromosomes),
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
        scores, pool = self.sort(self.scores[-1], self.populations[-1])  # type: ignore

        elite_size = round(self.population_size * self.elite_ratio)
        new_population = [chromosome.copy() for chromosome in pool[:elite_size]]

        scores = self.normalize(scores)
        pool_size = self.population_size - elite_size
        parents = choice(pool, size=pool_size if pool_size % 2 == 0 else pool_size + 1, p=scores)

        for parent_1, parent_2 in pairwise(parents):
            child_1, child_2 = parent_1.crossover(generation, parent_2)
            if random() <= self.chromosome_mutate_ratio:
                child_1.mutate(self.gene_mutate_ratio)
            if random() <= self.chromosome_mutate_ratio:
                child_2.mutate(self.gene_mutate_ratio)

            new_population.append(child_1)
            if len(new_population) < self.population_size:
                new_population.append(child_2)


        self.populations.append(self._P()(generation, new_population))


ROUNDS_PER_GENERATION = 10


class GreenCircleGene(Gene):
    synapse_weight: float

    def __init__(self, synapse_weight: Optional[float] = None):
        self.synapse_weight = synapse_weight or self._random()

    @classmethod
    def random(cls, _: Optional[Gene] = None) -> GreenCircleGene:
        return cls(
            cls._random()
        )

    @classmethod
    def _random(cls) -> float:
        return uniform(0, 1)

    def __str__(self) -> str:
        return f"{self.synapse_weight:.2f}"

    def copy(self) -> GreenCircleGene:
        return self.__class__(synapse_weight=self.synapse_weight)

    def crossover(
        self, weight: float, inv_weight: float, gene_2: Gene
    ) -> Tuple[GreenCircleGene, GreenCircleGene]:
        assert gene_2 is None or isinstance(gene_2, self.__class__)
        return self.__class__(
            weight * self.synapse_weight + inv_weight * gene_2.synapse_weight,
        ), self.__class__(
            inv_weight * self.synapse_weight + weight * gene_2.synapse_weight,
        )

    def mutate(self, _: Optional[Gene] = None) -> None:
        self.synapse_weight = self._random()


class GreenCircleChromosome(Chromosome[GreenCircleGene]):
    def encode(self) -> str:
        return " ".join(
            [
                str(gene)
                for gene in self.genes
            ]
        )


class GreenCirclePopulation(Population[GreenCircleChromosome]):
    pass


class GreenCircleGeneticAlgorithm(GeneticAlgorithm[GreenCirclePopulation]):

    def compute_fitness(self) -> None:
        scores = [0] * self.population_size
        pool = Pool(POOL_SIZE)

        results: List[Tuple[int, int, AsyncResult]] = []

        for _ in range(ROUNDS_PER_GENERATION):
            bracket = pairwise(sample(range(self.population_size), self.population_size))

            for player_1, player_2 in bracket:
                results.append((player_1, player_2, pool.apply_async(self.launch_duel, (self.populations[-1].chromosomes[player_1], self.populations[-1].chromosomes[player_2]))))
                #result = self.launch_duel(self.populations[-1].chromosomes[player_1], self.populations[-1].chromosomes[player_2])

        for player_1, player_2, res in results:
            result = res.get()
            # print(result)
            if result[0] > result[1]:
                scores[player_1] += 1
                scores[player_2] -= 1
            elif result[0] < result[1]:
                scores[player_1] -= 1
                scores[player_2] += 1

        self.scores.append(scores)


    def launch_duel(self, chromosome_1: GreenCircleChromosome, chromosome_2: GreenCircleChromosome) -> Tuple[int, int]:
        for _ in range(3):
            try:
                result = subprocess.run(["/usr/lib/jvm/java-8-openjdk-amd64/bin/java", "-cp", "/tmp/cp_7wdcdfymzs7kpssaoh0wot2cw.jar", "SkeletonMain", chromosome_1.encode(), chromosome_2.encode()], stdout=subprocess.PIPE)
                # print(result)
                # print(score)
                # with open('log.txt', 'w') as f:
                #     f.write("\n".join(result.stdout.decode('utf-8').splitlines()[:-1]))
                scores = (tuple([int(score) for score in result.stdout.decode('utf-8').splitlines()[-1].split(' ')]))
                return scores
            except:
                pass
        return (0, 0)
