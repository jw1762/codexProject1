from __future__ import annotations

from generator.palette import Palette
from generator.seed import rng_for_part
from generator.skeleton import DragonSkeleton
from render.image import Image, Rect, union_rects

from .common import PartResult


def generate(seed: int, skeleton: DragonSkeleton, palette: Palette) -> PartResult:
    rng = rng_for_part(seed, "tail")
    img = Image(skeleton.width, skeleton.height)
    base = skeleton.tail_base
    length = max(30, min(90, int(skeleton.torso_bounds[0] * 1.5) + rng.randint(-10, 10)))
    thickness = max(6, min(16, int(skeleton.torso_bounds[1] * 0.3)))
    rects: list[Rect] = []
    for i in range(8):
        t = i / 7
        x = base.x - int(length * t)
        y = base.y + int(10 * t)
        rx = max(2, thickness - i)
        ry = max(2, thickness // 2 - i // 2)
        color = palette.base if i < 5 else palette.shadow
        rects.append(img.fill_ellipse(x, y, rx, ry, color))
    spike = img.fill_rect(base.x - length - 4, base.y + 8, 5, 3, palette.horn)
    rects.append(spike)
    return PartResult("tail", img, union_rects(rects))
