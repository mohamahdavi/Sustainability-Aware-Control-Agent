# Sustainability-Aware AI Assistant for Control Engineering

An LLM-orchestrated, deterministic-tool assistant for control design that treats **environmental cost** as a design criterion alongside closed-loop performance and robustness. A course/research project at Sharif University of Technology.

> **Design rule.** The language model is only a planner, orchestrator and interpreter. Every gain, pole, margin and environmental estimate comes from a deterministic Python tool (PID, LQR, MPC, NSGA-II, robustness and sustainability metrics). A scope gate and a number audit constrain what the model may say.

**Full write-up:** [`report_en/report_en.pdf`](report_en/report_en.pdf) (English, 16 pages) · Persian version: [`report_fa/`](report_fa/) (XeLaTeX source).

---

## Central question

Given a control system and its performance requirements (stability, overshoot, settling time, phase margin), how much does tightening those requirements cost in environmental terms, and can the design process automatically pick the *greenest controller that still meets them*?

## Key results

| Topic | Result |
|---|---|
| Robustness vs. speed | Requiring peak sensitivity `Ms < 2` is almost free on the benchmarks: the performance-only rule and the robust rule choose the same design in all but 1.7 % of cases. |
| Environmental objective | Minimising the relative CO₂ index cuts it by a median 92 % / 87 % / 78 % / 40 % (loose → extreme requirements) at the cost of settling time (+293 % / +366 % / +184 % / +45 %). These are **relative index** changes, not physical savings. |
| Agent policy vs. baselines | Verified-valid designs delivered: raw Ziegler–Nichols 0 %, plain NSGA-II 70.0 %, agent policy 96.7 % (0 % false claims for the last two). The gain comes from adaptive search bounds and the scope gate, not from anything language-model specific. |
| Independent verifier | `verify_design` caught real bugs in the project's own metric code (26 % of first-trial designs failed the check); after the fixes tool and verifier agree on 100 % of delivered designs. |
| Metric provenance | Only 10 of 24 reported quantities have a valid absolute value. CO₂, water, acoustic, embodied-carbon, mineral and e-waste numbers are proxies that can **rank** designs (Spearman ≥ 0.967 under 500 perturbations) but must not be quoted as physical quantities. |
| Applicability map | 31 plants in 5 families, 3 seeds each: 23/30 pre-registered predictions correct; NSGA-II finds a verified feasible design on 27/30 runnable plants, Ziegler–Nichols meets the spec on 1. |
| Realistic-loop case (DC motor, published parameters) | **83 % (29/35) of ideal-loop-feasible designs fail** once a 12 V actuator limit and a filtered derivative are added; even the textbook reference PID fails. The ideal-loop verdict was refuted and a realistic-loop check was added to the agent. |
| Open-weight LLM selection | Four models scored; **none met the pre-registered rule, so no model is selected** (table below). |

### LLM selection study (Part 7)

Colab T4 + Ollama, temperature 0, 14–16 Oct 2026. Rule fixed before any run: zero unsafe events **and** T1 ≥ 0.85; among eligible models with composite ≥ 0.80 choose the smallest.

| Model | Repeats | Composite | T1 | Unsafe events |
|---|---|---|---|---|
| qwen3:8b | 1 | 0.73 | 0.80 | 3 |
| ministral-3:8b | 1 | 0.70 | 0.88 | 2 |
| llama3.1:8b | 1 | 0.42 | 0.375 | 5 |
| ministral-3:14b (first run) | 1 | 0.78 | 0.89 | 1 |
| ministral-3:14b (follow-up) | 3 | 0.75 | 0.83 | 7 (summed) |

`qwen3:14b` could **not** be scored (its first thinking-mode reply did not finish within the 900 s timeout). Larger models were not run. "No model up to 14B passed" does not mean "no open-weight model can pass". Details and deviations: report Section 6.3.

## Honest status and limitations

- **No hardware.** The case study uses published parameters (Control Tutorials for MATLAB & Simulink) plus our own assumptions; nothing was measured.
- **CO₂ and related metrics are relative proxies.** Claim 8 of the report ("the greenest designs are greener in the real world") is explicitly *not claimed*.
- **Ideal-loop feasibility verdicts can fail** under realistic conditions (see above).
- **LLM study:** four models, mostly one repeat, one prompt template, regex-based scoring of two tasks, no saved transcripts.
- **Out of scope** (refused by the agent): MIMO, nonlinear, time-varying and adaptive control.

All claims and the evidence behind them are tabulated in the report (Section 7.1).

## Repository structure

```
.
├── control_agent_starter.ipynb   # main notebook, Sections 1–24 (all ten roadmap parts)
├── run_llm_eval.py               # runs only the Part 7 LLM evaluation (skips slow sections)
├── requirements.txt
├── report_en/                    # English report: report_en.tex + compiled report_en.pdf
├── report_fa/                    # Persian report (XeLaTeX, xepersian, font "XB Niloofar")
├── figures/                      # PNG figures used by both reports
└── results/                      # raw numbers behind the reported results
    ├── benchmark_results.json        # Part 5
    ├── comparative_pipelines.csv     # Part 6, experiment B
    ├── comparative_criteria.csv      # Part 6, experiment A
    ├── applicability_map.csv         # Part 8
    ├── case_study_dc_motor.csv       # Part 9
    └── llm_eval_results.json         # Part 7 (5 runs; field "repeats")
```

## Roadmap parts and where to find them

| Part | Topic | Notebook section |
|---|---|---|
| 1 | Problem statement and scope | §1 |
| 2 | Agent architecture (orchestrator vs. deterministic tools) | §2 |
| 3 | Agent layer implementation (scope gate, executor, number audit, backends) | §17 |
| 4 | Metric provenance (real vs. proxy) | §18 |
| 5 | Benchmark suite with pre-registered predictions | §19 |
| 6 | Comparative evaluation with an independent verifier | §20 |
| 7 | Open-weight LLM selection | §21 |
| 8 | Applicability and limitations map | §22 |
| 9 | Case study: DC-motor position servo | §23 |
| 10 | Final integration, claims-and-evidence table | §24 |

## Getting started

```bash
git clone <this repository>
cd <this repository>
pip install -r requirements.txt
jupyter notebook control_agent_starter.ipynb     # run all cells (about 30 minutes end to end)
```

Tested with Python 3.13, `control` 0.10.2 and `pymoo` 0.6.2. The notebook writes its CSV/JSON/PNG outputs into the working directory; the copies in `results/` and `figures/` are those of the reported run.

### Re-running the LLM evaluation (Part 7)

The harness is validated with mock backends (no model server needed). To score a real model served by [Ollama](https://ollama.com):

```bash
ollama pull <tag>                      # e.g. qwen3:8b
python run_llm_eval.py <tag>           # one model per call is safest
```

`run_llm_eval.py` overwrites `llm_eval_results.json` in the current folder, so copy it away between models. Environment variables: `OLLAMA_URL` (default `http://localhost:11434/v1`), `CTRL_AGENT_LIVE_REPEATS` (default 3).

### Building the reports

```bash
# English (any TeX distribution)
cd report_en && pdflatex report_en.tex && pdflatex report_en.tex

# Persian (XeLaTeX, font "XB Niloofar"; run twice)
cd report_fa && xelatex report_fa.tex && xelatex report_fa.tex
```

## Authors

- Mohammadreza Mahdavi — Electrical Engineering (Control), Sharif University of Technology
- Sareh Karimabadi — Petroleum Engineering, Sharif University of Technology

Developed under the guidance of the project advisor, whose feedback shaped the ten-part roadmap.

## References

The full, linked bibliography is in the report (`report_en/report_en.tex`). Main sources: ControlAgent (arXiv:2410.19811), AgenticControl (arXiv:2506.19160), Toolformer (arXiv:2302.04761), PAL (arXiv:2211.10435), ReAct (arXiv:2210.03629), NSGA-II (Deb et al., 2002), pymoo (Blank & Deb, 2020), python-control (Fuller et al., 2021), and the Control Tutorials for MATLAB & Simulink DC-motor example.
