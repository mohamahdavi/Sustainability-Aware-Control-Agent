"""Runs ONLY what Part 7 (LLM model-selection study) needs from control_agent_starter.ipynb,
skipping the slow benchmark/sweep sections (19, 20, 22, 23, 24).

Usage (from the folder that contains control_agent_starter.ipynb):
    python run_llm_eval.py                  # uses the 3 default 8B models
    python run_llm_eval.py qwen3:8b         # or give model tags yourself
Environment variables (optional):
    OLLAMA_URL (default http://localhost:11434/v1)   CTRL_AGENT_LIVE_REPEATS (default 3)
"""
import json, os, sys, traceback, matplotlib
matplotlib.use("Agg")
os.environ["CTRL_AGENT_LIVE"] = "1"
if len(sys.argv) > 1: os.environ["CTRL_AGENT_ONLY_MODELS"] = ",".join(sys.argv[1:])
else: os.environ["CTRL_AGENT_ONLY_MODELS"] = "qwen3:8b,llama3.1:8b,ministral-3:8b"
SKIP = ("# ---- 18.", "# ---- 19.", "# ---- 20.", "# ---- 22.", "# ---- 23.", "# ---- 24.")
nb = json.load(open("control_agent_starter.ipynb", encoding="utf-8"))
ns = {"__name__": "__main__"}
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code": continue
    src = "".join(c["source"])
    if src.startswith(SKIP): continue
    src = "\n".join(l for l in src.split("\n") if not l.lstrip().startswith(("!", "%")))
    try: exec(compile(src, f"cell{i}", "exec"), ns)
    except Exception:
        print("FAILED in cell", i); traceback.print_exc(limit=4); sys.exit(1)
print("\nDONE. Send back the file llm_eval_results.json (created next to the notebook).")
