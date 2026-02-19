from __future__ import annotations

from generator.palette import Palette
from generator.seed import rng_for_part
from generator.skeleton import DragonSkeleton
from render.image import Image, Rect, union_rects

from .common import PartResult


def generate(seed: int, skeleton: DragonSkeleton, palette: Palette) -> PartResult:
    rng = rng_for_part(seed, "legs")
    img = Image(skeleton.width, skeleton.height)
    rects: list[Rect] = []
    leg_h = max(20, min(46, int(skeleton.torso_bounds[1] * 1.4) + rng.randint(-5, 5)))
    leg_w = max(8, min(16, int(skeleton.torso_bounds[0] * 0.18)))
    for anchor in (skeleton.left_leg_base, skeleton.right_leg_base):
        rects.append(img.fill_rect(anchor.x - leg_w // 2, anchor.y, leg_w, leg_h, palette.base))
        rects.append(img.fill_rect(anchor.x - leg_w, anchor.y + leg_h - 4, leg_w * 2, 4, palette.shadow))
        rects.append(img.fill_rect(anchor.x - leg_w // 2, anchor.y + leg_h // 3, leg_w, 2, palette.highlight))
    return PartResult("legs", img, union_rects(rects))
