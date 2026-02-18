from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .postprocessing import compute_metrics


@dataclass(slots=True)
class Mesh:
    nx: int
    ny: int
    width: float = 1.0
    height: float = 1.0

    @property
    def dx(self) -> float:
        return self.width / (self.nx - 1)

    @property
    def dy(self) -> float:
        return self.height / (self.ny - 1)


@dataclass(slots=True)
class SimulationConfig:
    nx: int = 20
    ny: int = 20
    iterations: int = 2000
    tolerance: float = 1e-6
    left_bc: float = 100.0
    right_bc: float = 0.0
    top_bc: float = 0.0
    bottom_bc: float = 0.0

    def validate(self) -> None:
        if self.nx < 3 or self.ny < 3:
            raise ValueError("nx and ny must be >= 3")
        if self.iterations <= 0:
            raise ValueError("iterations must be > 0")
        if self.tolerance <= 0:
            raise ValueError("tolerance must be > 0")


@dataclass(slots=True)
class SimulationResult:
    config: SimulationConfig
    temperature: List[List[float]]
    iterations_used: int
    residual: float

    def summary(self) -> str:
        metrics = compute_metrics(self.temperature)
        return (
            f"iterations: {self.iterations_used}\n"
            f"residual: {self.residual:.6f}\n"
            f"min: {metrics['min']:.6f}\n"
            f"max: {metrics['max']:.6f}\n"
            f"mean: {metrics['mean']:.6f}\n"
            f"center: {metrics['center']:.6f}"
        )


def _initialize_field(config: SimulationConfig) -> List[List[float]]:
    field = [[0.0 for _ in range(config.nx)] for _ in range(config.ny)]

    for y in range(config.ny):
        field[y][0] = config.left_bc
        field[y][-1] = config.right_bc

    for x in range(config.nx):
        field[0][x] = config.top_bc
        field[-1][x] = config.bottom_bc

    field[0][0] = (config.top_bc + config.left_bc) / 2.0
    field[0][-1] = (config.top_bc + config.right_bc) / 2.0
    field[-1][0] = (config.bottom_bc + config.left_bc) / 2.0
    field[-1][-1] = (config.bottom_bc + config.right_bc) / 2.0
    return field


def run_simulation(config: SimulationConfig) -> SimulationResult:
    config.validate()
    _ = Mesh(nx=config.nx, ny=config.ny)
    field = _initialize_field(config)

    residual = float("inf")
    iterations_used = 0

    for step in range(1, config.iterations + 1):
        residual = 0.0

        for y in range(1, config.ny - 1):
            for x in range(1, config.nx - 1):
                old_value = field[y][x]
                new_value = 0.25 * (
                    field[y - 1][x] + field[y + 1][x] + field[y][x - 1] + field[y][x + 1]
                )
                field[y][x] = new_value
                residual = max(residual, abs(new_value - old_value))

        iterations_used = step
        if residual < config.tolerance:
            break

    return SimulationResult(
        config=config,
        temperature=field,
        iterations_used=iterations_used,
        residual=residual,
    )
