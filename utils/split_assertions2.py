import re
from pathlib import Path

INPUT = Path("../llm_outputs/fifo_assertions.sv")
OUTDIR = Path("../llm_outputs/assertions")

OUTDIR.mkdir(exist_ok=True)

text = INPUT.read_text()

# Remove module wrapper if present
text = re.sub(
    r'module\s+\w+\s*;|endmodule',
    '',
    text,
    flags=re.MULTILINE
)

# Find all property blocks
properties = re.findall(
    r'property\s+\w+;.*?endproperty',
    text,
    flags=re.DOTALL
)

print(f"Found {len(properties)} properties")

for i, prop in enumerate(properties, start=1):
    fname = OUTDIR / f"a{i:03}.sv"
    fname.write_text(prop.strip() + "\n")
    print(f"Wrote {fname}")
