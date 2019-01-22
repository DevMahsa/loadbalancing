import random
import linecache
import copy


class BiologicalProcessManager:
    @staticmethod
    def pmx(crossover_rate, parentOne, parentTwo):
        random_probability = random.random()

        if random_probability < crossover_rate:
            return (parentOne, parentTwo)
        else:
            # Create two crossover points
            pivotOne = random.randint(0, len(parentOne.genotype_representation)-1)
            pivotTwo = random.randint(pivotOne, len(parentOne.genotype_representation)-1)
            #print("FIRST PIVOT POINT:{} ".format(pivotOne))
            #print("SECOND PIVOT POINT: {}".format(pivotTwo))
            # Setup offspring
            child_genotype = [0 for i in range(0,len(parentOne.genotype_representation))]
            # Copy segment from P1 into child
            segmentRange = [x for x in range(pivotOne, pivotTwo+1)]
            #print("SEGMENT RANGE: {}".format(segmentRange))
            #print("FIRST INSTRUCTION")
            for i, operation in enumerate(parentOne.genotype_representation):
                if i in segmentRange:
                    #print("ADDED op:{} to index:{}".format(operation, i))
                    child_genotype[i] = operation
            # Copy segment from P2 into child
            #print("SECOND INSTRUCTION")
            for j, operation in enumerate(parentTwo.genotype_representation):
                if j in segmentRange:
                    # Check  P1
                    op = parentOne.genotype_representation[j]
                    #print("OP in P1 SIDE: {}".format(op))
                    # Check where the element exists in P2
                    index_of_op = parentTwo.genotype_representation.index(op)
                    #print("INDEX OF PREV OP IN P2: {}".format(index_of_op))
                    # Check if the operation already exists in the child
                    if operation not in child_genotype:
                        # Check if position is occupied in the child
                        if child_genotype[index_of_op] == 0:
                            #print("ADDED op:{} to index:{}".format(operation, index_of_op))
                            child_genotype[index_of_op] = operation
                            #print("CHILD NOW HAS OP: {} in index: {}".format(child_genotype[index_of_op],index_of_op ))
                        else:
                            while(True):
                                #print("INFINI LOOOOOOOP!")
                                # Check P1
                                op = parentOne.genotype_representation[index_of_op]
                                #print("[WHILE] OP in P1 SIDE: {}".format(op))
                                # Check where the element exists in P2
                                index_of_op = parentTwo.genotype_representation.index(op)
                                if child_genotype[index_of_op] == 0:
                                    #print("[WHILE] ADDED op:{} to index:{}".format(operation, index_of_op))
                                    child_genotype[index_of_op] = operation
                                    #print("[WHILE] CHILD NOW HAS OP: {} in index: {}".format(child_genotype[index_of_op],index_of_op ))
                                    break
                                else:
                                    #print("[WHILE]  INDEX OP IS CURRENTLY: {}".format(index_of_op))
                                    continue




            # Copy the rest P2 into the child
            for k, operation in enumerate(parentTwo.genotype_representation):
                if k not in segmentRange:
                    if child_genotype[k] == 0:
                        #print("ADDED op:{} to index:{}".format(operation, k))
                        child_genotype[k] = operation

            # Create offspring
            child = Chromosome(parentOne.num_of_ops_ref)
            child.genotype_representation = child_genotype
            # Generate the phenotype representation of the child
            child.generate_phenotype_representation()
            # Return the new offspring
            #print("---------------------- \n")
            #print("FINISHED! RETURNING CHILD")
            #print("---------------------- \n")
            return (child, 0)




    @staticmethod
    def mutate(child):
        randindexone = random.randint(0,len(child.genotype_representation)-1)
        randindextwo = random.randint(0,len(child.genotype_representation)-1)
        if randindexone == randindextwo:
            while(True):
                randindextwo = random.randint(0,len(child.genotype_representation)-1)
                if randindextwo != randindexone:
                    break
                else:
                    continue
        temp = child.genotype_representation[randindexone]
        child.genotype_representation[randindexone] = child.genotype_representation[randindextwo]
        child.genotype_representation[randindextwo] = temp
        child.phenotype_representation = []
        child.generate_phenotype_representation()


class JobManager:
    jobs = []

class Operation:
    start_time = 0 # Used for Schedule Building
    job_number = None
    def __init__(self, number, machine, operation_time):
        self.number = number
        self.machine = machine
        self.operation_time = operation_time

class Job:
    operations = []

    def __init__(self, number):
        self.number = number


class ScheduleBuilder:
    @staticmethod
    def find_makespan(phenotype_rep):
        phenotype = copy.deepcopy(phenotype_rep)
        current_schedule = []
        j = None
        for i, operation in enumerate(phenotype):
            ''' DEBUGGING '''
            #for op in current_schedule:
                #print("---------")
                #print("Operation:{} job:{} current_time:{} machine: {} \n".format(op.number, op.job_number, op.start_time, op.machine))

            if len(current_schedule) == 0:
                #print("First schedule object")
                #print("Operation:  #{} job#{} start_time:{}".format(operation.number, operation.job_number, operation.start_time))
                operation.start_time += operation.operation_time
                current_schedule.append(operation)
            else:
                #print('\n')
                #print("Operation -> {} | job -> {} | start_time -> {} | machine -> {}".format(operation.number, operation.job_number, operation.start_time, operation.machine))
                #print("Looking for same job...")
                #print("Current Schedule count: {} \n".format(len(current_schedule)))
                j = len(current_schedule)-1
                could_not_find_same_job = False
                could_not_find_machine = False

                while(True):
                    # Find the same job
                    # If the same job
                    if current_schedule[j].job_number == operation.job_number:
                        same_job_but_no_machine_history = False
                        everything_went_fine = False
                        #print("Found same job for {} ".format(operation.number))
                        # Look up machine history
                        #print("Looking up machine... \n")
                        k = len(current_schedule)-1
                        while(True):
                            if current_schedule[k].machine == operation.machine:
                                #print("Found same machine! for op: {} \n".format(operation.number))
                                # Do schedule operation
                                machine_history = current_schedule[k].start_time
                                #print("Current machine history: {}".format(machine_history))
                                if machine_history < current_schedule[j].start_time:
                                    #print("CURRENT SCHED START: {}".format(current_schedule[j].start_time))
                                    #print("AND MACH HIST: {}".format(machine_history))
                                    #print("Machine history was less so I'll replace")
                                    operation.start_time = current_schedule[j].start_time
                                    operation.start_time += operation.operation_time
                                    current_schedule.append(operation)
                                    everything_went_fine = True
                                    break
                                elif machine_history >= current_schedule[j].start_time:
                                    #print("CURRENT SCHED START: {}".format(current_schedule[j].start_time))
                                    #print("AND MACH HIST: {}".format(machine_history))
                                    #print("Machine history was greater so I'll continue")
                                    operation.start_time = machine_history
                                    operation.start_time += operation.operation_time
                                    current_schedule.append(operation)
                                    everything_went_fine = True
                                    break
                            elif k == 0 and current_schedule[0].machine != operation.machine:
                                same_job_but_no_machine_history = True
                                break
                            else:
                                # continue
                                #print("I am now CONT to look for a machine!")
                                k = k - 1
                                continue

                        # Same job, but no other machine history
                        if same_job_but_no_machine_history:
                            #print("Same job for op: {}, but no machine history so...ADD!".format(operation.number))
                            operation.start_time = current_schedule[j].start_time
                            operation.start_time += operation.operation_time
                            current_schedule.append(operation)
                            break
                        elif everything_went_fine:
                            break

                    # Couldn't find same job
                    elif j == 0 and current_schedule[0].job_number != operation.job_number:
                        #print("Could not find a single job comparison for op: {}".format(operation.number))
                        could_not_find_same_job = True
                        break
                    else:
                        j = j - 1

                # Look for any machine history
                if could_not_find_same_job:
                    #print("Since I couldn't find a job for op: {}, I\"ll look for a machine \n".format(operation.number))
                    l = len(current_schedule)-1
                    # Try to find machine history
                    while(True):
                        if current_schedule[l].machine == operation.machine:
                            #print("Found a similar machine for op: {}".format(operation.number))
                            operation.start_time = current_schedule[l].start_time
                            operation.start_time += operation.operation_time
                            current_schedule.append(operation)
                            break
                        elif l == 0 and current_schedule[0].machine != operation.machine:
                            #print("Could not find a single machine for op: {}".format(operation.number))
                            could_not_find_machine = True
                            break
                        else:
                            l = l - 1

                if could_not_find_machine:
                    #print("Since I couldn't find a machine, I'll just add it to the sys for op: {} \n".format(operation.number))
                    operation.start_time += operation.operation_time
                    current_schedule.append(operation)

                # Reset the flags
                could_not_find_machine = False
                could_not_find_same_job = False

        # Return the makespan
        largest_time = None
        for operation in current_schedule:
            if largest_time == None or operation.start_time > largest_time:
                largest_time = operation.start_time

        return largest_time







class Chromosome:

    fitness = None

    def __init__(self, num_of_operations):
        # Create permuation from the number of operations given
        self.genotype_representation = []
        self.num_of_ops_ref = num_of_operations
        while(len(self.genotype_representation) != num_of_operations):
            random_num = random.randint(1, num_of_operations)
            if random_num not in self.genotype_representation:
                self.genotype_representation.append(random_num)
            else:
                continue

    def generate_phenotype_representation(self):
        self.phenotype_representation = []
        for gene in self.genotype_representation:
            for job in JobManager.jobs:
                for operation in job.operations:
                    if operation.number == gene:
                        self.phenotype_representation.append(operation)


    def generate_fitness(self):
        self.fitness = ScheduleBuilder.find_makespan(self.phenotype_representation)


class Population:

    population = []

    def __init__(self, size):
        self.population_size = size

    def select_parents(self,tournament):
		'''
			Tournament selection is being used to find two parents
		'''
		first_fittest_indiv = None
		second_fittest_indiv = None

		for individual in tournament:
			# Check if this indivudal is fitter than the current fittist individual
			if first_fittest_indiv == None or individual.fitness < first_fittest_indiv.fitness:
				first_fittest_indiv = individual

		tournament.remove(first_fittest_indiv)

		for individual in tournament:
			# Check if this indivudal is fitter than the current fittist individual
			if second_fittest_indiv == None or individual.fitness < second_fittest_indiv.fitness:
				second_fittest_indiv = individual

		#print("FIRST: {},  SECOND: {}".format(first_fittest_indiv.fitness,second_fittest_indiv.fitness))
		return (first_fittest_indiv,second_fittest_indiv)

    def initialize_population(self):
        '''
                Read from a file and create the chromosomes
        '''
        # Open data file
        dataFile = open('data.txt', 'r')

        # Obtain the number of jobs and machines
        num_of_jobs = int(dataFile.read(3))
        print("NUMBER OF JOBS: {}".format(num_of_jobs))
        num_of_machines = int(dataFile.read(3))
        print("NUM OF MACH: {}".format(num_of_machines))
        num_of_operations = num_of_jobs * num_of_machines

        # Helper variables
        list_of_operations = []
        op_counter = 1

        # Loop through the operations in the file
        for i, line in enumerate(dataFile):
            # Obtain a line of operations and split them.
            # Convert each operation time into a number and turn it into an Operation object
            # Append the operations into a list
            operation_list = []
            list_of_machines = []
            list_of_times = line.split()
            for operation_time in list_of_times:
                rand_num = random.randint(1, num_of_machines)
                if rand_num not in list_of_machines:
                    list_of_machines.append(rand_num)
                    time = int(operation_time)
                    new_operation = Operation(op_counter, rand_num, time)
                    operation_list.append(new_operation)
                    op_counter += 1
                else:
                    while(True):
                        rand_num = random.randint(1, num_of_machines)
                        if rand_num not in list_of_machines:
                            list_of_machines.append(rand_num)
                            time = int(operation_time)
                            new_operation = Operation(
                                op_counter, rand_num, time)
                            operation_list.append(new_operation)
                            op_counter += 1
                            break
                        else:
                            continue
            list_of_operations.append(operation_list)

        # Loop through the operations and place them into the appropriate job
        for i, op_list in enumerate(list_of_operations):
            new_job = Job(i + 1)
            new_job.operations = op_list
            for op in op_list:
                op.job_number = new_job.number

            # Add the job to the jobManager
            JobManager.jobs.append(new_job)


        # Create the chromsomes and append them to the population
        for x in range(0, self.population_size):
            # Create a new chromosome
            new_chrom = Chromosome(num_of_operations)
            #print(new_chrom.genotype_representation)
            # Generate the phenotype representation of the chromosome
            new_chrom.generate_phenotype_representation()
            # Generate a fitness for the chromsome
            new_chrom.generate_fitness()
            # Add the chromsome to the population
            self.population.append(new_chrom)