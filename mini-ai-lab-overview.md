# Mini AI Lab — Explained Simply

*Private note for explaining this project to someone new. Not part of the repo.*

## What is the objective?

We want to answer one question:

> Can a small AI "worker" learn to get better over time — like an employee
> that gets smarter at a job — when we give it a real budget of money,
> real tasks to fix, and a boss who watches the books?

Instead of asking "can a big AI do clever things?", we ask "can a small,
constrained AI *learn and adapt* — decide what to work on, do it, measure
whether it actually helped, and change its future behavior based on what it
learned?"

Think of it like a tiny startup inside a laptop. The AI is the employee.
The repo is the office, the rules, and the accountant. The experiment is
watching whether the "company" gets better at its job — fixing bugs and
writing tests — without going broke.

The main number we care about: **cost per validated success** — i.e. "how
much money (in coins) does it cost, on average, to get one genuinely good
piece of work done?" Everything else (coverage, regressions, compute used)
is a guardrail we watch so the number doesn't lie to us.

## How did we build it?

We built a **mini economy** around an AI model, with several separate pieces,
each doing one job:

1. **The worker (Model Ops)** — the AI that tries to solve a task. Right now
   it's simulated (a pretend worker with a "skill level" that improves over
   time), but it can also use a real small coding model running locally on
   the laptop (MLX / Qwen 0.5B).

2. **The checker (Evaluator)** — an independent referee that decides whether
   the worker's fix actually passed. Crucially, the worker and the checker
   are *separate*, so the worker can't grade its own homework. For real
   tasks it runs the actual tests in a throwaway copy of the code.

3. **The accountant (Ledger)** — a bank book that records every coin earned,
   spent, injected, and paused. Balances are always calculated from the
   history; nobody hand-edits numbers. If the account runs dry, spending
   stops and the "CEO" gets asked to inject more capital.

4. **The budget gate (Decide/Finance)** — before the worker attempts a task,
   the "finance department" checks: can we afford it? Is it worth it
   (expected reward vs cost)? If finance says no, the task is skipped — and
   that skip is recorded. Every skip is a moment where finance overruled
   engineering, and that tension is one of the things we study.

5. **The boss (CEO layer)** — a read-only view that stands *outside* the
   loop. It reads the accountant's books and the sprint reports and shows a
   one-screen status: how much runway we have, how the success rate is
   trending, whether the model is memorizing instead of learning. It never
   touches the worker's memory, so the worker can't cheat by looking at what
   the boss is watching.

6. **The safety guard (Thermal)** — real model runs on a laptop get hot.
   A guard refuses to run when the CPU is throttling, and training also
   requires the laptop to be plugged in. No override — a no-go gate.

7. **The rulebook (Policy)** — things like the reward schedule and the
   mission are "policy," and changing them requires an approval record (like
   a CEO sign-off) checked by the repo. This keeps the experiment honest:
   you can't quietly change the rules to make the numbers look good.

Each sprint (one work session) produces: a report, an evidence file per
attempt, resource measurements, ledger transactions, and decision records.
All of it lands in folders (`reports/`, `experiments/`, `agents/`,
`economy/`) so the trail is complete and inspectable.

## How do we monitor it — the simplest way?

Three commands, run from the repo root:

```sh
uv run pytest        # do all the automated checks still pass?
uv run lab doctor    # is the environment healthy (packages, hardware)?
uv run lab status    # one screen for the "CEO"
```

`lab status` is the whole monitoring story in one glance. It shows:

- **Balance** and **runway** — how many coins we have and roughly how many
  sprints that buys us. Broke = the lab stops on its own.
- **Latest sprint result** — success rate and whether it went up or down
  versus the previous sprint.
- **Holdout gap** — the honesty meter. If the model does well on the tasks
  it trains on but poorly on unseen ones, the gap grows, and that means the
  model is memorizing, not learning. This is the single most important
  warning light.
- **Tension** — how often finance blocked the worker from attempting a task.
- **Anything awaiting the boss** — e.g. an insolvency escalation ("we're out
  of money, please decide").

There's also `lab audit` for a full timeline of every coin event, and
`lab sentinel holdout-gap` to recompute the honesty meter. For real
monitoring, that's it: **pytest for correctness, status for the business.**