# Procedural Dragon Generator

This repository contains a minimal deterministic dragon generator that builds a single 32-bit RGBA PNG from seeded procedural parts.

## Project structure

- `src/main.py` – CLI entrypoint.
- `src/generator/` – high-level generation flow, skeleton model, palette, and seed derivation.
- `src/parts/` – part generators (`head`, `neck`, `torso`, `wings`, `legs`, `tail`).
- `src/render/` – RGBA image primitives and compositing/assembly order.

## Generation flow

1. Parse CLI arguments (`--seed`, `--width`, `--height`, `--out`, optional `--debug-parts-dir`).
2. Build a shared `DragonSkeleton` containing joint anchors and orientation metadata.
3. Create a single palette object and pass it to all part generators.
4. Generate each part procedurally using deterministic per-part seeds derived from the global seed.
5. Run fit/collision guards to keep dimensions proportional and prevent legs/wings from occupying forbidden torso core pixels.
6. Assemble layers in a fixed order for stable visual stacking.
7. Export a final PNG and optional debug part layers.

## Determinism

- Global seed controls the full dragon.
- Per-part seeds are derived with `sha256(global_seed + part_name)` and converted to integers.
- Fit retries (if needed) use deterministic seed offsets, so generation remains reproducible.

## Run

```bash
python3 src/main.py --seed 42 --width 512 --height 384 --out dragon.png
```

Optional debug layers:

```bash
python3 src/main.py --seed 42 --width 512 --height 384 --out dragon.png --debug-parts-dir debug_parts
```
