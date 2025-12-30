import subprocess 
import shutil
import json
from pathlib import Path 
import time

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent  

WRAPPER_PATH = REPO_ROOT / "formal/jasper/assertion_wrapper.sv"
ASSERT_DIR = REPO_ROOT / "llm_outputs/assertions"

OUT_DIR = Path('../llm_outputs/phase1_compile')
LOG_DIR = OUT_DIR / "logs"

OUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

results = {}

for assertion in sorted(ASSERT_DIR.glob("a*.sv")):
    name = assertion.stem 
    log_file = LOG_DIR / f"{name}.log"

    # Extract property name from the assertion file
    prop_text = assertion.read_text()
    prop_name = None

    for line in prop_text.splitlines():
        line = line.strip()
        if line.startswith("property"):
            prop_name = line.split()[1].rstrip(";")
            break

    assert prop_name is not None, f"No property found in {assertion}"

    wrapper_text = WRAPPER_PATH.read_text()
    wrapper_text = wrapper_text.replace("ASSERTION_FILE", str(assertion))
    wrapper_text = wrapper_text.replace("ASSERTION_NAME", prop_name)

    Path("assertion_wrapper.sv").write_text(wrapper_text)

    project_root = Path("/home/pandeyap/Desktop/MS_Thesis/llm_assertions/llm-fveval")
    proj_dir = project_root / f"jgproject_{name}"

    cmd = f""" 
    cd "{project_root}"
    source /opt/eda/cadence/.cshrc.cds.setup
    jg -no_gui -allow_unsupported_OS \
        -proj {proj_dir} \
        -tcl formal/jasper/compile_only.tcl    

    """
    try:
        proc = subprocess.run(
            ["tcsh", "-c", cmd],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=30   # seconds (start with 30–60)
        )
    except subprocess.TimeoutExpired as e:
        out = e.stdout.decode(errors="ignore") if isinstance(e.stdout, bytes) else (e.stdout or "")
        log_file.write_text(out + "\n[TIMEOUT]\n")
        results[name] = {
            "status": "TIMEOUT",
            "log": str(log_file)
        }
        continue
    
    subprocess.run(
        ["pkill", "-f", "jg_"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


    log_file.write_text(proc.stdout)

    if "ERROR" in proc.stdout or proc.returncode != 0:
        status = "COMPILE_FAIL"
        dest = OUT_DIR / "fail"
    else:
        status = "COMPILE_PASS"
        dest = OUT_DIR / "pass"

    dest.mkdir(exist_ok=True)
    shutil.copy(assertion, dest / assertion.name)

    results[name] = {
        "status" : status, 
        "log" : str(log_file)
    }

with open(OUT_DIR / "compile_results.json", "w") as f:
    json.dump(results, f, indent = 2)

print("Phase - 1 compile classification complete")