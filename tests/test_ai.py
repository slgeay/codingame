from random import randint
import unittest

from app.ai import AI, CHROMOSOME_SIZE, Chromosome, Gene, Population

class TestAI(unittest.TestCase):
    def assert_gene(self, gene:Gene):
        assert -90 <= gene.rotate <= 90
        assert 0 <= gene.power <= 4


    def assert_chromosome(self, chromosome:Chromosome):
        for gene in chromosome.genes:
            self.assert_gene(gene)


    def test_gene_random(self):
        gene = None
        previous_rotate = 0

        for _ in range(50):
            gene = Gene.random(gene)

            self.assert_gene(gene)
            assert -15 <= gene.rotate - previous_rotate <= 15
            assert str(gene) == f"{gene.rotate} {gene.power}"

            previous_rotate = gene.rotate


    def test_gene_copy(self):
        gene = Gene.random()
        copy = gene.copy()
        gene.power = -1

        self.assert_gene(copy)
        assert copy.power != -1

    
    def test_gene_crossover(self):
        gene_1 = Gene.random()
        gene_2 = Gene.random()

        gene_3, gene_4 = Gene.crossover(1, 0, gene_1, gene_2)
        assert str(gene_3) == str(gene_1)
        assert str(gene_4) == str(gene_2)
        self.assert_gene(gene_3)
        self.assert_gene(gene_4)

        gene_3, gene_4 = Gene.crossover(0, 1, gene_1, gene_2)
        assert str(gene_3) == str(gene_2)
        assert str(gene_4) == str(gene_1)
        self.assert_gene(gene_3)
        self.assert_gene(gene_4)

        gene_3, gene_4 = Gene.crossover(0.5, 0.5, gene_1, gene_2)
        assert gene_3.rotate == round((gene_1.rotate + gene_2.rotate) / 2)
        assert gene_3.power == round((gene_1.power + gene_2.power) / 2)
        assert gene_4.rotate == round((gene_1.rotate + gene_2.rotate) / 2)
        assert gene_4.power == round((gene_1.power + gene_2.power) / 2)
        self.assert_gene(gene_3)
        self.assert_gene(gene_4)


    def test_gene_mutate(self):
        gene = Gene.random()
        gene.mutate(None)

        self.assert_gene(gene)


    def test_chromosome_random(self):
        generation = randint(0,10)
        chromosome = Chromosome.random(generation)

        self.assert_chromosome(chromosome)
        assert chromosome.generation == generation
        assert len(set(chromosome.genes)) > 1
        assert len(set([str(gene) for gene in chromosome.genes])) > 1
        assert chromosome.run(CHROMOSOME_SIZE-1) == str(chromosome.genes[-1])


    def test_chromosome_copy(self):
        chromosome = Chromosome.random(0)
        copy = chromosome.copy()
        chromosome.genes[0].power = -1

        self.assert_chromosome(copy)
        assert copy.genes[0].power != -1

    
    def test_chromosome_crossover(self):
        chromosome_1 = Chromosome.random(0)
        chromosome_2 = Chromosome.random(0)
        chromosome_3, chromosome_4 = Chromosome.crossover(1, chromosome_1, chromosome_2)
        chromosome_1.genes[0].power = -1
        chromosome_2.genes[0].power = -1

        self.assert_chromosome(chromosome_3)
        self.assert_chromosome(chromosome_4)


    def test_chromosome_mutate(self):
        chromosome = Chromosome.random(0)
        copy = chromosome.copy()
        for _ in range(50):
            chromosome.mutate()

        self.assert_chromosome(chromosome)
        assert sum([gene.rotate + gene.power for gene in chromosome.genes]) != sum([gene.rotate + gene.power for gene in copy.genes])


    def test_population_random(self):
        population = Population.random()

        assert population.generation == 0
        assert len(set(population.chromosomes)) > 1
        assert len(set([str(chromosome) for chromosome in population.chromosomes])) > 1


    def test_population_copy(self):
        population = Population.random()
        copy = population.copy()
        population.chromosomes[0].genes[0].power = -1

        assert copy.chromosomes[0].genes[0].power != -1

    
    def test_ai_sort(self):
        population = Population.random()
        _,pool = AI().sort(reversed(range(len(population.chromosomes))), population)
        _,pool_reversed = AI().sort(range(len(population.chromosomes)), population)

        assert population.chromosomes == [chromosome for chromosome in pool]
        assert population.chromosomes == [chromosome for chromosome in reversed(pool_reversed)]
