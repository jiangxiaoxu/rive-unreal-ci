"""Package a Win64 Rive Unreal source plugin with freshly built runtime libraries."""

import argparse
import json
import re
import sys
import zipfile
from pathlib import Path


ROOT_FILES = ("Rive.uplugin", "LICENSE", "README.md")
ROOT_DIRS = ("Config", "Content", "Resources", "Shaders", "Source")
LIBRARIES = (
    "rive",
    "rive_decoders",
    "rive_harfbuzz",
    "rive_pls_renderer",
    "rive_sheenbidi",
    "rive_yoga",
    "rive_libpng",
    "rive_libjpeg",
    "rive_libwebp",
    "rive_miniaudio",
    "luau_vm",
)


def validate_build(root: Path) -> None:
    libraries = root / "Source/ThirdParty/RiveLibrary/Libraries/Win64"
    missing = []
    invalid = []
    for name in LIBRARIES:
        for suffix in ("", "_d"):
            path = libraries / f"{name}{suffix}.lib"
            if not path.is_file():
                missing.append(str(path))
            else:
                with path.open("rb") as stream:
                    if stream.read(8) != b"!<arch>\n":
                        invalid.append(str(path))
    required = (
        root / "Source/ThirdParty/RiveLibrary/Includes/rive/file.hpp",
        root / "Shaders/Private/Rive/Generated",
    )
    missing.extend(str(path) for path in required if not path.exists())
    generated = root / "Shaders/Private/Rive/Generated"
    if generated.is_dir() and not any(generated.glob("*.ush")):
        missing.append(f"{generated}/*.ush")
    if missing or invalid:
        raise ValueError(
            "Invalid Win64 build outputs:\n"
            + "\n".join(missing)
            + ("\nNon-COFF libraries: " + ", ".join(invalid) if invalid else "")
        )


def package(root: Path, output: Path, version: str) -> None:
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", version):
        raise ValueError(f"Invalid release tag: {version!r}")
    validate_build(root)
    descriptor = json.loads((root / "Rive.uplugin").read_text(encoding="utf-8-sig"))
    descriptor["VersionName"] = version
    for module in descriptor["Modules"]:
        module["PlatformAllowList"] = ["Win64"]

    files = [root / name for name in ROOT_FILES if name != "Rive.uplugin"]
    for directory in ROOT_DIRS:
        files.extend(path for path in (root / directory).rglob("*") if path.is_file())
    files.sort()
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        archive.writestr("Rive/Rive.uplugin", json.dumps(descriptor, indent=4) + "\n")
        for path in files:
            relative = path.relative_to(root)
            if relative.parts[:4] == ("Source", "ThirdParty", "RiveLibrary", "Libraries"):
                if relative.parts[4] != "Win64":
                    continue
            archive.write(path, (Path("Rive") / relative).as_posix())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True, help="Upstream release tag")
    parser.add_argument("--output", required=True, type=Path, help="Output zip path")
    parser.add_argument("--plugin-root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    package(args.plugin_root.resolve(), args.output.resolve(), args.version)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, IndexError) as error:
        print(error, file=sys.stderr)
        sys.exit(1)
