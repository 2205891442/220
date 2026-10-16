from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSETS = {
    "cat": ROOT / "DesktopPets/Resources.xcassets/cat.imageset/cat.png",
    "budgie": ROOT / "DesktopPets/Resources.xcassets/budgie.imageset/budgie.png",
    "pat-sticker": ROOT / "DesktopPets/Resources.xcassets/pat-sticker.imageset/pat-sticker.png",
}
REQUIRED_SYMBOLS = {
    "PetView.swift": ["TimelineView", "pausedUntil", "PatStickerView", "accessibilityLabel"],
    "PetStageView.swift": ["LinearGradient", "PetView", "safeAreaInsets"],
    "DesktopPetsApp.swift": ["@main", "WindowGroup"],
}


def main() -> int:
    for name, path in ASSETS.items():
        if not path.is_file():
            raise SystemExit(f"missing asset: {path}")
        image = Image.open(path).convert("RGBA")
        if image.width < 1 or image.height < 1 or image.width > 1024 or image.height > 1024:
            raise SystemExit(f"invalid size for {name}: {image.size}")
        if image.getchannel("A").getbbox() is None:
            raise SystemExit(f"asset is fully transparent: {name}")
        if name in {"cat", "budgie"}:
            corners = [image.getpixel((0, 0)), image.getpixel((image.width - 1, 0)), image.getpixel((0, image.height - 1)), image.getpixel((image.width - 1, image.height - 1))]
            if any(pixel[3] != 0 for pixel in corners):
                raise SystemExit(f"pet background is not transparent: {name}")
        print(f"asset ok: {name} {image.size} RGBA")

    for filename, symbols in REQUIRED_SYMBOLS.items():
        path = ROOT / "DesktopPets" / filename
        source = path.read_text(encoding="utf-8")
        missing = [symbol for symbol in symbols if symbol not in source]
        if missing:
            raise SystemExit(f"missing symbols in {filename}: {', '.join(missing)}")
        print(f"source ok: {filename}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
