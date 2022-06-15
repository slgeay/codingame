from __future__ import annotations

from random import randint, random, uniform
from typing import Generic, List, Optional, Tuple, TypeVar

from numpy.random import choice

CHROMOSOME_SIZE = 10
POPULATION_SIZE = 100
GENERATION_SIZE = 50

ELITE_RATIO = 0.1
MUTATE_RATIO = 0.1


# Comment on CodinGame
def input() -> str:
    return ""


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

    def mutate(self):
        i = randint(0, len(self.genes) - 1)
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
    mutate_ratio: float
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
        mutate_ratio: float = MUTATE_RATIO,
    ):
        self.chromosome_size = chromosome_size
        self.population_size = population_size
        self.generation_size = generation_size
        self.elite_ratio = elite_ratio
        self.mutate_ratio = mutate_ratio
        self.populations = []
        self.scores = []

    def run(self):
        self.initialize()
        for generation in range(1, self.generation_size + 1):
            self.select()
            self.reproduce_and_mutate(generation)
        # print(self.populations)

    def initialize(self) -> None:
        self.populations = [
            self._P().random(self.population_size, self.chromosome_size)  # type: ignore
        ]

    def select(self) -> None:
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
        parents = choice(pool, size=self.population_size - elite_size, p=scores)

        for parent_1, parent_2 in pairwise(parents):
            child_1, child_2 = parent_1.crossover(generation, parent_2)
            if random() <= self.mutate_ratio:
                child_1.mutate()
            if random() <= self.mutate_ratio:
                child_2.mutate()

            new_population.append(child_1)
            new_population.append(child_2)

        self.populations.append(self._P()(generation, new_population))


class BaseGene(Gene):
    rotate: int
    power: int

    def __init__(self, rotate: int, power: int):
        self.rotate = rotate
        self.power = power

    @classmethod
    def random(cls, previous: Optional[Gene] = None) -> BaseGene:
        assert previous is None or isinstance(previous, BaseGene)
        return cls(cls.random_rotate(previous), cls.random_power(previous))

    @classmethod
    def random_rotate(cls, previous: Optional[Gene] = None) -> int:
        assert previous is None or isinstance(previous, BaseGene)
        return min(
            90,
            max(-90, randint(-15, 15) + (0 if previous is None else previous.rotate)),
        )

    @classmethod
    def random_power(cls, previous: Optional[Gene] = None) -> int:
        assert previous is None or isinstance(previous, BaseGene)
        return min(
            0, max(4, randint(-1, 1) + (0 if previous is None else previous.power))
        )

    def __str__(self) -> str:
        return f"{self.rotate} {self.power}"

    def copy(self) -> BaseGene:
        return self.__class__(rotate=self.rotate, power=self.power)

    def crossover(
        self, weight: float, inv_weight: float, gene_2: Gene
    ) -> Tuple[BaseGene, BaseGene]:
        assert gene_2 is None or isinstance(gene_2, BaseGene)
        return self.__class__(
            round(self.rotate * weight + gene_2.rotate * inv_weight),
            round(self.power * weight + gene_2.power * inv_weight),
        ), self.__class__(
            round(self.rotate * inv_weight + gene_2.rotate * weight),
            round(self.power * inv_weight + gene_2.power * weight),
        )

    def mutate(self, previous: Optional[Gene] = None) -> None:
        assert previous is None or isinstance(previous, BaseGene)
        self.rotate = BaseGene.random_rotate(previous)
        self.power = BaseGene.random_power(previous)


class BaseChromosome(Chromosome[BaseGene]):
    pass


class BasePopulation(Population[BaseChromosome]):
    pass


class BaseGeneticAlgorithm(GeneticAlgorithm[BasePopulation]):
    def get_score(self, chromosome: Chromosome) -> float:
        assert isinstance(chromosome, BaseChromosome)
        return sum(
            [gene.rotate + gene.power for gene in chromosome.genes]
        )  # todo: change
