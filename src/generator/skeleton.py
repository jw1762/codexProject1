from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Anchor:
    x: int
    y: int
    angle_deg: float


@dataclass(frozen=True)
class DragonSkeleton:
    width: int
    height: int
    torso_center: Anchor
    neck_base: Anchor
    head_base: Anchor
    left_wing_base: Anchor
    right_wing_base: Anchor
    left_leg_base: Anchor
    right_leg_base: Anchor
    tail_base: Anchor
    torso_bounds: tuple[int, int]
    forbidden_torso_region: tuple[int, int, int, int]



def build_skeleton(width: int, height: int) -> DragonSkeleton:
    cx = width // 2
    cy = int(height * 0.58)
    torso_w = max(40, int(width * 0.26))
    torso_h = max(28, int(height * 0.19))

    return DragonSkeleton(
        width=width,
        height=height,
        torso_center=Anchor(cx, cy, 0.0),
        neck_base=Anchor(cx + torso_w // 2 - 8, cy - torso_h // 3, -25.0),
        head_base=Anchor(cx + torso_w // 2 + 24, cy - torso_h // 2 - 8, -8.0),
        left_wing_base=Anchor(cx - torso_w // 3, cy - torso_h // 2, -125.0),
        right_wing_base=Anchor(cx + torso_w // 4, cy - torso_h // 2, -55.0),
        left_leg_base=Anchor(cx - torso_w // 4, cy + torso_h // 3, 95.0),
        right_leg_base=Anchor(cx + torso_w // 5, cy + torso_h // 3, 85.0),
        tail_base=Anchor(cx - torso_w // 2 + 3, cy + torso_h // 6, 185.0),
        torso_bounds=(torso_w, torso_h),
        forbidden_torso_region=(cx - torso_w // 8, cy - torso_h // 4, torso_w // 3, torso_h // 2),
    )
