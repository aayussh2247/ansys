# ANSYS

This repository provides a **new project named ANSYS** with a complete starter implementation of a small simulation workflow:

1. Build a rectangular mesh.
2. Apply boundary conditions.
3. Run an iterative steady-state heat solver.
4. Generate summary post-processing metrics.
5. Show a terminal preview of the solved field.

It is intentionally lightweight but organized like production engineering software so it can be extended into a larger platform.

## Features

- Structured mesh generation (`Mesh`) for 2D domains.
- Configurable simulation model (`SimulationConfig`).
- Boundary-condition aware finite-difference solver.
- Post-processing statistics (min/max/mean/center values).
- ASCII preview mode for quick visual validation in terminal.
- Command-line interface (`ansys`) for running jobs quickly.
- Unit tests for solver convergence and postprocessing consistency.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
ansys --nx 25 --ny 25 --iterations 3000 --left 100 --right 0 --preview
```

Example output:

```text
Simulation complete.
iterations: 3000
residual: 0.000341
min: 0.000000
max: 100.000000
mean: 24.731245
center: 24.912384

Preview (ASCII heatmap):
=.......................
*=-:::::::..............
#*+=--::::::...........
...
```

## Python API example

```python
from ansys.core import SimulationConfig, run_simulation
from ansys.postprocessing import render_ascii_preview

config = SimulationConfig(nx=20, ny=20, iterations=2000, left_bc=100.0, right_bc=0.0)
result = run_simulation(config)
print(result.summary())
print(render_ascii_preview(result.temperature))
```

## Project layout

- `src/ansys/core.py`: mesh, config, solver, and result models.
- `src/ansys/postprocessing.py`: computed simulation metrics and ASCII preview renderer.
- `src/ansys/cli.py`: CLI entrypoint.
- `tests/test_core.py`: behavior tests.

## Notes

This is not the official commercial ANSYS product. It is an educational/open starter codebase designed to be expanded with:

- more physics models,
- richer geometry and meshing,
- file I/O formats,
- and visualization.
