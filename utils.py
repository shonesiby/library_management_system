# ──────────────────────────────────────────
#  utils.py  –  Shared helper utilities
# ──────────────────────────────────────────

def print_header(title: str):
    """Print a styled section header."""
    width = 60
    print("\n" + "═" * width)
    print(f"  {title.upper()}")
    print("═" * width)


def print_table(headers: list, rows: list):
    """Pretty-print a table from headers + rows."""
    if not rows:
        print("  (no records found)")
        return

    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell) if cell is not None else ""))

    sep = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    row_fmt = "|" + "|".join(f" {{:<{w}}} " for w in col_widths) + "|"

    print(sep)
    print(row_fmt.format(*headers))
    print(sep)
    for row in rows:
        formatted = [str(c) if c is not None else "" for c in row]
        print(row_fmt.format(*formatted))
    print(sep)
    print(f"  Total records: {len(rows)}")


def input_int(prompt: str, min_val: int = None, max_val: int = None) -> int:
    """Read a validated integer from stdin."""
    while True:
        try:
            val = int(input(prompt))
            if (min_val is not None and val < min_val) or \
               (max_val is not None and val > max_val):
                print(f"  Please enter a number between {min_val} and {max_val}.")
            else:
                return val
        except ValueError:
            print("  Invalid input – please enter a whole number.")


def confirm(prompt: str = "Are you sure? (y/n): ") -> bool:
    """Yes/No confirmation."""
    return input(prompt).strip().lower() in ("y", "yes")
