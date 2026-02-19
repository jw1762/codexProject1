from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .seed import rng_for_part

Color = tuple[int, int, int, int]


PALETTE_FAMILIES = {
    "emerald": ((44, 122, 84), (62, 161, 111), (26, 74, 51)),
    "ember": ((155, 74, 47), (197, 111, 73), (97, 42, 29)),
    "azure": ((63, 93, 161), (84, 125, 202), (37, 56, 105)),
    "violet": ((108, 74, 148), (146, 105, 191), (68, 45, 99)),
}


@dataclass(frozen=True)
class Palette:
    base: Color
    highlight: Color
    shadow: Color
    horn: Color
    eye: Color

    @classmethod
    def from_seed(cls, seed: int) -> "Palette":
        rng = rng_for_part(seed, "palette")
        family_name = rng.choice(sorted(PALETTE_FAMILIES.keys()))
        base_rgb, hi_rgb, sh_rgb = PALETTE_FAMILIES[family_name]
        alpha = 255
        horn = (220, 210, 188, alpha)
        eye = (255, 232, 126, alpha)
        return cls(
            base=(*base_rgb, alpha),
            highlight=(*hi_rgb, alpha),
            shadow=(*sh_rgb, alpha),
            horn=horn,
            eye=eye,
        )

    def as_debug_map(self) -> Dict[str, Color]:
        return {
            "base": self.base,
            "highlight": self.highlight,
            "shadow": self.shadow,
            "horn": self.horn,
            "eye": self.eye,
        }
