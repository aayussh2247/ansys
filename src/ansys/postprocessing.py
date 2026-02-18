from __future__ import annotations

from typing import Dict, List


def compute_metrics(field: List[List[float]]) -> Dict[str, float]:
    if not field or not field[0]:
        raise ValueError("field cannot be empty")

    ny = len(field)
    nx = len(field[0])

    values = [value for row in field for value in row]
    center_y = ny // 2
    center_x = nx // 2

    return {
        "min": min(values),
        "max": max(values),
        "mean": sum(values) / len(values),
        "center": field[center_y][center_x],
    }


def render_ascii_preview(field: List[List[float]], levels: str = " .:-=+*#%@") -> str:
    """Render a scalar field as a coarse ASCII heatmap preview."""
    if not field or not field[0]:
        raise ValueError("field cannot be empty")
    if len(levels) < 2:
        raise ValueError("levels must contain at least two characters")

    flat_values = [value for row in field for value in row]
    min_v = min(flat_values)
    max_v = max(flat_values)

    if max_v == min_v:
        idx = len(levels) // 2
        char = levels[idx]
        return "\n".join(char * len(field[0]) for _ in field)

    scale = (len(levels) - 1) / (max_v - min_v)

    lines: List[str] = []
    for row in field:
        chars = []
        for value in row:
            level_idx = int(round((value - min_v) * scale))
            level_idx = max(0, min(level_idx, len(levels) - 1))
            chars.append(levels[level_idx])
        lines.append("".join(chars))

    return "\n".join(lines)
