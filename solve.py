from pddl_generator import generate_domain, generate_problem
from unified_planning.io import PDDLReader
from unified_planning.shortcuts import OneshotPlanner


def main():
   generate_domain()
   generate_problem()


   # parse & solve
   reader  = PDDLReader()
   problem = reader.parse_problem("openrouter-domain.pddl",
                                  "openrouter-problem.pddl")
   with OneshotPlanner() as planner:
       result = planner.solve(problem)
   if result.plan:
       for a in result.plan.actions:
           print(a)
   else:
       print("No plan found!")


if __name__ == "__main__":
   main()
