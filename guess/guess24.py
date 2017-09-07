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
    class Guess24(GeneticFunctions):
        def __init__(self, number_list,
                     limit=200, size=400,
                     prob_crossover=0.9, prob_mutation=0.2):
            self.target = 24
            self.number_list = number_list
            self.op_list = ['+', '-', '|', '*', '/', '\\']
            self.exp_start = 4
            self.exp_end = 6
            self.generation = 0

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
            random.shuffle(self.number_list)
            return [self.number_list + self._select_op() for j in range(self.size)]

        def fitness(self, chromo):
            return self._fitness_chromo(chromo)

        def check_stop(self, fits_populations):
            self.generation += 1
            best_match = list(sorted(fits_populations))[-1][1]
            fits = [f for f, ch in fits_populations]
            best = max(fits)
            worst = min(fits)
            ave = sum(fits) / len(fits)
            print(
                "[G %3d] score=(%4d, %4d, %4d): %r" %
                (self.generation, best, ave, worst,
                 self._chromo2text(best_match)))
            return (self.generation >= self.limit or best == 0)

        def parents(self, fits_populations):
            while True:
                father = self._tournament(fits_populations)
                mother = self._tournament(fits_populations)
                yield (father, mother)
                pass
            pass

        def crossover(self, parents):
            father, mother = parents
            index1 = random.randint(self.exp_start, self.exp_end)
            index2 = random.randint(self.exp_start, self.exp_end)
            if index1 > index2: index1, index2 = index2, index1
            child1 = father[:index1] + mother[index1:index2] + father[index2:]
            child2 = mother[:index1] + father[index1:index2] + mother[index2:]
            return (child1, child2)

        def mutation(self, chromosome):
            return self._mutation_chromo(chromosome)

        # private functions
        def _select_op(self):
            return [self.op_list[random.randint(0, len(self.op_list)-1)], \
            self.op_list[random.randint(0, len(self.op_list)-1)], \
            self.op_list[random.randint(0, len(self.op_list)-1)]]


        def _tournament(self, fits_populations):
            firstF, first = self._select_random(fits_populations)
            secondF, second = self._select_random(fits_populations)
            return first if firstF > secondF else second

        def _select_random(self, fits_populations):
            return fits_populations[random.randint(0, len(fits_populations)-1)]

        def _calculate_op(self, number1, number2, op):
            if op == self.op_list[0]: return float(number1) + float(number2)
            elif op == self.op_list[1]: return float(number1) - float(number2)
            elif op == self.op_list[2]: return float(number2) - float(number1)
            elif op == self.op_list[3]: return float(number1) * float(number2)
            elif op == self.op_list[4]: return float(number1) / float(number2) if int(number2) != 0 else 0
            elif op == self.op_list[5]: return float(number2) / float(number1) if int(number1) != 0 else 0
            else: return 0

        def _calculate_chromo(self, chromo):
            text = str(chromo[0]) + chromo[4] + str(chromo[1]) + \
            chromo[5] + str(chromo[2]) + chromo[6] + str(chromo[3])
            result = self._calculate_op(chromo[0], chromo[1], chromo[4])
            result = self._calculate_op(result, chromo[2], chromo[5])
            result = self._calculate_op(result, chromo[3], chromo[6])
            return text, result

        def _chromo2text(self, chromo):
            text, result = self._calculate_chromo(chromo)
            text += ' = ' + str(result)
            return text

        def _fitness_chromo(self, chromo):
            return -abs(self._calculate_chromo(chromo)[1]-self.target)

        def _mutation_chromo(self, chromosome):
            random.shuffle(self.number_list)
            mutated = self.number_list + self._select_op()
            return mutated

        pass

    GeneticAlgorithm(Guess24([1,3,5,8])).run()
    pass


