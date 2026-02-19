from __future__ import annotations

import argparse
import os

from generator.dragon import build_dragon


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Procedural dragon generator")
    p.add_argument("--seed", type=int, required=True, help="Global seed")
    p.add_argument("--width", type=int, default=512, help="Output width")
    p.add_argument("--height", type=int, default=384, help="Output height")
    p.add_argument("--out", type=str, default="dragon.png", help="PNG output path")
    p.add_argument(
        "--debug-parts-dir",
        type=str,
        default=None,
        help="Optional directory for per-part debug PNG layers",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    dragon = build_dragon(args.seed, args.width, args.height)
    out_lower = args.out.lower()
    if out_lower.endswith((".jpg", ".jpeg")):
        dragon.image.write_jpeg(args.out)
    else:
        dragon.image.write_png(args.out)

    if args.debug_parts_dir:
        os.makedirs(args.debug_parts_dir, exist_ok=True)
        for name, image in dragon.debug_layers.items():
            image.write_png(os.path.join(args.debug_parts_dir, f"{name}.png"))


if __name__ == "__main__":
    main()
