from __future__ import annotations

from generator.palette import Palette
from generator.seed import rng_for_part
from generator.skeleton import DragonSkeleton
from render.image import Rect, Image, union_rects

from .common import PartResult


def generate(seed: int, skeleton: DragonSkeleton, palette: Palette) -> PartResult:
    rng = rng_for_part(seed, "head")
    img = Image(skeleton.width, skeleton.height)
    base = skeleton.head_base
    head_w = rng.randint(24, 34)
    head_h = rng.randint(16, 24)
    r1 = img.fill_ellipse(base.x, base.y, head_w // 2, head_h // 2, palette.base)
    snout = img.fill_rect(base.x + head_w // 4, base.y - head_h // 5, head_w // 2, head_h // 3, palette.highlight)
    horn1 = img.fill_rect(base.x - 3, base.y - head_h // 2 - 6, 3, 7, palette.horn)
    horn2 = img.fill_rect(base.x + 4, base.y - head_h // 2 - 5, 3, 6, palette.horn)
    eye = img.fill_rect(base.x + head_w // 5, base.y - 2, 2, 2, palette.eye)
    jaw = img.fill_rect(base.x + 2, base.y + head_h // 5, head_w // 2, 3, palette.shadow)
    return PartResult("head", img, union_rects([r1, snout, horn1, horn2, eye, jaw]))
