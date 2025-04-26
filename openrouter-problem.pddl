(define (problem openrouter-simple-problem)
  (:domain openrouter-simple)
  (:objects
    gpt4o llama2 safemodel - llm
    openai anthropic providerX - provider
    coding multilingual kidsafe - capability
    req-code req-multi req-kids - request
  )
  (:init
    (provided-by gpt4o openai)
    (provided-by llama2 anthropic)
    (provided-by safemodel providerX)
    (has-capability gpt4o coding)
    (has-capability llama2 multilingual)
    (has-capability safemodel kidsafe)
    (request-requires req-code coding)
    (request-requires req-multi multilingual)
    (request-requires req-kids kidsafe)
  )
  (:goal
    (and
      (routed req-code gpt4o)
      (routed req-multi llama2)
      (routed req-kids safemodel)
    )
  )
)
