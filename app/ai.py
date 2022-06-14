from __future__ import annotations

from random import randint, random, uniform
from typing import List, Optional, Tuple

from numpy.random import choice

CHROMOSOME_SIZE = 10
POPULATION_SIZE = 100
GENERATION_SIZE = 50

ELITE_RATIO = 0.1
MUTATE_RATIO = 0.1


## Comment on CodinGame
def input() -> str:
    return ""


def unzip(zipped) -> Tuple:
    return tuple(zip(*zipped))


def pairwise(iterable):
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    a = iter(iterable)
    return zip(a, a)


class Gene:
    rotate: int
    power: int

    def __init__(self, rotate: int, power: int):
        self.rotate = rotate
        self.power = power

    def check(self):
        rotate = min(90, max(-90, rotate))
        power = min(4, max(0, power))

    @classmethod
    def random(cls, previous: Optional[Gene] = None) -> Gene:
        return cls(cls.random_rotate(previous), cls.random_power(previous))

    @classmethod
    def random_rotate(cls, previous: Optional[Gene] = None) -> int:
        return min(
            90,
            max(-90, randint(-15, 15) + (0 if previous is None else previous.rotate)),
        )

    @classmethod
    def random_power(cls, previous: Optional[Gene] = None) -> int:
        return min(
            0, max(4, randint(-1, 1) + (0 if previous is None else previous.power))
        )

    def __str__(self) -> str:
        return f"{self.rotate} {self.power}"

    def __repr__(self) -> str:
        return str(self)

    def copy(self) -> Gene:
        return Gene(rotate=self.rotate, power=self.power)

    @classmethod
    def crossover(
        cls, weight: float, inv_weight: float, gene_1: Gene, gene_2: Gene
    ) -> Tuple[Gene, Gene]:
        return Gene(
            round(gene_1.rotate * weight + gene_2.rotate * inv_weight),
            round(gene_1.power * weight + gene_2.power * inv_weight),
        ), Gene(
            round(gene_1.rotate * inv_weight + gene_2.rotate * weight),
            round(gene_1.power * inv_weight + gene_2.power * weight),
        )

    def mutate(self, previous: Optional[Gene] = None) -> None:
        self.rotate = Gene.random_rotate(previous)
        self.power = Gene.random_power(previous)


class Chromosome:
    generation: int
    genes: List[Gene]

    def __init__(self, generation: int, genes: List[Gene]):
        self.genes = [gene.copy() for gene in genes]
        self.generation = generation

    @classmethod
    def random(cls, generation: int) -> Chromosome:
        gene = None
        genes = []
        for _ in range(CHROMOSOME_SIZE):
            gene = Gene.random(gene)
            genes.append(gene)

        return cls(generation=generation, genes=genes)

    def __str__(self) -> str:
        return f"({self.generation})<{';'.join([str(gene) for gene in self.genes])}>"

    def __repr__(self) -> str:
        return str(self)

    def run(self, round: int):
        return str(self.genes[round])

    def copy(self) -> Chromosome:
        return Chromosome(
            generation=self.generation, genes=[gene.copy() for gene in self.genes]
        )

    @classmethod
    def crossover(
        cls, generation: int, parent_1: Chromosome, parent_2: Chromosome
    ) -> Tuple[Chromosome, Chromosome]:
        weight = uniform(0.1, 0.9)
        inv_weight = 1 - weight
        child_1_genes, child_2_genes = unzip(
            [
                Gene.crossover(weight, inv_weight, gene_1, gene_2)
                for gene_1, gene_2 in zip(parent_1.genes, parent_2.genes)
            ]
        )

        return (
            Chromosome(generation=generation, genes=child_1_genes),
            Chromosome(generation=generation, genes=child_2_genes),
        )

    def mutate(self):
        i = randint(0, len(self.genes) - 1)
        self.genes[i].mutate(self.genes[i - 1] if i > 0 else None)


class Population:
    generation: int
    chromosomes: List[Chromosome] = []

    def __init__(self, generation, chromosomes):
        self.generation = generation
        self.chromosomes = chromosomes

    @classmethod
    def random(cls, size: int = POPULATION_SIZE) -> Population:
        return cls(
            generation=0,
            chromosomes=[Chromosome.random(0) for _ in range(size)],
        )

    def __str__(self) -> str:
        return f"\nGeneration {self.generation}:\n" + "\n".join(
            [str(chromosome) for chromosome in self.chromosomes]
        ) 

    def __repr__(self) -> str:
        return str(self)

    def copy(self) -> Population:
        return Population(
            generation=self.generation,
            chromosomes=[chromosome.copy() for chromosome in self.chromosomes],
        )


class AI:
    populations: List[Population]
    scores: List[float]

    def __init__(self):
        pass

    def run(self):
        self.initialize()
        for generation in range(1, GENERATION_SIZE + 1):
            self.select()
            self.reproduce_and_mutate(generation)


    def initialize(self):
        self.populations = [Population.random(POPULATION_SIZE)]

    def select(self):
        self.scores = [
            self.get_score(chromosome)
            for chromosome in self.populations[-1].chromosomes
        ]

    def get_score(self, chromosome: Chromosome):
        return sum([gene.rotate + gene.power for gene in chromosome.genes])  # todo: change

    def sort(
        self, scores: List[float], population: Population
    ) -> Tuple[List[int], List[Chromosome]]:
        return unzip(
            sorted(
                zip(scores, population.chromosomes),
                key=lambda z: z[0],
                reverse=True,
            )
        )

    def reproduce_and_mutate(self, generation: int):
        scores, pool = self.sort(self.scores, self.populations[-1])
        elite_size = round(POPULATION_SIZE * ELITE_RATIO)
        new_population = [chromosome.copy() for chromosome in pool[:elite_size]]

        lower_score = scores[-1]
        total = sum([score - lower_score for score in scores]) 
        scores = [(score - lower_score) / total for score in scores] if total != 0 else [1 / len(scores)] * len(scores)

        parents = choice(pool, size=POPULATION_SIZE - elite_size, p=scores)

        for parent_1, parent_2 in pairwise(parents):
            child_1, child_2 = Chromosome.crossover(generation, parent_1, parent_2)
            if random() <= MUTATE_RATIO:
                child_1.mutate()
            if random() <= MUTATE_RATIO:
                child_2.mutate()

            new_population.append(child_1)
            new_population.append(child_2)

        self.populations.append(Population(generation, new_population))
