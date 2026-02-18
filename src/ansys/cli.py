from __future__ import annotations

import argparse

from .core import SimulationConfig, run_simulation
from .postprocessing import render_ascii_preview


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run ANSYS starter thermal simulation")
    parser.add_argument("--nx", type=int, default=20)
    parser.add_argument("--ny", type=int, default=20)
    parser.add_argument("--iterations", type=int, default=2000)
    parser.add_argument("--tolerance", type=float, default=1e-6)
    parser.add_argument("--left", dest="left_bc", type=float, default=100.0)
    parser.add_argument("--right", dest="right_bc", type=float, default=0.0)
    parser.add_argument("--top", dest="top_bc", type=float, default=0.0)
    parser.add_argument("--bottom", dest="bottom_bc", type=float, default=0.0)
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Print an ASCII heatmap preview of the final temperature field",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    config = SimulationConfig(
        nx=args.nx,
        ny=args.ny,
        iterations=args.iterations,
        tolerance=args.tolerance,
        left_bc=args.left_bc,
        right_bc=args.right_bc,
        top_bc=args.top_bc,
        bottom_bc=args.bottom_bc,
    )
    result = run_simulation(config)
    print("Simulation complete.")
    print(result.summary())

    if args.preview:
        print("\nPreview (ASCII heatmap):")
        print(render_ascii_preview(result.temperature))


if __name__ == "__main__":
    main()
