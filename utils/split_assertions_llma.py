import re
from pathlib import Path

INPUT = Path("../llm_outputs/llama_fifo_assertions.sv")
OUTDIR = Path("../llm_outputs/assertions_llama")
OUTDIR.mkdir(exist_ok=True)

text = INPUT.read_text()

# ------------------------------------------------
# 1) Remove markdown fences
# ------------------------------------------------
text = re.sub(r"```systemverilog", "", text, flags=re.IGNORECASE)
text = text.replace("```", "")

# ------------------------------------------------
# 2) Remove comments
# ------------------------------------------------
text = re.sub(r"//.*", "", text)

# ------------------------------------------------
# 3) Remove module wrapper ONLY (keep body)
# ------------------------------------------------
text = re.sub(r"\bmodule\b.*?;", "", text, flags=re.DOTALL)
text = re.sub(r"\bendmodule\b", "", text)

# ------------------------------------------------
# 4) Extract explicit assert property (...)
# ------------------------------------------------
explicit = re.findall(
    r"assert\s+property\s*\(.*?\)\s*;",
    text,
    flags=re.DOTALL
)

# ------------------------------------------------
# 5) Extract implicit clocked assertions
#    Pattern: @(...) disable iff (...) <expr>;
# ------------------------------------------------
implicit = re.findall(
    r"@\s*\(.*?\)\s*disable\s+iff\s*\(.*?\)\s*.*?;",
    text,
    flags=re.DOTALL
)

print(
    f"Found {len(explicit) + len(implicit)} assertions "
    f"({len(explicit)} explicit, {len(implicit)} implicit)"
)

# ------------------------------------------------
# 6) Normalize implicit assertions
# ------------------------------------------------
all_asserts = []

# Keep explicit ones as-is
for a in explicit:
    all_asserts.append(a.strip())

# Wrap implicit ones
for a in implicit:
    wrapped = f"assert property (\n{a.strip()}\n);"
    all_asserts.append(wrapped)

# ------------------------------------------------
# 7) Write each assertion to its own file
# ------------------------------------------------
for i, a in enumerate(all_asserts, start=1):
    fname = OUTDIR / f"a{i:03}.sv"
    fname.write_text(a + "\n")
    print(f"Wrote {fname}")
