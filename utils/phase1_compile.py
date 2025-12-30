import subprocess 
import shutil
import json
from pathlib import Path 

ASSERT_DIR = Path("../llm_outputs/assertions")
OUT_DIR = Path('../llm_outputs/phase1_compile')
LOG_DIR = OUT_DIR / "logs"

OUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

results = {}

for assertion in sorted(ASSERT_DIR.glob("a*.sv")):
    name = assertion.stem 
    log_file = LOG_DIR / f"{name}.log"

    wrapper_text = Path("assertion_wrapper.sv").read_text()
    wrapper_text = wrapper_text.replace("ASSERTION_FILE", str(assertion))

    Path("assertion_wrapper.sv").write_text(wrapper_text)

    project_root = "some location"

    cmd = f""" 
    cd {project_root}
    source /opt/eda/cadence/.cshrc.cds.setup
    jg -no_gui -tcl formal/jasper/compile_only.tcl      

    """
    proc = subprocess.run(
        ["tcsh", "-c", cmd], 
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
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