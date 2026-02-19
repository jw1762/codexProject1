from __future__ import annotations

from generator.palette import Palette
from generator.seed import rng_for_part
from generator.skeleton import DragonSkeleton
from render.image import Image, Rect, union_rects

from .common import PartResult


def generate(seed: int, skeleton: DragonSkeleton, palette: Palette) -> PartResult:
    rng = rng_for_part(seed, "wings")
    img = Image(skeleton.width, skeleton.height)
    left = skeleton.left_wing_base
    right = skeleton.right_wing_base
    span = max(36, min(int(skeleton.width * 0.38), 90 + rng.randint(-16, 14)))
    depth = max(24, min(int(skeleton.height * 0.32), 54 + rng.randint(-10, 8)))
    rects: list[Rect] = []
    rects.append(img.fill_rect(left.x - span, left.y - 4, span, 8, palette.shadow))
    rects.append(img.fill_ellipse(left.x - span // 2, left.y + depth // 3, span // 2, depth // 2, (palette.base[0], palette.base[1], palette.base[2], 220)))
    rects.append(img.fill_rect(right.x, right.y - 4, span, 8, palette.shadow))
    rects.append(img.fill_ellipse(right.x + span // 2, right.y + depth // 3, span // 2, depth // 2, (palette.base[0], palette.base[1], palette.base[2], 220)))
    return PartResult("wings", img, union_rects(rects))
