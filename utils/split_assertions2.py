import re
from pathlib import Path

INPUT = Path("../llm_outputs/deep_seek_fifo_assertions.sv")
OUTDIR = Path("../llm_outputs/assertions_deep_seek")
OUTDIR.mkdir(exist_ok=True)

text = INPUT.read_text()

# ------------------------------------------------
# 1) Remove markdown code fences
# ------------------------------------------------
text = re.sub(r"```systemverilog", "", text, flags=re.IGNORECASE)
text = text.replace("```", "")

# ------------------------------------------------
# 2) Remove comments (important!)
# ------------------------------------------------
text = re.sub(r"//.*", "", text)

# ------------------------------------------------
# 3) Extract inline assert property statements
# ------------------------------------------------
asserts = re.findall(
    r"assert\s+property\s*\(.*?\)\s*;",
    text,
    flags=re.DOTALL
)

print(f"Found {len(asserts)} assertions")

# ------------------------------------------------
# 4) Write each assertion to its own file
# ------------------------------------------------
for i, a in enumerate(asserts, start=1):
    fname = OUTDIR / f"a{i:03}.sv"
    fname.write_text(a.strip() + "\n")
    print(f"Wrote {fname}")
