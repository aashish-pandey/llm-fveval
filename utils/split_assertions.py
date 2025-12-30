import re
from pathlib import Path 

INPUT = Path("../llm_outputs/fifo_assertions.sv")
OUTDIR = Path("../llm_outputs/assertions")

OUTDIR.mkdir(exist_ok=True)

text = INPUT.read_text()

chunks = re.split(r'(?=assert\s+property)', text)

assertions = []
for chunk in chunks:
    chunk = chunk.strip()
    if chunk.startswith("assert property"):
        assertions.append(chunk)

print(f"Found {len(assertions)} assertions")

for i, a in enumerate(assertions, start=1):
    fname = OUTDIR / f"a{i:03}.sv"
    fname.write_text(a + "\n")
    print(f"Written {fname}")