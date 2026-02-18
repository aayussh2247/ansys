from ansys.core import SimulationConfig, run_simulation
from ansys.postprocessing import compute_metrics, render_ascii_preview


def test_run_simulation_converges_and_preserves_boundaries() -> None:
    config = SimulationConfig(nx=15, ny=15, iterations=2500, tolerance=1e-5, left_bc=100, right_bc=0)
    result = run_simulation(config)

    assert result.iterations_used <= config.iterations
    assert result.residual < 0.1

    for row in result.temperature[1:-1]:
        assert abs(row[0] - config.left_bc) < 1e-9
        assert abs(row[-1] - config.right_bc) < 1e-9


def test_metrics_are_consistent() -> None:
    config = SimulationConfig(nx=10, ny=10, iterations=1000, tolerance=1e-4)
    result = run_simulation(config)
    metrics = compute_metrics(result.temperature)

    assert metrics["max"] >= metrics["mean"] >= metrics["min"]
    assert metrics["min"] <= metrics["center"] <= metrics["max"]


def test_ascii_preview_has_expected_shape() -> None:
    config = SimulationConfig(nx=8, ny=6, iterations=300, tolerance=1e-5)
    result = run_simulation(config)
    preview = render_ascii_preview(result.temperature)

    lines = preview.splitlines()
    assert len(lines) == config.ny
    assert all(len(line) == config.nx for line in lines)
