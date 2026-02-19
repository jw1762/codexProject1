from __future__ import annotations

import hashlib
import random


def derive_seed(global_seed: int, part_name: str) -> int:
    material = f"{global_seed}:{part_name}".encode("utf-8")
    digest = hashlib.sha256(material).digest()
    return int.from_bytes(digest[:8], "big", signed=False)


def rng_for_part(global_seed: int, part_name: str) -> random.Random:
    return random.Random(derive_seed(global_seed, part_name))
