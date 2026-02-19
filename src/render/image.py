from __future__ import annotations

import struct
import zlib
from dataclasses import dataclass
from typing import Iterable

Color = tuple[int, int, int, int]


@dataclass
class Rect:
    x0: int
    y0: int
    x1: int
    y1: int

    def intersects(self, other: "Rect") -> bool:
        return not (
            self.x1 <= other.x0
            or self.x0 >= other.x1
            or self.y1 <= other.y0
            or self.y0 >= other.y1
        )


class Image:
    def __init__(self, width: int, height: int, clear: Color = (0, 0, 0, 0)) -> None:
        self.width = width
        self.height = height
        self.pixels = [list(clear) for _ in range(width * height)]

    def copy(self) -> "Image":
        clone = Image(self.width, self.height)
        clone.pixels = [px[:] for px in self.pixels]
        return clone

    def _idx(self, x: int, y: int) -> int:
        return y * self.width + x

    def blend_pixel(self, x: int, y: int, color: Color) -> None:
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            return
        src_r, src_g, src_b, src_a = color
        if src_a == 0:
            return
        dst_r, dst_g, dst_b, dst_a = self.pixels[self._idx(x, y)]
        a = src_a / 255.0
        ia = 1.0 - a
        out_a = min(255, int(src_a + dst_a * ia))
        out_r = int(src_r * a + dst_r * ia)
        out_g = int(src_g * a + dst_g * ia)
        out_b = int(src_b * a + dst_b * ia)
        self.pixels[self._idx(x, y)] = [out_r, out_g, out_b, out_a]

    def fill_rect(self, x: int, y: int, w: int, h: int, color: Color) -> Rect:
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.width, x + w)
        y1 = min(self.height, y + h)
        for yy in range(y0, y1):
            for xx in range(x0, x1):
                self.blend_pixel(xx, yy, color)
        return Rect(x0, y0, x1, y1)

    def fill_ellipse(self, cx: int, cy: int, rx: int, ry: int, color: Color) -> Rect:
        x0 = max(0, cx - rx)
        y0 = max(0, cy - ry)
        x1 = min(self.width, cx + rx + 1)
        y1 = min(self.height, cy + ry + 1)
        if rx <= 0 or ry <= 0:
            return Rect(x0, y0, x0, y0)
        for yy in range(y0, y1):
            for xx in range(x0, x1):
                nx = (xx - cx) / rx
                ny = (yy - cy) / ry
                if nx * nx + ny * ny <= 1.0:
                    self.blend_pixel(xx, yy, color)
        return Rect(x0, y0, x1, y1)

    def composite(self, other: "Image") -> None:
        if self.width != other.width or self.height != other.height:
            raise ValueError("Image sizes must match for compositing")
        for y in range(self.height):
            for x in range(self.width):
                r, g, b, a = other.pixels[other._idx(x, y)]
                self.blend_pixel(x, y, (r, g, b, a))


    def write_jpeg(self, path: str, quality: int = 92) -> None:
        try:
            from PIL import Image as PILImage
        except ImportError as exc:
            raise RuntimeError(
                "JPEG export requires Pillow. Install dependencies with: pip install -r requirements.txt"
            ) from exc

        data = bytearray()
        for r, g, b, _a in self.pixels:
            data.extend((r, g, b))
        pil_img = PILImage.frombytes("RGB", (self.width, self.height), bytes(data))
        pil_img.save(path, format="JPEG", quality=quality)
    def write_png(self, path: str) -> None:
        raw = bytearray()
        for y in range(self.height):
            raw.append(0)
            row = self.pixels[y * self.width : (y + 1) * self.width]
            for r, g, b, a in row:
                raw.extend((r, g, b, a))
        compressed = zlib.compress(bytes(raw), level=9)

        def chunk(chunk_type: bytes, data: bytes) -> bytes:
            crc = zlib.crc32(chunk_type)
            crc = zlib.crc32(data, crc)
            return (
                struct.pack(">I", len(data))
                + chunk_type
                + data
                + struct.pack(">I", crc & 0xFFFFFFFF)
            )

        ihdr = struct.pack(">IIBBBBB", self.width, self.height, 8, 6, 0, 0, 0)
        png = bytearray(b"\x89PNG\r\n\x1a\n")
        png.extend(chunk(b"IHDR", ihdr))
        png.extend(chunk(b"IDAT", compressed))
        png.extend(chunk(b"IEND", b""))
        with open(path, "wb") as f:
            f.write(png)


def union_rects(rects: Iterable[Rect]) -> Rect:
    xs0 = [r.x0 for r in rects]
    ys0 = [r.y0 for r in rects]
    xs1 = [r.x1 for r in rects]
    ys1 = [r.y1 for r in rects]
    if not xs0:
        return Rect(0, 0, 0, 0)
    return Rect(min(xs0), min(ys0), max(xs1), max(ys1))
