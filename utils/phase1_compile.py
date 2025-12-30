import subprocess
import shutil
import json
from pathlib import Path

def classify_compile(output: str, returncode: int, timed_out: bool):
    
    ERROR_PATTERNS = [
        "ERROR (",
        "Summary of errors detected",
        "ignored due to previous errors",
        "cannot open include file",
        "is not declared"
    ]

    for pat in ERROR_PATTERNS:
        if pat in output:
            return "COMPILE_FAIL"

    return "COMPILE_PASS"


# -------------------------------------------------
# Paths
# -------------------------------------------------
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT  = SCRIPT_DIR.parent

ASSERT_DIR   = REPO_ROOT / "llm_outputs/assertions"
WRAPPER_TPL = REPO_ROOT / "formal/jasper/assertion_wrapper.sv"
TCL_TPL     = REPO_ROOT / "formal/jasper/compile_only.tcl"

OUT_DIR = REPO_ROOT / "llm_outputs/phase1_compile"
LOG_DIR = OUT_DIR / "logs"

OUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

results = {}

# -------------------------------------------------
# Iterate over assertions
# -------------------------------------------------
for assertion in sorted(ASSERT_DIR.glob("a*.sv")):
    name = assertion.stem
    log_file = LOG_DIR / f"{name}.log"

    print(f"[Phase1] Checking {name}")

    # ---------------------------------------------
    # Extract property name
    # ---------------------------------------------
    prop_name = None
    for line in assertion.read_text().splitlines():
        line = line.strip()
        if line.startswith("property"):
            prop_name = line.split()[1].rstrip(";")
            break

    if prop_name is None:
        log_file.write_text("ERROR: No property found\n")
        results[name] = {
            "status": "COMPILE_FAIL",
            "log": str(log_file)
        }
        continue

    # ---------------------------------------------
    # Create isolated Jasper project
    # ---------------------------------------------
    proj_dir = REPO_ROOT / f"jgproject_{name}"
    if proj_dir.exists():
        shutil.rmtree(proj_dir, ignore_errors=True)
    proj_dir.mkdir(parents=True)

    # ---------------------------------------------
    # Generate assertion wrapper
    # ---------------------------------------------
    wrapper_text = WRAPPER_TPL.read_text()
    wrapper_text = wrapper_text.replace("ASSERTION_FILE", str(assertion))
    wrapper_text = wrapper_text.replace("ASSERTION_NAME", prop_name)
    Path("assertion_wrapper.sv").write_text(wrapper_text)
    # (proj_dir / "assertion_wrapper.sv").write_text(wrapper_text)
    shutil.copy(TCL_TPL, proj_dir / "compile_only.tcl")

    # ---------------------------------------------
    # Run JasperGold (tcsh required)
    # ---------------------------------------------
    cmd = f"""
    cd "{proj_dir}"
    source /opt/eda/cadence/.cshrc.cds.setup
    jg -no_gui -allow_unsupported_OS \
       -proj "{proj_dir}" \
       -tcl compile_only.tcl
    """

    try:
        proc = subprocess.run(
            ["tcsh", "-c", cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=30
        )
        output = proc.stdout
    except subprocess.TimeoutExpired as e:
        output = (e.stdout.decode(errors="ignore")
                  if isinstance(e.stdout, bytes)
                  else (e.stdout or ""))
        output += "\n[TIMEOUT]\n"
        log_file.write_text(output)

        subprocess.run(
            ["pkill", "-f", "jg_"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        results[name] = {
            "status": "TIMEOUT",
            "log": str(log_file)
        }
        continue

    # ---------------------------------------------
    # Cleanup leaked Jasper processes
    # ---------------------------------------------
    subprocess.run(
        ["pkill", "-f", "jg_"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    log_file.write_text(output)

    # ---------------------------------------------
    # Classification
    # ---------------------------------------------
    status = classify_compile(
        output=output,
        returncode=proc.returncode,
        timed_out=False
    )
    print(status)
    if status == "COMPILE_PASS":
        dest = OUT_DIR / "pass"
    elif status == "COMPILE_FAIL":
        dest = OUT_DIR / "fail"
    else:
        dest = OUT_DIR / "timeout"

    dest.mkdir(exist_ok=True)

# -------------------------------------------------
# Save results
# -------------------------------------------------
with open(OUT_DIR / "compile_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Phase-1 compile classification complete")
