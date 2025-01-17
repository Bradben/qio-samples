# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

from azure.quantum import Workspace
from azure.quantum.optimization import Problem, ProblemType, Term
from azure.quantum.target.oneqbit import TabuSearch, PticmSolver, PathRelinkingSolver
import time

# Workspace information
workspace = Workspace(
    resource_id = "", # add the Resource ID of your Azure Quantum workspace
    location = ""     # add the location of your Azure Quantum workspace (e.g. "westus")
)

# Define the problem
problem = Problem(name="My First 1QBit Problem", problem_type=ProblemType.ising)

problem.add_terms([
    Term(w=-9, indices=[0]),
    Term(w=-3, indices=[1,0]),
    Term(w=5, indices=[2,0]),
    Term(w=9, indices=[2,1]),
    Term(w=2, indices=[3,0]),
    Term(w=-4, indices=[3,1]),
    Term(w=4, indices=[3,2])
])

# Create 1QBit solvers
print('instantiate solvers...')
solvers = [
    TabuSearch(workspace, improvement_cutoff=10),
    PticmSolver(workspace, num_sweeps_per_run=99),
    PathRelinkingSolver(workspace, distance_scale=0.44),
]

# Submit the problem to each solver
print('submit jobs...')
jobs = [solver.submit(problem) for solver in solvers]

# Solve the problem
for job in jobs:
    while job.details.status != 'Succeeded' and job.details.status != 'Failed':
        job.refresh()
        print(f'Job {job.id} ({job.details.target}) state is {job.details.status}')
        time.sleep(1)

print('All jobs complete!')
for job in jobs:
    results = job.get_results()
    print('{0}: {1}'.format(job.details.target, results))