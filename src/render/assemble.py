from __future__ import annotations

from generator.skeleton import DragonSkeleton
from parts.common import PartResult
from render.image import Image, Rect


class FitError(RuntimeError):
    pass


def _region_intersects_nontransparent(part: PartResult, region: tuple[int, int, int, int]) -> bool:
    x, y, w, h = region
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(part.image.width, x + w)
    y1 = min(part.image.height, y + h)
    for yy in range(y0, y1):
        for xx in range(x0, x1):
            if part.image.pixels[yy * part.image.width + xx][3] > 0:
                return True
    return False


def guard_part_fit(skeleton: DragonSkeleton, part: PartResult) -> None:
    torso_w, torso_h = skeleton.torso_bounds
    max_w = int(torso_w * 2.6)
    max_h = int(torso_h * 2.6)
    if (part.bbox.x1 - part.bbox.x0) > max_w and part.name in {"head", "neck", "legs", "tail"}:
        raise FitError(f"{part.name} width too large for torso proportions")
    if (part.bbox.y1 - part.bbox.y0) > max_h and part.name in {"head", "neck", "legs", "tail"}:
        raise FitError(f"{part.name} height too large for torso proportions")

    if part.name in {"legs", "wings"} and _region_intersects_nontransparent(
        part, skeleton.forbidden_torso_region
    ):
        raise FitError(f"{part.name} intersects forbidden torso region")


def compose_layers(width: int, height: int, layers: list[PartResult]) -> Image:
    canvas = Image(width, height)
    for layer in layers:
        canvas.composite(layer.image)
    return canvas


def order_parts(parts: dict[str, PartResult]) -> list[PartResult]:
    return [
        parts["tail"],
        parts["legs"],
        parts["wings_back"],
        parts["torso"],
        parts["wings_front"],
        parts["neck"],
        parts["head"],
    ]
