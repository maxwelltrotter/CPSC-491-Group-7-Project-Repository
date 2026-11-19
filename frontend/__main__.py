"""Start the mock frontend or perform a headless demo-data preflight."""

import argparse


def main() -> int:
    parser = argparse.ArgumentParser(description="AI-IDS mock frontend")
    parser.add_argument(
        "--check-demo",
        action="store_true",
        help="validate bundled mock demo data without opening a GUI",
    )
    args = parser.parse_args()

    if args.check_demo:
        from .demo_preflight import check_demo_data

        try:
            result = check_demo_data()
            import tkinter as tk
        except (ImportError, OSError, ValueError) as error:
            parser.exit(1, f"Demo preflight FAILED: {error}\n")
        print(
            f"Demo preflight OK: {result['alert_count']} Mock/Synthetic alerts "
            f"({', '.join(result['alert_ids'])}); Tcl/Tk {tk.TkVersion}."
        )
        print("This does not verify that a desktop GUI can launch or that live detection works.")
        return 0

    from .app import run

    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
