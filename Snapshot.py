"""
snapshot.py  -  save and compare optimizer results (WPG vs bipath WPG)

Put this file in the same folder as actOpt.py and run it from that folder.

Workflow
--------
1.  python actOpt.py U8 wpg 11              (run the plain WPG)
2.  python snapshot.py save wpg_U8 wpg U8     (take a snapshot of that result)
3.  python actOpt.py U8 bipathwpg 11        (run the bipath WPG)
4.  python snapshot.py save bwpg_U8 bwpg U8   (take a snapshot of that result)
5.  python snapshot.py compare wpg_U8 bwpg_U8 (side-by-side table)

Other commands
--------------
python snapshot.py list                      (show saved snapshots)
python snapshot.py show <name>               (print one snapshot)
python snapshot.py compare                   (compare the last two snapshots)
python snapshot.py compare <a> <b> all       (also show values that are equal)
python snapshot.py delete <name>             (remove a snapshot)

When saving, the design is rebuilt with your own actuator code to get the
forces in every mesh and the thickness of every gear.

Snapshots are kept in snapshots.json, so they survive between runs.
Each comparison is also written to results/comparisons/<a>_vs_<b>.csv.
"""

import contextlib
import csv
import importlib
import io
import json
import os
import re
import sys
from datetime import datetime

# --------------------------------------------------------------------------
# Where the optimizer writes its results (relative to this file's folder).
# Change these if your file names are different.
# --------------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
SNAPSHOT_FILE = os.path.join(HERE, "snapshots.json")

SOURCES = {
    "wpg": {
        "csv": os.path.join("results", "results_BruteForce_{motor}", "WPG_BRUTEFORCE_MIT_{motor}.csv"),
        "eq":  os.path.join("CADs", "WPG", "wpg_equations.txt"),
    },
    "bwpg": {
        "csv": os.path.join("results", "results_BruteForce_{motor}", "BWPG_BRUTEFORCE_MIT_{motor}.csv"),
        # after the file-name edit this is bwpg_equations.txt; the old name is tried as a fallback
        "eq":  os.path.join("CADs", "BIPATHWPG", "bwpg_equations.txt"),
        "eq_fallback": os.path.join("CADs", "BIPATHWPG", "wpg_equations.txt"),
    },
}

# Results shown first in the comparison, in this order (CSV column names).
KEY_RESULTS = [
    "gearRatio", "mass", "eff", "peakTorque", "Torque_Density", "Actuator_width", "Cost",
    "numPlanet", "moduleBig", "Ns", "NpBig", "NpSmall", "NrBig", "NrSmall",
    "fwSunMM", "fwPlanetBigMM", "fwPlanetSmallMM", "fwRingBigMM", "fwRingSmallMM",
    "gear_stack_width", "Outer_Bearing_mass",
]

# Driver module and gearbox attribute for each type (used to recompute forces and widths)
DRIVERS = {
    "wpg":  {"module": "Opt_wolfromPlanetaryGBOptimization",       "gearbox_attr": "wolfromPlanetaryGearbox"},
    "bwpg": {"module": "Opt_bipathWolfromPlanetaryGBOptimisation", "gearbox_attr": "bipathwolfromPlanetaryGearbox"},
}

# What is printed, section by section: (description, key, unit).
# A key is looked up in the recomputed values first, then the equation file, then the results CSV.
LAYOUT = [
    ("OVERVIEW", [
        ("Gear ratio",                                   "gearRatio",       ""),
        ("Actuator mass",                                "mass",            "kg"),
        ("Efficiency",                                   "eff",             ""),
        ("Peak output torque",                           "peakTorque",      "Nm"),
        ("Torque density",                               "Torque_Density",  "Nm/kg"),
        ("Actuator axial width (whole actuator)",        "Actuator_width",  "mm"),
        ("Optimizer cost",                               "Cost",            ""),
        ("Number of planets",                            "numPlanet",       ""),
        ("Module",                                       "moduleBig",       "mm"),
        ("Sun teeth",                                    "Ns",              ""),
        ("Big planet teeth",                             "NpBig",           ""),
        ("Small planet teeth (= idler teeth)",           "NpSmall",         ""),
        ("Big ring teeth",                               "NrBig",           ""),
        ("Small ring teeth",                             "NrSmall",         ""),
        ("Floating sun teeth",                           "Ns_fs",           ""),
        ("Bypass load share beta (direct path)",         "beta",            ""),
    ]),
    ("THICKNESS - STAGE 1 (big gears)", [
        ("Big planet gear thickness",                    "fw_p_b",          "mm"),
        ("Big ring gear thickness (fixed ring)",         "fw_r_b",          "mm"),
        ("Sun min width from stress (reference only)",   "fw_s_calc",       "mm"),
    ]),
    ("THICKNESS - STAGE 2 (small gears)", [
        ("Small ring gear thickness (output ring)",      "fw_r_s",          "mm"),
        ("Small planet gear thickness",                  "fw_p_s",          "mm"),
        ("Floating sun thickness",                       "fw_fs",           "mm"),
        ("Idler planet thickness",                       "fw_idler",        "mm"),
    ]),
    ("THICKNESS - WHOLE STACK", [
        ("Sun gear total length",                        "fw_s_used",       "mm"),
        ("Gap between carrier plates",                   "carrier_inner_gap", "mm"),
        ("Stage 1 + stage 2 planet widths",              "gear_stack_width", "mm"),
    ]),
    ("RADIAL THICKNESS (walls)", [
        ("Big ring wall",                                "ring_radial_thickness",            "mm"),
        ("Small ring casing wall",                       "small_ring_case_thickness",        "mm"),
        ("Small ring output wall",                       "small_ring_output_wall_thickness", "mm"),
        ("Carrier plate",                                "carrier_thickness",                "mm"),
        ("Sec carrier plate",                            "sec_carrier_thickness",            "mm"),
    ]),
    ("FORCES PER PLANET (tangential, at pitch circle, incl. service factor)", [
        ("Sun <-> big planet",                           "F_sun_bigplanet",          "N"),
        ("Big planet <-> big ring",                      "F_bigplanet_bigring",      "N"),
        ("Small planet <-> small ring (direct path)",    "F_smallplanet_smallring",  "N"),
        ("Small planet <-> floating sun (bypass)",       "F_smallplanet_floatsun",   "N"),
        ("Floating sun <-> idler (bypass)",              "F_floatsun_idler",         "N"),
        ("Idler <-> small ring (bypass)",                "F_idler_smallring",        "N"),
        ("Total into small ring (direct + bypass)",      "F_total_smallring",        "N"),
        ("Idler pin load (estimate: 2 x bypass)",        "F_idler_pin_est",          "N"),
    ]),
]


# --------------------------------------------------------------------------
# Reading the optimizer outputs
# --------------------------------------------------------------------------
def to_number(text):
    """Turn '12.5' into 12.5 and '4' into 4; leave anything else as text."""
    text = text.strip()
    try:
        value = float(text)
        return int(value) if value.is_integer() and "." not in text else value
    except ValueError:
        return text


def read_results_csv(path):
    """Return the last result row of an optimizer CSV as a dict, plus the row count."""
    with open(path, "r") as f:
        lines = [line.strip() for line in f]

    # The header is the line whose first field is 'iter'; result rows follow it.
    header_index = None
    for i, line in enumerate(lines):
        if line.split(",")[0].strip() == "iter":
            header_index = i
    if header_index is None:
        raise ValueError("no 'iter, gearRatio, ...' header line found")

    header = [h.strip() for h in lines[header_index].split(",")]
    header = ["fwPlanetSmallMM" if h == "fwPanetSmallMM" else h for h in header]  # fix typo in the optimizer

    rows = []
    for line in lines[header_index + 1:]:
        fields = [x.strip() for x in line.split(",")]
        if len(fields) == len(header) and isinstance(to_number(fields[0]), (int, float)):
            rows.append(dict(zip(header, (to_number(x) for x in fields))))
    if not rows:
        raise ValueError("header found but no result rows (no design met the gear ratio?)")

    result = rows[-1]
    if isinstance(result.get("fwPlanetBigMM"), (int, float)) and isinstance(result.get("fwPlanetSmallMM"), (int, float)):
        result["gear_stack_width"] = round(result["fwPlanetBigMM"] + result["fwPlanetSmallMM"], 3)
    return result, len(rows)


def read_equation_file(path):
    """Read lines like  "Ns" = 56  into a dict."""
    values = {}
    pattern = re.compile(r'^"(.+?)"\s*=\s*(.+)$')
    with open(path, "r") as f:
        for line in f:
            match = pattern.match(line.strip())
            if match:
                values[match.group(1)] = to_number(match.group(2))
    return values


def recompute_with_model(gearbox_type, motor, results):
    """Rebuild the chosen design with your actuator code and read thicknesses and forces.

    Uses the driver file for this gearbox type, so the numbers come from exactly the
    same code the optimizer uses. Returns {} (with a warning) if anything is missing.
    """
    needed = ["moduleBig", "moduleSmall", "Ns", "NpBig", "NpSmall", "NrBig", "NrSmall", "numPlanet"]
    if not all(isinstance(results.get(k), (int, float)) for k in needed):
        print("WARNING: tooth counts missing from the CSV, so forces could not be recomputed")
        return {}

    info = DRIVERS[gearbox_type]
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    try:
        with contextlib.redirect_stdout(io.StringIO()):      # keep the driver's prints out of the way
            driver = importlib.import_module(info["module"])
            actuator = getattr(driver, f"Actuator_{motor}")
            gb = getattr(actuator, info["gearbox_attr"])
            gb.setModuleBig(results["moduleBig"]); gb.setModuleSmall(results["moduleSmall"])
            gb.setNs(results["Ns"]); gb.setNpBig(results["NpBig"]); gb.setNpSmall(results["NpSmall"])
            gb.setNrBig(results["NrBig"]); gb.setNrSmall(results["NrSmall"]); gb.setNumPlanet(results["numPlanet"])
            actuator.updateFacewidth()
            forces = actuator.getToothForces(False)
            actuator.getMassKG_3DP()
            actuator.setVariables()
    except Exception as err:
        print(f"WARNING: could not recompute forces with {info['module']}.py: {err}")
        return {}

    f_sp, f_rb, f_rs = (abs(float(x)) for x in forces)
    calc = {
        "F_sun_bigplanet": round(f_sp, 2),
        "F_bigplanet_bigring": round(f_rb, 2),
        "F_smallplanet_smallring": round(f_rs, 2),
    }
    if gearbox_type == "bwpg":
        f_bp = abs(float(getattr(actuator, "Ft_bypass", f_rs)))   # old /2 code: bypass = direct
        calc.update({
            "beta": actuator.design_params.get("bypass_load_share", 0.5),
            "F_smallplanet_floatsun": round(f_bp, 2),
            "F_floatsun_idler": round(f_bp, 2),
            "F_idler_smallring": round(f_bp, 2),
            "F_total_smallring": round(f_rs + f_bp, 2),
            "F_idler_pin_est": round(2 * f_bp, 2),
        })
    else:
        calc.update({"beta": 1.0, "F_total_smallring": round(f_rs, 2)})

    for name in ["fw_p_b", "fw_r_b", "fw_s_calc", "fw_r_s", "fw_p_s", "fw_fs", "fw_idler", "fw_s_used",
                 "ring_radial_thickness", "small_ring_case_thickness", "small_ring_output_wall_thickness",
                 "carrier_thickness", "sec_carrier_thickness", "Ns_fs"]:
        if hasattr(actuator, name):
            value = getattr(actuator, name)
            calc[name] = round(float(value), 3) if isinstance(value, (int, float)) else value
    if all(k in calc for k in ("fw_p_b", "fw_p_s")) and hasattr(actuator, "clearance_planet"):
        calc["carrier_inner_gap"] = round(calc["fw_p_b"] + calc["fw_p_s"] + actuator.clearance_planet, 3)
    return calc


def file_time(path):
    return datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")


# --------------------------------------------------------------------------
# Snapshot storage
# --------------------------------------------------------------------------
def load_snapshots():
    if os.path.exists(SNAPSHOT_FILE):
        with open(SNAPSHOT_FILE, "r") as f:
            return json.load(f)
    return {}


def save_snapshots(snapshots):
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(snapshots, f, indent=2)


def cmd_save(name, gearbox_type, motor):
    gearbox_type = gearbox_type.lower()
    if gearbox_type not in SOURCES:
        sys.exit(f"Type must be one of {list(SOURCES)}, not '{gearbox_type}'")

    src = SOURCES[gearbox_type]
    csv_path = os.path.join(HERE, src["csv"].format(motor=motor))
    eq_path = os.path.join(HERE, src["eq"])
    if not os.path.exists(eq_path) and "eq_fallback" in src:
        eq_path = os.path.join(HERE, src["eq_fallback"])

    snapshot = {
        "type": gearbox_type,
        "motor": motor,
        "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": {},
        "cad": {},
        "calc": {},
        "sources": {},
    }

    if os.path.exists(csv_path):
        try:
            snapshot["results"], n_rows = read_results_csv(csv_path)
            snapshot["sources"]["csv"] = {"path": csv_path, "modified": file_time(csv_path)}
            print(f"Results CSV : {csv_path}")
            print(f"              last written {file_time(csv_path)}, {n_rows} result row(s), using the last one")
        except ValueError as err:
            print(f"WARNING: could not read {csv_path}: {err}")
    else:
        print(f"WARNING: results CSV not found: {csv_path}")

    if os.path.exists(eq_path):
        snapshot["cad"] = read_equation_file(eq_path)
        snapshot["sources"]["eq"] = {"path": eq_path, "modified": file_time(eq_path)}
        print(f"Equation file: {eq_path}")
        print(f"              last written {file_time(eq_path)}, {len(snapshot['cad'])} variables")
    else:
        print(f"WARNING: equation file not found: {eq_path}")

    if snapshot["results"]:
        snapshot["calc"] = recompute_with_model(gearbox_type, motor, snapshot["results"])
        if snapshot["calc"]:
            print(f"Forces and thicknesses recomputed with {DRIVERS[gearbox_type]['module']}.py")

    if not snapshot["results"] and not snapshot["cad"]:
        sys.exit("Nothing was read, so no snapshot was saved. Did the optimizer run from this folder?")

    snapshots = load_snapshots()
    if name in snapshots:
        print(f"Note: replacing the existing snapshot '{name}'")
    snapshots[name] = snapshot
    save_snapshots(snapshots)
    print(f"Saved snapshot '{name}'. Check the times above match the run you just did.")


def cmd_list():
    snapshots = load_snapshots()
    if not snapshots:
        print("No snapshots saved yet.")
        return
    print(f"{'name':<20}{'type':<7}{'motor':<11}{'saved at':<21}{'GR':>8}{'mass kg':>10}")
    for name, s in snapshots.items():
        r = s.get("results", {})
        gr = r.get("gearRatio", "")
        mass = r.get("mass", "")
        gr = f"{gr:.3f}" if isinstance(gr, float) else gr
        print(f"{name:<20}{s['type']:<7}{s['motor']:<11}{s['saved_at']:<21}{gr:>8}{mass:>10}")


def lookup(snapshot, key):
    for section in ("calc", "cad", "results"):
        if key in snapshot.get(section, {}):
            return snapshot[section][key]
    return None


def cmd_show(name):
    snapshots = load_snapshots()
    if name not in snapshots:
        sys.exit(f"No snapshot called '{name}'. Use: python snapshot.py list")
    s = snapshots[name]
    print(f"{name}  ({s['type']}, {s['motor']}, saved {s['saved_at']})")
    for title, items in LAYOUT:
        rows = [(d, k, u, lookup(s, k)) for d, k, u in items if lookup(s, k) is not None]
        if rows:
            print(f"\n{title}")
            for desc, key, unit, value in rows:
                print(f"  {desc:<46}{key:<34}{fmt(value):>12} {unit}")
    print("\n(use 'python snapshot.py compare' to see all CAD variables)")


def cmd_delete(name):
    snapshots = load_snapshots()
    if snapshots.pop(name, None) is None:
        sys.exit(f"No snapshot called '{name}'.")
    save_snapshots(snapshots)
    print(f"Deleted '{name}'.")


# --------------------------------------------------------------------------
# Comparison
# --------------------------------------------------------------------------
def fmt(value):
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.4g}" if abs(value) < 1e5 else f"{value:.4e}"
    return str(value)


def diff_of(va, vb):
    if isinstance(va, (int, float)) and isinstance(vb, (int, float)):
        diff = vb - va
        pct = (diff / va * 100) if va != 0 else None
        return diff, pct
    return None, None


def print_section(title, rows, name_a, name_b):
    """rows: (description, key, unit, va, vb)"""
    if not rows:
        return
    print(f"\n{title}")
    print(f"  {'what it is':<44}{'variable':<34}{name_a:>12}{name_b:>12}{'diff':>11}{'%':>8}  unit")
    print("  " + "-" * 126)
    for desc, key, unit, va, vb in rows:
        diff, pct = diff_of(va, vb)
        diff_text = f"{diff:+.4g}" if diff is not None else ""
        pct_text = f"{pct:+.1f}" if pct is not None else ""
        print(f"  {desc:<44}{key:<34}{fmt(va):>12}{fmt(vb):>12}{diff_text:>11}{pct_text:>8}  {unit}")


def cmd_compare(name_a=None, name_b=None, show_all=False):
    snapshots = load_snapshots()
    if name_a is None:
        if len(snapshots) < 2:
            sys.exit("Need at least two snapshots. Use: python snapshot.py save ...")
        name_a, name_b = list(snapshots)[-2:]
    for n in (name_a, name_b):
        if n not in snapshots:
            sys.exit(f"No snapshot called '{n}'. Use: python snapshot.py list")
    a, b = snapshots[name_a], snapshots[name_b]

    print(f"Comparing  {name_a} ({a['type']}, {a['motor']})  ->  {name_b} ({b['type']}, {b['motor']})")
    print("diff and % are second minus first;  '-' means that design does not have this part")

    csv_rows = []
    shown_keys = set()
    for title, items in LAYOUT:
        rows = []
        for desc, key, unit in items:
            va, vb = lookup(a, key), lookup(b, key)
            if va is None and vb is None:
                continue
            rows.append((desc, key, unit, va, vb))
            shown_keys.add(key)
            csv_rows.append((title, desc, key, unit, va, vb))
        print_section(title, rows, name_a, name_b)

    # every other CAD variable: the ones that differ (or all, with 'all')
    cad_a, cad_b = a.get("cad", {}), b.get("cad", {})
    other = [k for k in list(cad_a) + [k for k in cad_b if k not in cad_a] if k not in shown_keys]
    rows = []
    for key in other:
        va, vb = cad_a.get(key), cad_b.get(key)
        if not show_all and va == vb:
            continue
        rows.append(("", key, "", va, vb))
        csv_rows.append(("OTHER CAD VARIABLES", "", key, "", va, vb))
    title = "OTHER CAD VARIABLES" + ("" if show_all else " THAT DIFFER") + " (equation file)"
    print_section(title, rows, name_a, name_b)
    if not show_all:
        hidden = sum(1 for k in other if cad_a.get(k) == cad_b.get(k))
        print(f"\n({hidden} other CAD variables are equal and hidden; add 'all' to show them)")
    if not a.get("calc") or not b.get("calc"):
        print("\nNote: a snapshot has no recomputed forces (saved with an older snapshot.py, or the")
        print("      driver could not be loaded). Save it again to get the force section.")

    out_dir = os.path.join(HERE, "results", "comparisons")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{name_a}_vs_{name_b}.csv")
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["section", "what_it_is", "variable", "unit", name_a, name_b, "difference", "change_%"])
        for title, desc, key, unit, va, vb in csv_rows:
            diff, pct = diff_of(va, vb)
            writer.writerow([title, desc, key, unit, va, vb,
                             "" if diff is None else round(diff, 6),
                             "" if pct is None else round(pct, 3)])
    print(f"Comparison saved to {out_path}")


# --------------------------------------------------------------------------
def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    command = args[0].lower()

    if command == "save":
        if len(args) < 3:
            sys.exit("Usage: python snapshot.py save <name> <wpg|bwpg> [motor, default U8]")
        cmd_save(args[1], args[2], args[3] if len(args) > 3 else "U8")
    elif command == "list":
        cmd_list()
    elif command == "show":
        if len(args) < 2:
            sys.exit("Usage: python snapshot.py show <name>")
        cmd_show(args[1])
    elif command == "compare":
        show_all = "all" in [x.lower() for x in args[1:]]
        names = [x for x in args[1:] if x.lower() != "all"]
        if len(names) == 2:
            cmd_compare(names[0], names[1], show_all)
        elif len(names) == 0:
            cmd_compare(show_all=show_all)
        else:
            sys.exit("Usage: python snapshot.py compare [<first> <second>] [all]")
    elif command == "delete":
        if len(args) < 2:
            sys.exit("Usage: python snapshot.py delete <name>")
        cmd_delete(args[1])
    else:
        print(__doc__)


if __name__ == "__main__":
    main()