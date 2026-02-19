from __future__ import annotations

from dataclasses import dataclass

from render.image import Image, Rect


@dataclass
class PartResult:
    name: str
    image: Image
    bbox: Rect
