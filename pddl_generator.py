import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
   raise RuntimeError("Set OPENROUTER_API_KEY in your .env")


client = OpenAI(
   base_url="https://openrouter.ai/api/v1",
   api_key=API_KEY
)


def _extract_pddl(raw: str) -> str:
   """
   Strip markdown fences and any text before/after the (define ...) block.
   """
   text = raw.strip()
   if text.startswith("```"):
       # remove ```...``` fences
       text = text.strip("```").strip()
   start = text.find("(define")
   end   = text.rfind(")")
   return text[start:end+1]


def generate_domain(output_path: str = "openrouter-domain.pddl"):
   """
   Ask the LLM to emit a STRIPS-only OpenRouter domain
   """
   prompt = """
Design a PDDL domain for "openrouter-simple" with only STRIPS features:
- Requirements: :typing
- Types: llm, provider, capability, request
- Predicates:
 - (has-capability ?m - llm ?c - capability)
 - (provided-by    ?m - llm ?p - provider)
 - (request-requires ?r - request ?c - capability)
 - (routed         ?r - request ?m - llm)
- Exactly one action "route-request" with parameters (?r - request, ?m - llm, ?c - capability),
 whose preconditions enforce (request-requires ?r ?c) and (has-capability ?m ?c),
 and whose effect adds (routed ?r ?m).
"""
   res = client.chat.completions.create(
       model="openai/gpt-4o-mini",
       messages=[
           {"role":"system", "content":"You are an expert PDDL generator. Output only raw PDDL."},
           {"role":"user",   "content":prompt.strip()}
       ]
   )
   domain_pddl = _extract_pddl(res.choices[0].message.content)
   with open(output_path, "w") as f:
       f.write(domain_pddl + "\n")
   print(f"Wrote generated domain to {output_path}")


def generate_problem(output_path: str = "openrouter-problem.pddl"):
   """
   Ask the LLM to emit a STRIPS-only OpenRouter problem
   """
   prompt = """
Using the domain "openrouter-simple" defined above, generate a PDDL problem
named "openrouter-simple-problem" that includes:
- Objects:
   gpt4o llama2 safemodel      - llm
   openai anthropic providerX  - provider
   coding multilingual kidsafe - capability
   req-code req-multi req-kids - request
- Init facts for:
   (provided-by ...)
   (has-capability ...)
   (request-requires ...)
- A goal that routes each request to its matching capability:


 (and
   (routed req-code  gpt4o)
   (routed req-multi llama2)
   (routed req-kids  safemodel)
 )
"""
   res = client.chat.completions.create(
       model="openai/gpt-4o-mini",
       messages=[
           {"role":"system","content":"You are an expert PDDL problem generator. Output only raw PDDL."},
           {"role":"user",  "content":prompt.strip()}
       ]
   )
   problem_pddl = _extract_pddl(res.choices[0].message.content)
   with open(output_path, "w") as f:
       f.write(problem_pddl + "\n")
   print(f"Wrote generated problem to {output_path}")
