from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from generator.palette import Palette
from generator.skeleton import DragonSkeleton, build_skeleton
from parts import head, legs, neck, tail, torso, wings
from parts.common import PartResult
from render.assemble import FitError, compose_layers, guard_part_fit, order_parts
from render.image import Image


@dataclass
class DragonBuild:
    image: Image
    debug_layers: dict[str, Image]


def _build_part_with_guards(
    seed: int,
    name: str,
    skeleton: DragonSkeleton,
    palette: Palette,
    generator: Callable[[int, DragonSkeleton, Palette], PartResult],
    *,
    attempts: int = 4,
) -> PartResult:
    last_error: Exception | None = None
    for attempt in range(attempts):
        part_seed = seed + (attempt * 9973)
        part = generator(part_seed, skeleton, palette)
        try:
            guard_part_fit(skeleton, part)
            return part
        except FitError as exc:
            last_error = exc
    raise FitError(f"Unable to fit part '{name}' after {attempts} attempts: {last_error}")


def build_dragon(seed: int, width: int, height: int) -> DragonBuild:
    skeleton = build_skeleton(width, height)
    palette = Palette.from_seed(seed)

    torso_part = torso.generate(seed, skeleton, palette)
    neck_part = _build_part_with_guards(seed, "neck", skeleton, palette, neck.generate)
    head_part = _build_part_with_guards(seed, "head", skeleton, palette, head.generate)
    wings_part = _build_part_with_guards(seed, "wings", skeleton, palette, wings.generate)
    legs_part = _build_part_with_guards(seed, "legs", skeleton, palette, legs.generate)
    tail_part = _build_part_with_guards(seed, "tail", skeleton, palette, tail.generate)

    parts_map: dict[str, PartResult] = {
        "torso": torso_part,
        "neck": neck_part,
        "head": head_part,
        "legs": legs_part,
        "tail": tail_part,
        "wings_back": wings_part,
        "wings_front": wings_part,
    }

    ordered = order_parts(parts_map)
    final_image = compose_layers(width, height, ordered)
    debug = {name: part.image for name, part in parts_map.items() if not name.startswith("wings_")}
    debug["wings"] = wings_part.image

    return DragonBuild(final_image, debug)
