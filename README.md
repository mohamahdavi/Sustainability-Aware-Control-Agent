# Sustainability-Aware AI Assistant for Control Engineering

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![Control](https://img.shields.io/badge/Library-python--control%20%7C%20pymoo-1f4e79.svg)](#getting-started)
[![Report EN](https://img.shields.io/badge/Report-English%20PDF-b31b1b.svg)](Sustainability-Aware-Control-Agent/report_en/report_en.pdf)
[![Report FA](https://img.shields.io/badge/Report-Persian%20XeLaTeX-2e7d32.svg)](Sustainability-Aware-Control-Agent/report_fa/report_fa.tex)

An LLM-orchestrated, deterministic-tool assistant for control design that treats **environmental cost** as an explicit design criterion alongside closed-loop performance and robustness. Developed as a independent research project.

> [!IMPORTANT]
> **Core Architectural Rule:** The language model acts strictly as a planner, orchestrator, and interpreter. Every controller gain, pole, stability margin, and environmental metric is computed by deterministic Python tools (PID, LQR, MPC, NSGA-II, robustness, and sustainability evaluators). A deterministic **scope gate** and **number audit** constrain all model outputs to prevent numerical hallucination.

<p align="center">
  <img src="Sustainability-Aware-Control-Agent/figures/part6_summary.png" width="85%" alt="Comparative Evaluation Summary">
</p>

---

## Central Research Question

Given a dynamical plant and its closed-loop specifications (stability, overshoot, settling time, phase margin), how much does tightening those requirements cost in environmental terms—and can an automated pipeline reliably select the **greenest controller that still satisfies all specifications**?

## Key Findings

| Evaluation Area | Summary of Findings |
| :--- | :--- |
| **Robustness vs. Speed** | Enforcing peak sensitivity $M_s < 2$ is nearly cost-free across benchmarks: performance-only and robust rules select the same design in **98.3%** of cases. |
| **Environmental Trade-off** | Minimizing the relative $\text{CO}_2$ index reduces it by a median **92% / 87% / 78% / 40%** (loose $\rightarrow$ extreme specs) at the cost of increased settling time (**+293% / +366% / +184% / +45%**). *Note: These represent relative ranking indices, not physical savings.* |
| **Agent Policy vs. Baselines** | Verified-valid designs delivered: raw Ziegler–Nichols **0%**, plain NSGA-II **70.0%**, agent policy **96.7%** (with **0%** false claims for the latter two), driven by adaptive search bounds and the scope gate. |
| **Independent Verification** | `verify_design` exposed real bugs in initial metric code (**26%** of first-trial designs failed verification); post-fix, tool outputs and verifier agree on **100%** of delivered designs. |
| **Metric Provenance** | Only **10 of 24** reported quantities possess valid absolute physical units. $\text{CO}_2$, water, acoustic, embodied-carbon, mineral, and e-waste metrics are **ranking proxies** ($\text{Spearman } \rho \ge 0.967$ under 500 perturbations) and are never quoted as absolute physical quantities. |
| **Applicability Map** | Evaluated across 31 plants (5 families, 3 seeds each): **23/30** pre-registered predictions confirmed; NSGA-II finds a verified feasible design on **27/30** runnable plants vs. **1/30** for Ziegler–Nichols. |
| **Realistic-Loop Validation** | On a DC-motor case study (published parameters), **83% (29/35)** of ideal-loop-feasible designs fail once a $12\text{ V}$ actuator saturation limit and filtered derivative are introduced—including the textbook reference PID. A realistic-loop check was subsequently integrated into the agent. |
| **Open-Weight LLM Study** | Four local models (up to 14B) were benchmarked under a pre-registered selection rule (zero unsafe events and $T_1 \ge 0.85$); **none qualified**, so no local model was selected (see below). |

### Applicability Map & DC-Motor Case Study

<p align="center">
  <img src="Sustainability-Aware-Control-Agent/figures/applicability_map.png" width="48%" alt="Applicability Map">
  <img src="Sustainability-Aware-Control-Agent/figures/case_study_dc_motor.png" width="48%" alt="DC Motor Case Study">
</p>

### Open-Weight LLM Selection Study (Part 7)

Evaluated on Colab T4 + Ollama (`temperature = 0`, 14–16 Oct 2026). Pre-registered criterion: `0` unsafe events **and** $T_1 \ge 0.85$; among eligible models with $\text{Composite} \ge 0.80$, select the smallest.

| Model | Repeats | Composite Score | $T_1$ | Unsafe Events | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `qwen3:8b` | 1 | 0.73 | 0.800 | 3 | Rejected |
| `ministral-3:8b` | 1 | 0.70 | 0.880 | 2 | Rejected |
| `llama3.1:8b` | 1 | 0.42 | 0.375 | 5 | Rejected |
| `ministral-3:14b` (initial) | 1 | 0.78 | 0.890 | 1 | Rejected |
| `ministral-3:14b` (follow-up) | 3 | 0.75 | 0.830 | 7 (total) | Rejected |

> `qwen3:14b` timed out ($> 900\text{ s}$) on its initial thinking-mode response and was excluded. Models $> 14\text{B}$ were not evaluated. Full protocol and deviation logs are documented in [**Report Section 6.3**](Sustainability-Aware-Control-Agent/report_en/report_en.pdf).

---

## Scope & Limitations

- **Simulation-Only Study:** The DC-motor case study relies on published parameters (*Control Tutorials for MATLAB & Simulink*) and explicit modeling assumptions; no physical hardware experiments were conducted.
- **Proxy Environmental Metrics:** Environmental outputs are dimensionless/relative proxies suitable for design ranking, not physical life-cycle assessments (Claim 8 is explicitly *not claimed*).
- **Ideal vs. Realistic Loops:** Ideal-loop feasibility does not guarantee actuator-constrained feasibility; the agent now enforces a realistic-loop verification step.
- **LLM Benchmark Scope:** Limited to 4 open-weight models ($\le 14\text{B}$), single prompt template, regex-based task scoring, and unarchived transcripts.
- **Out-of-Scope Plants (Refused by Scope Gate):** MIMO, nonlinear, time-varying, and adaptive control systems.

All claims and their supporting empirical evidence are tabulated in [**Report Section 7.1**](Sustainability-Aware-Control-Agent/report_en/report_en.pdf).

---

## Getting Started

### 1. Run the Full Benchmark & Agent Notebook
```bash
git clone https://github.com/mohamahdavi/Sustainability-Aware-Control-Agent.git
cd Sustainability-Aware-Control-Agent/Sustainability-Aware-Control-Agent
pip install -r requirements.txt
jupyter notebook control_agent_starter.ipynb   # ~30 minutes end-to-end
```
*Tested on Python 3.13, `control` 0.10.2, and `pymoo` 0.6.2. Saved outputs from the reported run are preserved in `results/` and `figures/`.*

### 2. Re-run the LLM Evaluation Harness (Part 7)
The harness runs offline with mock backends by default. To evaluate a live model via [Ollama](https://ollama.com):
```bash
ollama pull qwen3:8b
python run_llm_eval.py qwen3:8b
```
*(Note: `run_llm_eval.py` overwrites `llm_eval_results.json` in the working directory. Environment variables: `OLLAMA_URL` [default: `http://localhost:11434/v1`], `CTRL_AGENT_LIVE_REPEATS` [default: `3`].)*

### 3. Compile Technical Reports
```bash
# English Report (16 pages)
cd report_en && pdflatex report_en.tex && pdflatex report_en.tex

# Persian Report (XeLaTeX + xepersian, requires "XB Niloofar" font)
cd report_fa && xelatex report_fa.tex && xelatex report_fa.tex
```

---

## Repository Structure

```text
.
├── README.md
└── Sustainability-Aware-Control-Agent/
    ├── control_agent_starter.ipynb   # Main notebook (Sections 1–24 covering Parts 1–10)
    ├── run_llm_eval.py               # Standalone runner for Part 7 LLM evaluation
    ├── requirements.txt              # Python dependencies
    ├── report_en/                    # English report source (report_en.tex) & compiled PDF
    ├── report_fa/                    # Persian report source (report_fa.tex)
    ├── figures/                      # High-resolution plots used in both reports
    └── results/                      # Raw numerical artifacts behind all reported tables
        ├── benchmark_results.json        # Part 5: Benchmark suite
        ├── comparative_criteria.csv      # Part 6A: Performance vs. sustainability criteria
        ├── comparative_pipelines.csv     # Part 6B: Agent policy vs. baselines
        ├── llm_eval_results.json         # Part 7: Open-weight LLM scoring runs
        ├── applicability_map.csv         # Part 8: 31-plant applicability study
        └── case_study_dc_motor.csv       # Part 9: Ideal vs. realistic DC-motor loop
```

<details>
<summary><strong>Click to expand: 10-Part Research Roadmap & Notebook Index</strong></summary>

| Part | Topic | Notebook Section |
| :---: | :--- | :---: |
| 1 | Problem statement and scope definition | `§1` |
| 2 | Agent architecture (LLM orchestrator vs. deterministic tools) | `§2` |
| 3 | Agent layer implementation (scope gate, executor, number audit) | `§17` |
| 4 | Metric provenance (physical quantities vs. ranking proxies) | `§18` |
| 5 | Benchmark suite with pre-registered predictions | `§19` |
| 6 | Comparative evaluation with an independent verifier | `§20` |
| 7 | Open-weight LLM selection study | `§21` |
| 8 | Applicability and limitations map across plant families | `§22` |
| 9 | Case study: DC-motor position servo (ideal vs. realistic loop) | `§23` |
| 10 | Final integration and claims-and-evidence matrix | `§24` |

</details>

---

## Authors & Supervision

- **Mohammadreza Mahdavi** — B.Sc. Student in Electrical Engineering (Control Systems), Sharif University of Technology
- **Sareh Karimabadi** — B.Sc. Student in Petroleum Engineering, Sharif University of Technology

**Academic Guidance:** Conducted with technical consultation from **Morteza Hajji** (Ph.D. candidate) under the supervision of **Prof. Ali Akbar Safavi** (Shiraz University).

## Key References

Full linked bibliography is provided in [`report_en.tex`](Sustainability-Aware-Control-Agent/report_en/report_en.tex). Core foundations include:
- **LLM + Tool Use:** ControlAgent (`arXiv:2410.19811`), AgenticControl (`arXiv:2506.19160`), Toolformer (`arXiv:2302.04761`), PAL (`arXiv:2211.10435`), ReAct (`arXiv:2210.03629`).
- **Control & Optimization:** `python-control` (Fuller et al., 2021), `pymoo` (Blank & Deb, 2020), NSGA-II (Deb et al., 2002), and *Control Tutorials for MATLAB & Simulink*.
