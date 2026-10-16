from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path

from PIL import Image, ImageDraw


CAT_ID = "2324219253546966734"
BUDGIE_ID = "4784028547053439212"


def edge_connected_background(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    width, height = image.size
    pixels = image.load()
    visited: set[tuple[int, int]] = set()
    queue: deque[tuple[int, int]] = deque()

    for x in range(width):
        queue.append((x, 0))
        queue.append((x, height - 1))
    for y in range(height):
        queue.append((0, y))
        queue.append((width - 1, y))

    def near_white(x: int, y: int) -> bool:
        r, g, b, a = pixels[x, y]
        return a > 0 and r > 245 and g > 245 and b > 245

    while queue:
        x, y = queue.popleft()
        if (x, y) in visited or not near_white(x, y):
            continue
        visited.add((x, y))
        pixels[x, y] = (pixels[x, y][0], pixels[x, y][1], pixels[x, y][2], 0)
        if x > 0:
            queue.append((x - 1, y))
        if x < width - 1:
            queue.append((x + 1, y))
        if y > 0:
            queue.append((x, y - 1))
        if y < height - 1:
            queue.append((x, y + 1))

    return image


def fit_image(image: Image.Image, max_size: int = 1024) -> Image.Image:
    image = image.convert("RGBA")
    image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    return image


def create_pat_sticker(path: Path) -> None:
    size = 474
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    outline = (25, 25, 32, 255)
    white = (250, 250, 250, 255)
    gray = (214, 215, 221, 255)
    blush = (244, 132, 145, 255)
    skin = (255, 214, 182, 255)

    draw.ellipse((42, 88, 431, 414), fill=white, outline=outline, width=6)
    draw.pieslice((44, 260, 429, 430), 0, 180, fill=gray)
    draw.arc((44, 88, 431, 414), 0, 360, fill=outline, width=6)

    draw.arc((108, 188, 190, 260), 198, 342, fill=outline, width=8)
    draw.arc((284, 188, 366, 260), 198, 342, fill=outline, width=8)
    draw.ellipse((106, 246, 173, 286), fill=blush)
    draw.ellipse((301, 246, 368, 286), fill=blush)
    draw.arc((207, 244, 268, 302), 20, 160, fill=outline, width=7)
    draw.arc((219, 286, 258, 316), 0, 180, fill=outline, width=6)

    draw.line((42, 275, 2, 265), fill=outline, width=5)
    draw.line((42, 300, 0, 304), fill=outline, width=5)
    draw.line((431, 275, 472, 265), fill=outline, width=5)
    draw.line((431, 300, 474, 304), fill=outline, width=5)

    hand = [(110, 139), (132, 86), (170, 52), (204, 37), (234, 38), (259, 62),
            (282, 37), (311, 31), (330, 49), (323, 78), (355, 60), (386, 63),
            (394, 86), (370, 112), (342, 137), (314, 152), (273, 167),
            (226, 171), (179, 164), (143, 154)]
    draw.polygon(hand, fill=skin, outline=outline)
    draw.line((168, 85, 149, 127), fill=outline, width=5)
    draw.line((232, 66, 220, 126), fill=outline, width=5)
    draw.line((302, 66, 284, 126), fill=outline, width=5)
    draw.line((355, 83, 330, 126), fill=outline, width=5)

    image.save(path, format="PNG", optimize=True)


def find_source(source_dir: Path, marker: str) -> Path:
    matches = [p for p in source_dir.iterdir() if marker in p.name and p.is_file()]
    if not matches:
        raise FileNotFoundError(f"找不到包含 MsgID={marker} 的图片")
    return matches[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    cat_path = find_source(args.source_dir, CAT_ID)
    budgie_path = find_source(args.source_dir, BUDGIE_ID)
    cat_out = args.out / "cat.imageset" / "cat.png"
    budgie_out = args.out / "budgie.imageset" / "budgie.png"
    sticker_out = args.out / "pat-sticker.imageset" / "pat-sticker.png"
    cat_out.parent.mkdir(parents=True, exist_ok=True)
    budgie_out.parent.mkdir(parents=True, exist_ok=True)
    sticker_out.parent.mkdir(parents=True, exist_ok=True)

    edge_connected_background(Image.open(cat_path)).save(cat_out, format="PNG", optimize=True)
    edge_connected_background(Image.open(budgie_path)).save(budgie_out, format="PNG", optimize=True)
    create_pat_sticker(sticker_out)
    print(f"cat={cat_path}")
    print(f"budgie={budgie_path}")
    print(f"sticker={sticker_out} (本地绘制的摸头表情，参照用户提供图片)")


if __name__ == "__main__":
    main()
