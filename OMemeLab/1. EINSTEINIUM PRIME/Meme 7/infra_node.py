import os
import sys
import platform
import ctypes
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict

import requests

# Optional Qiskit (future backend). Will be used if installed.
try:
    from qiskit import QuantumCircuit, Aer, execute  # type: ignore
    QISKIT_AVAILABLE = True
except Exception:
    QISKIT_AVAILABLE = False

# -----------------------------
# Logging & configuration
# -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

@dataclass
class Config:
    repo_api_url: str = "https://api.github.com/repos/L11-21/L11-21"
    c_lib_name_win: str = "Viable.dll"
    c_lib_name_linux: str = "Viable.so"
    c_lib_rel_path: str = "."  # where the binary sits relative to script
    product_name: str = "Sparsity Rock"
    price_usd: float = 1.00
    # Fibonacci-based product code (Golden-step barcode)
    barcode_10d: str = "1123581347"


config = Config()

# -----------------------------
# Repo status and usage prediction
# -----------------------------

def check_repo_status(url: str) -> bool:
    try:
        r = requests.get(url, timeout=10)
        ok = (r.status_code == 200)
        logging.info("Repository accessible: %s", ok)
        return ok
    except Exception as e:
        logging.error("Failed to access repo: %s", e)
        return False


def predict_usage(hour: int) -> str:
    if 0 <= hour < 6:
        return "Low usage"
    elif 6 <= hour < 12:
        return "Moderate usage"
    elif 12 <= hour < 18:
        return "High usage"
    elif 18 <= hour < 24:
        return "Moderate usage"
    return "Invalid hour"


# -----------------------------
# Fibonacci utilities
# -----------------------------

def fib_sequence(n: int) -> List[int]:
    """Generate first n Fibonacci numbers (starting at 1, 1)."""
    if n <= 0:
        return []
    if n == 1:
        return [1]
    seq = [1, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq


def is_fibonacci(x: int) -> bool:
    """Check if x is Fibonacci via perfect square tests."""
    import math
    def is_square(k: int) -> bool:
        r = int(math.isqrt(k))
        return r * r == k
    return is_square(5 * x * x + 4) or is_square(5 * x * x - 4)


def golden_ratio() -> float:
    """Return φ (phi), the golden ratio."""
    return (1 + 5 ** 0.5) / 2


def map_to_fib_barcode(seed: str, length: int = 10) -> str:
    """
    Deterministically map a seed string to a Fibonacci-flavored numeric code.
    - Hash the seed  blend with Fibonacci sequence  mod 10 digits.
    - Ensures consistency and lore alignment.
    """
    import hashlib
    base = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    fibs = fib_sequence(length + 5)  # extra terms for mixing
    digits = []
    for i in range(length):
        hex_pair = base[i * 2:(i * 2) + 2]
        v = int(hex_pair, 16)
        d = (v + fibs[i]) % 10
        digits.append(str(d))
    code = "".join(digits)
    # guard against trivial sequences; nudge with phi if too uniform
    if len(set(digits)) <= 3:
        phi = int(golden_ratio() * 100) % 10
        digits[-1] = str((int(digits[-1]) + phi) % 10)
        code = "".join(digits)
    return code


# -----------------------------
# Cubit preparation (proportional scaffolding)
# -----------------------------

@dataclass
class CubitPlan:
    unit_length: float        # base unit length (e.g., 1 cubit)
    ratios: List[float]       # proportional ratios (e.g., Fibonacci/phi steps)
    notes: str                # lore/context


class CubitCounter:
    """
    Prepares proportions for the future counting cubits feature using Fibonacci and φ.
    This does not do geometry yet; it sets consistent ratios ready for downstream use.
    """
    def __init__(self, base_unit: float = 1.0):
        self.base_unit = base_unit
        self.phi = golden_ratio()
        self.fibs = fib_sequence(12)

    def plan(self) -> CubitPlan:
        ratios = [f / self.fibs[0] for f in self.fibs]  # normalized to 1
        ratios += [self.phi, self.phi ** 2, 1 / self.phi]
        return CubitPlan(
            unit_length=self.base_unit,
            ratios=ratios,
            notes="Fibonacci-normalized proportions + golden ratio harmonics for architectural scaling."
        )

    def snap_to_nearest_ratio(self, value: float) -> float:
        plan = self.plan()
        scaled = [self.base_unit * r for r in plan.ratios]
        return min(scaled, key=lambda x: abs(x - value))


# -----------------------------
# DNS severity and octal axes
# -----------------------------

DNS_SEVERITY: Dict[int, str] = {
    0o1: "Informational",
    0o2: "Low",
    0o3: "Medium",
    0o4: "High",
    0o5: "Critical",
    0o6: "Severe",
    0o7: "Catastrophic",
}

@dataclass
class OctalAxes:
    yOct: List[int]
    xOct: List[int]

OCTAL_AXES = OctalAxes(
    yOct=[0o1, 0o2, 0o3, 0o4, 0o5, 0o6, 0o7],
    xOct=[0o1, 0o2, 0o3, 0o4, 0o5, 0o6, 0o7],
)


# -----------------------------
# C library wrapper (ctypes)
# -----------------------------

class CLibrary:
    def __init__(self, config: Config):
        sysname = platform.system().lower()
        if "windows" in sysname:
            libfile = config.c_lib_name_win
        else:
            libfile = config.c_lib_name_linux

        lib_path = os.path.abspath(os.path.join(config.c_lib_rel_path, libfile))
        if not os.path.exists(lib_path):
            logging.warning("C library not found at: %s", lib_path)
            self.lib = None
            return

        try:
            self.lib = ctypes.CDLL(lib_path)
            self.lib.initialize_system.restype = None
            self.lib.set_aeration.argtypes = [ctypes.c_int]
            self.lib.set_aeration.restype = None
            self.lib.compute_with_cosmos.argtypes = [ctypes.c_int]
            self.lib.compute_with_cosmos.restype = ctypes.c_int
            logging.info("C library loaded: %s", lib_path)
        except Exception as e:
            logging.error("Failed to load C library: %s", e)
            self.lib = None

    def compute(self, cosmos_value: int, aeration: int = 5) -> Optional[int]:
        if not self.lib:
            logging.warning("C library unavailable; skipping compute.")
            return None
        self.lib.initialize_system()
        self.lib.set_aeration(aeration)
        res = int(self.lib.compute_with_cosmos(cosmos_value))
        logging.info("C compute result: %s", res)
        return res


# -----------------------------
# Qiskit backend (prepared, optional)
# -----------------------------

class QuantumBackend:
    def __init__(self):
        self.available = QISKIT_AVAILABLE

    def run_fib_pulse(self, fib_terms: int = 8) -> Optional[Dict]:
        if not self.available:
            logging.info("Qiskit not available; skipping quantum job.")
            return None

        fibs = fib_sequence(fib_terms)
        qc = QuantumCircuit(1, 1)
        for f in fibs:
            theta = (f % 8) * (3.14159 / 8.0)
            qc.rx(theta, 0)

        qc.measure(0, 0)
        backend = Aer.get_backend("qasm_simulator")
        job = execute(qc, backend, shots=256)
        result = job.result().get_counts()
        logging.info("Quantum fib pulse counts: %s", result)
        return {"counts": result, "fibs": fibs}


# -----------------------------
# Application glue
# -----------------------------

def main():
    repo_ok = check_repo_status(config.repo_api_url)
    logging.info("Repo OK: %s", repo_ok)

    hour = datetime.now().hour
    usage = predict_usage(hour)
    logging.info("Predicted usage @%02d: %s", hour, usage)

    logging.info("DNS severity spectrum: %s", DNS_SEVERITY)
    logging.info("yOct labels: %s", [DNS_SEVERITY[n] for n in OCTAL_AXES.yOct])
    logging.info("xOct labels: %s", [DNS_SEVERITY[n] for n in OCTAL_AXES.xOct])

    seed = f"{config.product_name}-{datetime.now().date().isoformat()}"
    fib_barcode = map_to_fib_barcode(seed, length=10)
    logging.info("Seeded Fibonacci barcode: %s", fib_barcode)
    logging.info("Golden-step barcode (fixed): %s", config.barcode_10d)

    cubits = CubitCounter(base_unit=1.0)
    plan = cubits.plan()
    logging.info("Cubit plan unit: %s | ratios: %s", plan.unit_length, plan.ratios)

    snap_example = cubits.snap_to_nearest_ratio(3.2)
    logging.info("Snap 3.2  nearest proportional length: %s", snap_example)

    cwrap = CLibrary(config)
    c_res = cwrap.compute(cosmos_value=3, aeration=5)
    logging.info("C library result: %s", c_res)

    qback = QuantumBackend()
    q_res = qback.run_fib_pulse(fib_terms=10)
    logging.info("Quantum result: %s", q_res)

    summary = {
        "repo_access": repo_ok,
        "usage_window": usage,
        "dns_labels": DNS_SEVERITY,
        "product": {
            "name": config.product_name,
            "price_usd": config.price_usd,
            "barcode_fixed": config.barcode_10d,
            "barcode_seeded": fib_barcode,
        },
        "cubit_plan": {
            "unit": plan.unit_length,
            "ratios_count": len(plan.ratios),
            "phi": golden_ratio(),
        },
        "c_lib_result": c_res,
        "quantum": q_res,
    }
    logging.info("Node summary: %s", summary)
    return summary


if __name__ == "__main__":
    main()
