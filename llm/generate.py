import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = "qwen2.5-coder:7b"

rtl = Path(ROOT/"rtl"/"fifo.sv").read_text()
prompt = Path(ROOT/"prompt"/"base.txt").read_text()

full_prompt = f"""{prompt}

RTL:
{rtl}
"""

result = subprocess.run(
    ["ollama", "run", MODEL],
    input=full_prompt,
    text=True,
    capture_output=True
)

out = Path("llm_outputs/fifo_assertions.sv")
out.parent.mkdir(exist_ok=True)
out.write_text(result.stdout)

print(f"[OK] Assertions written to {out}")