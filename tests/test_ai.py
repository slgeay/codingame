from random import randint

from app.ai import LanderSimulation, LanderChromosome, LanderGene, LanderGeneticAlgorithm, LanderPopulation, Chromosome, Gene

def assert_gene(gene:Gene):
    assert -90 <= gene.rotate <= 90
    assert 0 <= gene.power <= 4


def assert_chromosome(chromosome:Chromosome):
    for gene in chromosome.genes:
        assert_gene(gene)


def test_gene_random():
    gene = None
    previous_rotate = 0

    for _ in range(50):
        gene = LanderGene.random(gene)

        assert_gene(gene)
        assert -15 <= gene.rotate - previous_rotate <= 15
        assert str(gene) == f"{gene.rotate} {gene.power}"

        previous_rotate = gene.rotate


def test_gene_copy():
    gene = LanderGene.random()
    copy = gene.copy()
    gene.power = -1

    assert_gene(copy)
    assert copy.power != -1


def test_gene_crossover():
    gene_1 = LanderGene.random()
    gene_2 = LanderGene.random()

    gene_3, gene_4 = gene_1.crossover(1, 0, gene_2)
    assert str(gene_3) == str(gene_1)
    assert str(gene_4) == str(gene_2)
    assert_gene(gene_3)
    assert_gene(gene_4)

    gene_3, gene_4 = gene_1.crossover(0, 1, gene_2)
    assert str(gene_3) == str(gene_2)
    assert str(gene_4) == str(gene_1)
    assert_gene(gene_3)
    assert_gene(gene_4)

    gene_3, gene_4 = gene_1.crossover(0.5, 0.5, gene_2)
    assert gene_3.rotate == round((gene_1.rotate + gene_2.rotate) / 2)
    assert gene_3.power == round((gene_1.power + gene_2.power) / 2)
    assert gene_4.rotate == round((gene_1.rotate + gene_2.rotate) / 2)
    assert gene_4.power == round((gene_1.power + gene_2.power) / 2)
    assert_gene(gene_3)
    assert_gene(gene_4)


def test_gene_mutate():
    gene = LanderGene.random()
    gene.mutate(None)

    assert_gene(gene)


def test_chromosome_random():
    generation = randint(0,10)
    chromosome = LanderChromosome.random(generation, 10)

    assert_chromosome(chromosome)
    assert chromosome.generation == generation
    assert len(set(chromosome.genes)) > 1
    assert len(set([str(gene) for gene in chromosome.genes])) > 1
    assert chromosome.run(9) == str(chromosome.genes[-1])


def test_chromosome_copy():
    chromosome = LanderChromosome.random(0, 10)
    copy = chromosome.copy()
    chromosome.genes[0].power = -1

    assert_chromosome(copy)
    assert copy.genes[0].power != -1


def test_chromosome_crossover():
    chromosome_1 = LanderChromosome.random(0, 10)
    chromosome_2 = LanderChromosome.random(0, 10)
    chromosome_3, chromosome_4 = chromosome_1.crossover(1, chromosome_2)
    chromosome_1.genes[0].power = -1
    chromosome_2.genes[0].power = -1

    assert_chromosome(chromosome_3)
    assert_chromosome(chromosome_4)


def test_chromosome_mutate():
    chromosome = LanderChromosome.random(0, 10)
    copy = chromosome.copy()
    for _ in range(50):
        chromosome.mutate()

    assert_chromosome(chromosome)
    assert sum([gene.rotate + gene.power for gene in chromosome.genes]) != sum([gene.rotate + gene.power for gene in copy.genes])


def test_population_random():
    population = LanderPopulation.random(10, 10)

    assert population.generation == 0
    assert len(set(population.chromosomes)) > 1
    assert len(set([str(chromosome) for chromosome in population.chromosomes])) > 1


def test_population_copy():
    population = LanderPopulation.random(10, 10)
    copy = population.copy()
    population.chromosomes[0].genes[0].power = -1

    assert copy.chromosomes[0].genes[0].power != -1


def test_genetic_algorithm_sort():
    population = LanderPopulation.random(10, 10)
    _,pool = LanderGeneticAlgorithm().sort(reversed(range(len(population.chromosomes))), population)
    _,pool_reversed = LanderGeneticAlgorithm().sort(range(len(population.chromosomes)), population)

    assert population.chromosomes == [chromosome for chromosome in pool]
    assert population.chromosomes == [chromosome for chromosome in reversed(pool_reversed)]


def test_simulation_land():
    land = LanderSimulation.random_land()
    
    assert 2 <= len(land) < 30
    flat = 0
    for i, point in enumerate(land):
        assert 0 <= point[0] < 7000
        assert 0 <= point[1] < 3000
        if i > 0:
            assert land[i-1][0] < point[0]
            if land[i-1][1] == land[i][1]:
                flat += 1

    assert flat == 1, land

        

