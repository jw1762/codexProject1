from __future__ import annotations

from generator.palette import Palette
from generator.seed import rng_for_part
from generator.skeleton import DragonSkeleton
from render.image import Image, Rect, union_rects

from .common import PartResult


def generate(seed: int, skeleton: DragonSkeleton, palette: Palette) -> PartResult:
    rng = rng_for_part(seed, "neck")
    img = Image(skeleton.width, skeleton.height)
    base = skeleton.neck_base
    length = max(18, min(52, int(skeleton.torso_bounds[0] * 0.7) + rng.randint(-6, 6)))
    thickness = max(8, min(18, int(skeleton.torso_bounds[1] * 0.28) + rng.randint(-2, 2)))
    seg = max(4, length // 4)
    rects: list[Rect] = []
    for i in range(seg):
        x = base.x + i * (length // seg)
        y = base.y - i * 2
        rects.append(img.fill_ellipse(x, y, thickness // 2, thickness // 3 + 1, palette.base))
        if i % 2 == 0:
            rects.append(img.fill_rect(x - 1, y - thickness // 2, 3, 3, palette.highlight))
    return PartResult("neck", img, union_rects(rects))
