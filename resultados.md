(trabajo-grupal) [gabriel@GFSM trabajo_grupal]$ uv run python test_litellm.py

Semantic Cache Research — LiteLLM + Ollama + Redis

Resetting Redis semantic cache ...

  Cache reset done.

Warming up models ...

  warmup: Count from one to five.  (854 ms)

  warmup: What color is the sky?  (840 ms)

  warmup: Is water wet?  (845 ms)

  warmup: Tell me a joke.  (861 ms)

─────────────────────────────────────────────────────────────────────────────────────────────── Exact duplicates ────────────────────────────────────────────────────────────────────────────────────────────────

10 topics × 2 identical prompts — second MUST always be HIT.

  [1/20] What is the boiling point of water?...  MISS     5979 ms
  [2/20] What is the boiling point of water?...  HIT       32 ms
  [3/20] What is the atomic number of carbon?...  MISS     5889 ms
  [4/20] What is the atomic number of carbon?...  HIT       30 ms
  [5/20] What is the square root of 144?...  MISS     5896 ms
  [6/20] What is the square root of 144?...  HIT       31 ms
  [7/20] What is the freezing point of water?...  MISS     5953 ms
  [8/20] What is the freezing point of water?...  HIT       30 ms
  [9/20] What is the pH of pure water?...  MISS     6035 ms
  [10/20] What is the pH of pure water?...  HIT       30 ms
  [11/20] What is the density of water?...  MISS     5930 ms
  [12/20] What is the density of water?...  HIT       30 ms
  [13/20] What is the speed of sound?...  MISS     6015 ms
  [14/20] What is the speed of sound?...  HIT       29 ms
  [15/20] What is the chemical symbol for gold?...  MISS     5926 ms
  [16/20] What is the chemical symbol for gold?...  HIT       31 ms
  [17/20] What is the value of pi to 3 decimal places?...  MISS     5960 ms
  [18/20] What is the value of pi to 3 decimal places?...  HIT       35 ms
  [19/20] What is the chemical formula of methane?...  MISS     5962 ms
  [20/20] What is the chemical formula of methane?...  HIT       31 ms

──────────────────────────────────────────────────────────────────────────────────────────── Paraphrase — Geography ─────────────────────────────────────────────────────────────────────────────────────────────

5 geography topics × 3 phrasings — prompt 2+ should HIT.

  [1/15] What is the capital of France?...  MISS     5903 ms
  [2/15] What is the capital city of France?...  HIT       30 ms
  [3/15] Which city serves as the capital of France?...  HIT       31 ms
  [4/15] What is the longest river in the world?...  MISS     5894 ms
  [5/15] Which river is the longest in the world?...  HIT       31 ms
  [6/15] What is the world's longest river?...  HIT       30 ms
  [7/15] How many continents are there on Earth?...  MISS     5882 ms
  [8/15] What is the number of continents on Earth?...  HIT       32 ms
  [9/15] How many continents exist on Earth?...  HIT       31 ms
  [10/15] What is the largest ocean on Earth?...  MISS     6041 ms
  [11/15] Which ocean is the largest on Earth?...  HIT       31 ms
  [12/15] What is the biggest ocean in the world?...  HIT       32 ms
  [13/15] What is the tallest mountain in the world?...  MISS     6029 ms
  [14/15] Which mountain is the highest on Earth?...  HIT       30 ms
  [15/15] What is the highest peak in the world?...  HIT       32 ms

───────────────────────────────────────────────────────────────────────────────────────────── Paraphrase — Science ──────────────────────────────────────────────────────────────────────────────────────────────

5 science topics × 3 phrasings — prompt 2+ should HIT.

  [1/15] How does photosynthesis work?...  MISS     5820 ms
  [2/15] Explain the process of photosynthesis...  MISS     5898 ms
  [3/15] What happens during photosynthesis?...  MISS     5863 ms
  [4/15] How many planets are in our solar system?...  MISS     5957 ms
  [5/15] What is the number of planets orbiting the sun?...  MISS     5875 ms
  [6/15] How many planets orbit our sun?...  HIT       30 ms
  [7/15] What is gravity?...  MISS     5851 ms
  [8/15] How does gravity work?...  MISS     5869 ms
  [9/15] What force pulls objects toward Earth?...  MISS     5898 ms
  [10/15] What gas do plants absorb from the atmosphere?...  MISS     6030 ms
  [11/15] Which gas do plants take in from the air?...  HIT       32 ms
  [12/15] What gas is absorbed by plants during photosynthesis?...  HIT       31 ms
  [13/15] How does sound travel?...  MISS     5990 ms
  [14/15] How does sound propagate through air?...  MISS     5881 ms
  [15/15] What is the mechanism by which sound travels?...  HIT       32 ms

────────────────────────────────────────────────────────────────────────────────────────── Paraphrase — History & Arts ──────────────────────────────────────────────────────────────────────────────────────────

5 history/arts topics × 3 phrasings — prompt 2+ should HIT.

  [1/15] Who painted the Mona Lisa?...  MISS     5997 ms
  [2/15] Who was the artist of the Mona Lisa?...  MISS     6044 ms
  [3/15] Who created the Mona Lisa painting?...  HIT       31 ms
  [4/15] When did World War II end?...  MISS     5983 ms
  [5/15] What year did World War II end?...  HIT       30 ms
  [6/15] When was the end of World War II?...  HIT       30 ms
  [7/15] Who wrote Romeo and Juliet?...  MISS     5858 ms
  [8/15] Who was the author of Romeo and Juliet?...  HIT       31 ms
  [9/15] Who penned Romeo and Juliet?...  HIT       29 ms
  [10/15] What is the Great Wall of China?...  HIT       31 ms
  [11/15] Describe the Great Wall of China...  MISS     5889 ms
  [12/15] What is the Great Wall of China made of?...  MISS     5958 ms
  [13/15] Who discovered penicillin?...  MISS     5923 ms
  [14/15] Who discovered the antibiotic penicillin?...  HIT       32 ms
  [15/15] Who is credited with discovering penicillin?...  HIT       32 ms

───────────────────────────────────────────────────────────────────────────────────────────── Related but distinct ──────────────────────────────────────────────────────────────────────────────────────────────

Same domain, different facts — should MISS at 0.85.

  [1/9] What is a list in Python?...  MISS     5822 ms
  [2/9] How do you sort a list in Python?...  MISS     5967 ms
  [3/9] What is a dictionary in Python?...  MISS     5988 ms
  [4/9] What temperature should you bake bread at?...  MISS     5930 ms
  [5/9] How long does it take to bake bread?...  MISS     5992 ms
  [6/9] What ingredients are in bread dough?...  MISS     5926 ms
  [7/9] How long is a football match?...  MISS     5892 ms
  [8/9] How many players are on a football team?...  MISS     5919 ms
  [9/9] What is offside in football?...  MISS     5905 ms

──────────────────────────────────────────────────────────────────────────────────────────── Unrelated (cross-check) ────────────────────────────────────────────────────────────────────────────────────────────

Completely different topics — must never hit cache.

  [1/5] What is the speed of light?...  MISS     5784 ms
  [2/5] Who invented the telephone?...  MISS     5762 ms
  [3/5] Explain how a lever works....  MISS     6045 ms
  [4/5] What is the boiling point of ethanol?...  HIT       31 ms
  [5/5] How do vaccines work?...  MISS     5978 ms

───────────────────────────────────────────────────────────────────────────────────────────── Load balancing probe ──────────────────────────────────────────────────────────────────────────────────────────────

10 identical requests with cache OFF — shows request distribution.

  [1/10] Say hello in one word....  MISS     5875 ms
  [2/10] Say hello in one word....  MISS     5903 ms
  [3/10] Say hello in one word....  MISS     6057 ms
  [4/10] Say hello in one word....  MISS     6111 ms
  [5/10] Say hello in one word....  MISS     5865 ms
  [6/10] Say hello in one word....  MISS     5832 ms
  [7/10] Say hello in one word....  MISS     5957 ms
  [8/10] Say hello in one word....  MISS     5831 ms
  [9/10] Say hello in one word....  MISS     5951 ms
  [10/10] Say hello in one word....  MISS     5834 ms

────────────────────────────────────────────────────────────────────────────────────────────── Per-request results ──────────────────────────────────────────────────────────────────────────────────────────────

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┓

┃ Group                      ┃ Prompt                               ┃ Cache  ┃ Deploy     ┃    Latency ┃

┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━┩

│ Exact duplicates           │ What is the boiling point of         │   M    │ ollama-1   │       5979 │

│                            │ water...                             │        │            │            │

│ Exact duplicates           │ What is the boiling point of         │   H    │ ollama-1   │         32 │

│                            │ water...                             │        │            │            │

│ Exact duplicates           │ What is the atomic number of         │   M    │ ollama-2   │       5889 │

│                            │ carbo...                             │        │            │            │

│ Exact duplicates           │ What is the atomic number of         │   H    │ ollama-1   │         30 │

│                            │ carbo...                             │        │            │            │

│ Exact duplicates           │ What is the square root of 144?      │   M    │ ollama-1   │       5896 │

│ Exact duplicates           │ What is the square root of 144?      │   H    │ ollama-1   │         31 │

│ Exact duplicates           │ What is the freezing point of        │   M    │ ollama-1   │       5953 │

│                            │ wate...                              │        │            │            │

│ Exact duplicates           │ What is the freezing point of        │   H    │ ollama-2   │         30 │

│                            │ wate...                              │        │            │            │

│ Exact duplicates           │ What is the pH of pure water?        │   M    │ ollama-1   │       6035 │

│ Exact duplicates           │ What is the pH of pure water?        │   H    │ ollama-1   │         30 │

│ Exact duplicates           │ What is the density of water?        │   M    │ ollama-2   │       5930 │

│ Exact duplicates           │ What is the density of water?        │   H    │ ollama-2   │         30 │

│ Exact duplicates           │ What is the speed of sound?          │   M    │ ollama-1   │       6015 │

│ Exact duplicates           │ What is the speed of sound?          │   H    │ ollama-2   │         29 │

│ Exact duplicates           │ What is the chemical symbol for      │   M    │ ollama-2   │       5926 │

│                            │ go...                                │        │            │            │

│ Exact duplicates           │ What is the chemical symbol for      │   H    │ ollama-1   │         31 │

│                            │ go...                                │        │            │            │

│ Exact duplicates           │ What is the value of pi to 3         │   M    │ ollama-1   │       5960 │

│                            │ decim...                             │        │            │            │

│ Exact duplicates           │ What is the value of pi to 3         │   H    │ ollama-1   │         35 │

│                            │ decim...                             │        │            │            │

│ Exact duplicates           │ What is the chemical formula of      │   M    │ ollama-1   │       5962 │

│                            │ me...                                │        │            │            │

│ Exact duplicates           │ What is the chemical formula of      │   H    │ ollama-2   │         31 │

│                            │ me...                                │        │            │            │

│ Paraphrase — Geography     │ What is the capital of France?       │   M    │ ollama-2   │       5903 │

│ Paraphrase — Geography     │ What is the capital city of          │   H    │ ollama-1   │         30 │

│                            │ France...                            │        │            │            │

│ Paraphrase — Geography     │ Which city serves as the capital     │   H    │ ollama-1   │         31 │

│                            │ o...                                 │        │            │            │

│ Paraphrase — Geography     │ What is the longest river in the     │   M    │ ollama-1   │       5894 │

│                            │ w...                                 │        │            │            │

│ Paraphrase — Geography     │ Which river is the longest in the    │   H    │ ollama-1   │         31 │

│                            │ ...                                  │        │            │            │

│ Paraphrase — Geography     │ What is the world's longest river?   │   H    │ ollama-1   │         30 │

│ Paraphrase — Geography     │ How many continents are there on     │   M    │ ollama-2   │       5882 │

│                            │ E...                                 │        │            │            │

│ Paraphrase — Geography     │ What is the number of continents     │   H    │ ollama-2   │         32 │

│                            │ o...                                 │        │            │            │

│ Paraphrase — Geography     │ How many continents exist on         │   H    │ ollama-2   │         31 │

│                            │ Earth...                             │        │            │            │

│ Paraphrase — Geography     │ What is the largest ocean on         │   M    │ ollama-1   │       6041 │

│                            │ Earth...                             │        │            │            │

│ Paraphrase — Geography     │ Which ocean is the largest on        │   H    │ ollama-1   │         31 │

│                            │ Eart...                              │        │            │            │

│ Paraphrase — Geography     │ What is the biggest ocean in the     │   H    │ ollama-2   │         32 │

│                            │ w...                                 │        │            │            │

│ Paraphrase — Geography     │ What is the tallest mountain in      │   M    │ ollama-1   │       6029 │

│                            │ th...                                │        │            │            │

│ Paraphrase — Geography     │ Which mountain is the highest on     │   H    │ ollama-2   │         30 │

│                            │ E...                                 │        │            │            │

│ Paraphrase — Geography     │ What is the highest peak in the      │   H    │ ollama-2   │         32 │

│                            │ wo...                                │        │            │            │

│ Paraphrase — Science       │ How does photosynthesis work?        │   M    │ ollama-2   │       5820 │

│ Paraphrase — Science       │ Explain the process of               │   M    │ ollama-2   │       5898 │

│                            │ photosynthe...                       │        │            │            │

│ Paraphrase — Science       │ What happens during                  │   M    │ ollama-2   │       5863 │

│                            │ photosynthesis...                    │        │            │            │

│ Paraphrase — Science       │ How many planets are in our solar    │   M    │ ollama-1   │       5957 │

│                            │ ...                                  │        │            │            │

│ Paraphrase — Science       │ What is the number of planets        │   M    │ ollama-2   │       5875 │

│                            │ orbi...                              │        │            │            │

│ Paraphrase — Science       │ How many planets orbit our sun?      │   H    │ ollama-1   │         30 │

│ Paraphrase — Science       │ What is gravity?                     │   M    │ ollama-2   │       5851 │

│ Paraphrase — Science       │ How does gravity work?               │   M    │ ollama-2   │       5869 │

│ Paraphrase — Science       │ What force pulls objects toward      │   M    │ ollama-2   │       5898 │

│                            │ Ea...                                │        │            │            │

│ Paraphrase — Science       │ What gas do plants absorb from       │   M    │ ollama-1   │       6030 │

│                            │ the...                               │        │            │            │

│ Paraphrase — Science       │ Which gas do plants take in from     │   H    │ ollama-2   │         32 │

│                            │ t...                                 │        │            │            │

│ Paraphrase — Science       │ What gas is absorbed by plants       │   H    │ ollama-1   │         31 │

│                            │ dur...                               │        │            │            │

│ Paraphrase — Science       │ How does sound travel?               │   M    │ ollama-1   │       5990 │

│ Paraphrase — Science       │ How does sound propagate through     │   M    │ ollama-2   │       5881 │

│                            │ a...                                 │        │            │            │

│ Paraphrase — Science       │ What is the mechanism by which       │   H    │ ollama-2   │         32 │

│                            │ sou...                               │        │            │            │

│ Paraphrase — History & Ar  │ Who painted the Mona Lisa?           │   M    │ ollama-1   │       5997 │

│ Paraphrase — History & Ar  │ Who was the artist of the Mona       │   M    │ ollama-1   │       6044 │

│                            │ Lis...                               │        │            │            │

│ Paraphrase — History & Ar  │ Who created the Mona Lisa            │   H    │ ollama-2   │         31 │

│                            │ painting...                          │        │            │            │

│ Paraphrase — History & Ar  │ When did World War II end?           │   M    │ ollama-1   │       5983 │

│ Paraphrase — History & Ar  │ What year did World War II end?      │   H    │ ollama-2   │         30 │

│ Paraphrase — History & Ar  │ When was the end of World War II?    │   H    │ ollama-1   │         30 │

│ Paraphrase — History & Ar  │ Who wrote Romeo and Juliet?          │   M    │ ollama-2   │       5858 │

│ Paraphrase — History & Ar  │ Who was the author of Romeo and      │   H    │ ollama-1   │         31 │

│                            │ Ju...                                │        │            │            │

│ Paraphrase — History & Ar  │ Who penned Romeo and Juliet?         │   H    │ ollama-2   │         29 │

│ Paraphrase — History & Ar  │ What is the Great Wall of China?     │   H    │ ollama-1   │         31 │

│ Paraphrase — History & Ar  │ Describe the Great Wall of China     │   M    │ ollama-2   │       5889 │

│ Paraphrase — History & Ar  │ What is the Great Wall of China      │   M    │ ollama-2   │       5958 │

│                            │ ma...                                │        │            │            │

│ Paraphrase — History & Ar  │ Who discovered penicillin?           │   M    │ ollama-1   │       5923 │

│ Paraphrase — History & Ar  │ Who discovered the antibiotic        │   H    │ ollama-2   │         32 │

│                            │ peni...                              │        │            │            │

│ Paraphrase — History & Ar  │ Who is credited with discovering     │   H    │ ollama-1   │         32 │

│                            │ p...                                 │        │            │            │

│ Related but distinct       │ What is a list in Python?            │   M    │ ollama-2   │       5822 │

│ Related but distinct       │ How do you sort a list in Python?    │   M    │ ollama-1   │       5967 │

│ Related but distinct       │ What is a dictionary in Python?      │   M    │ ollama-1   │       5988 │

│ Related but distinct       │ What temperature should you bake     │   M    │ ollama-1   │       5930 │

│                            │ b...                                 │        │            │            │

│ Related but distinct       │ How long does it take to bake        │   M    │ ollama-1   │       5992 │

│                            │ brea...                              │        │            │            │

│ Related but distinct       │ What ingredients are in bread        │   M    │ ollama-2   │       5926 │

│                            │ doug...                              │        │            │            │

│ Related but distinct       │ How long is a football match?        │   M    │ ollama-2   │       5892 │

│ Related but distinct       │ How many players are on a            │   M    │ ollama-2   │       5919 │

│                            │ football...                          │        │            │            │

│ Related but distinct       │ What is offside in football?         │   M    │ ollama-2   │       5905 │

│ Unrelated (cross-check)    │ What is the speed of light?          │   M    │ ollama-2   │       5784 │

│ Unrelated (cross-check)    │ Who invented the telephone?          │   M    │ ollama-1   │       5762 │

│ Unrelated (cross-check)    │ Explain how a lever works.           │   M    │ ollama-1   │       6045 │

│ Unrelated (cross-check)    │ What is the boiling point of         │   H    │ ollama-2   │         31 │

│                            │ ethan...                             │        │            │            │

│ Unrelated (cross-check)    │ How do vaccines work?                │   M    │ ollama-2   │       5978 │

│ Load balancing probe       │ Say hello in one word.               │   M    │ ollama-2   │       5875 │

│ Load balancing probe       │ Say hello in one word.               │   M    │ ollama-1   │       5903 │

│ Load balancing probe       │ Say hello in one word.               │   M    │ ollama-1   │       6057 │

│ Load balancing probe       │ Say hello in one word.               │   M    │ ollama-1   │       6111 │

│ Load balancing probe       │ Say hello in one word.               │   M    │ ollama-2   │       5865 │

│ Load balancing probe       │ Say hello in one word.               │   M    │ ollama-2   │       5832 │

│ Load balancing probe       │ Say hello in one word.               │   M    │ ollama-1   │       5957 │

│ Load balancing probe       │ Say hello in one word.               │   M    │ ollama-2   │       5831 │

│ Load balancing probe       │ Say hello in one word.               │   M    │ ollama-1   │       5951 │

│ Load balancing probe       │ Say hello in one word.               │   M    │ ollama-2   │       5834 │

└────────────────────────────┴──────────────────────────────────────┴────────┴────────────┴────────────┘

Cache HIT   avg=31 ms  median=31 ms  n=33

Cache MISS  avg=5929 ms  median=5925 ms  n=56

Cache speedup: 191.5×

────────────────────────────────────────────────────────────────────────────────────────── Load balancing distribution ──────────────────────────────────────────────────────────────────────────────────────────

  ollama-1       45 req  ██████████░░░░░░░░░░ 51%

  ollama-2       44 req  █████████░░░░░░░░░░░ 49%

  TOTAL          89 req
