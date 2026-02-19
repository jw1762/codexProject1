from __future__ import annotations

from generator.palette import Palette
from generator.seed import rng_for_part
from generator.skeleton import DragonSkeleton
from render.image import Image, Rect, union_rects

from .common import PartResult


def generate(seed: int, skeleton: DragonSkeleton, palette: Palette) -> PartResult:
    rng = rng_for_part(seed, "torso")
    img = Image(skeleton.width, skeleton.height)
    torso_w, torso_h = skeleton.torso_bounds
    torso_w += rng.randint(-6, 6)
    torso_h += rng.randint(-4, 4)
    cx, cy = skeleton.torso_center.x, skeleton.torso_center.y
    r1 = img.fill_ellipse(cx, cy, torso_w // 2, torso_h // 2, palette.base)
    r2 = img.fill_ellipse(cx + torso_w // 6, cy - torso_h // 6, torso_w // 3, torso_h // 3, palette.highlight)
    ridge = img.fill_rect(cx - torso_w // 4, cy - torso_h // 2 - 4, torso_w // 2, 6, palette.shadow)
    return PartResult("torso", img, union_rects([r1, r2, ridge]))
