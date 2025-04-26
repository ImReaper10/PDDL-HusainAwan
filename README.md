# PDDL-HusainAwan
This repository contains a PDDL‐based “routing” agent that picks the best LLM for each request, based on capability.  It uses:

- **PDDL** for domain & problem modeling  
- **Unified Planning** (Python) to parse & solve  
- OpenRouter API calls to auto-generate the `.pddl` files  

---
**PDDL Files**  
   - `openrouter-domain.pddl`  
   - `openrouter-problem.pddl`
   - These define the domain (types, predicates) and problem (objects, init, goal).

 **Python Code**  
   - `solve.py` (the feed-forward agent + solver)  
   -  `pddl_generator.py` (to dynamically generate PDDL via the OpenRouter API)
**Output**
![image](https://github.com/user-attachments/assets/8fd5baff-ae87-46c2-8c8b-7069b7edcf1d)
