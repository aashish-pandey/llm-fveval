from pathlib import Path
from google import genai

# -------------------------
# Paths
# -------------------------
ROOT = Path(__file__).resolve().parents[1]

rtl = (ROOT / "rtl" / "fifo.sv").read_text()
prompt = (ROOT / "prompt" / "base.txt").read_text()

full_prompt = f"""{prompt}

RTL:
{rtl}
"""

# -------------------------
# Gemini call (simple)
# -------------------------
client = genai.Client(api_key="AIzaSyA1Xds4CrVsVm9NIBlOcar4jobSVdl1j6Q")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=full_prompt
)

# -------------------------
# Write output
# -------------------------
out = Path("../llm_outputs/gemini_fifo_assertions.sv")
out.parent.mkdir(exist_ok=True)
out.write_text(response.text)

print(f"[OK] Assertions written to {out}")
