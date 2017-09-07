import random

class GeneticAlgorithm(object):
    def __init__(self, genetics):
        self.genetics = genetics
        pass

    def run(self):
        population = self.genetics.initial()
        while True:
            fits_pops = [(self.genetics.fitness(ch),  ch) for ch in population]
            if self.genetics.check_stop(fits_pops): break
            population = self.next(fits_pops)
            pass
        return population

    def next(self, fits):
        parents_generator = self.genetics.parents(fits)
        size = len(fits)
        nexts = []
        while len(nexts) < size:
            parents = next(parents_generator)
            cross = random.random() < self.genetics.probability_crossover()
            children = self.genetics.crossover(parents) if cross else parents
            for ch in children:
                mutate = random.random() < self.genetics.probability_mutation()
                nexts.append(self.genetics.mutation(ch) if mutate else ch)
                pass
            pass
        return nexts[0:size]
    pass

class GeneticFunctions(object):
    def probability_crossover(self):
        return 1.0

    def probability_mutation(self):
        return 0.0

    def initial(self):
        return []

    def fitness(self, chromosome):
        return len(chromosome)

    def check_stop(self, fits_populations):
        return False

    def parents(self, fits_populations):
        gen = iter(sorted(fits_populations))
        while True:
            f1, ch1 = next(gen)
            f2, ch2 = next(gen)
            yield (ch1, ch2)
            pass
        return

    def crossover(self, parents):
        return parents

    def mutation(self, chromosome):
        return chromosome
    pass

if __name__ == "__main__":
    class GuessText(GeneticFunctions):
        def __init__(self, target_text,
                     limit=200, size=400,
                     prob_crossover=0.9, prob_mutation=0.2):
            self.target = self._text2chromo(target_text)
            self.counter = 0

            self.limit = limit
            self.size = size
            self.prob_crossover = prob_crossover
            self.prob_mutation = prob_mutation
            pass

        def probability_crossover(self):
            return self.prob_crossover

        def probability_mutation(self):
            return self.prob_mutation

        def initial(self):
            return [self._random_chromo() for j in range(self.size)]

        def fitness(self, chromo):
            return -sum(abs(c - t) for c, t in zip(chromo, self.target))

        def check_stop(self, fits_populations):
            self.counter += 1
            best_match = list(sorted(fits_populations))[-1][1]
            fits = [f for f, ch in fits_populations]
            best = max(fits)
            worst = min(fits)
            ave = sum(fits) / len(fits)
            print(
                "[G %3d] score=(%4d, %4d, %4d): %r" %
                (self.counter, best, ave, worst,
                 self._chromo2text(best_match)))
            return (self.counter >= self.limit or best == 0)

        def parents(self, fits_populations):
            while True:
                father = self._tournament(fits_populations)
                mother = self._tournament(fits_populations)
                yield (father, mother)
                pass
            pass

        def crossover(self, parents):
            father, mother = parents
            index1 = random.randint(1, len(self.target) - 2)
            index2 = random.randint(1, len(self.target) - 2)
            if index1 > index2: index1, index2 = index2, index1
            child1 = father[:index1] + mother[index1:index2] + father[index2:]
            child2 = mother[:index1] + father[index1:index2] + mother[index2:]
            return (child1, child2)

        def mutation(self, chromosome):
            index = random.randint(0, len(self.target) - 1)
            vary = random.randint(-5, 5)
            mutated = list(chromosome)
            mutated[index] += vary
            return mutated

        # private functions
        def _tournament(self, fits_populations):
            firstF, first = self._select_random(fits_populations)
            secondF, second = self._select_random(fits_populations)
            return first if firstF > secondF else second

        def _select_random(self, fits_populations):
            return fits_populations[random.randint(0, len(fits_populations)-1)]

        def _text2chromo(self, text):
            return [ord(ch) for ch in text]

        def _chromo2text(self, chromo):
            return "".join(chr(max(1, min(ch, 255))) for ch in chromo)

        def _random_chromo(self):
            return [random.randint(1, 255) for i in range(len(self.target))]
        pass

    GeneticAlgorithm(GuessText("Hello World!")).run()
    pass


