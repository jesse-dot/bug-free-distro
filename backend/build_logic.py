from __future__ import annotations

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class BuildConfig(BaseModel):
    base_os: str = Field(pattern="^(debian|ubuntu|arch)$")
    package_manager: str = Field(pattern="^(apt|pacman)$")
    software: list[str] = Field(default_factory=list)


def validate_package_manager(config: BuildConfig) -> None:
    expected = "pacman" if config.base_os == "arch" else "apt"
    if config.package_manager != expected:
        raise ValueError(f"package_manager must be '{expected}' for base_os '{config.base_os}'")


def render_build_script(
    config: BuildConfig,
    build_root: Path,
    template_path: Path,
    boot_logo_path: Optional[Path] = None,
    wallpaper_path: Optional[Path] = None,
) -> Path:
    validate_package_manager(config)

    build_dir = build_root / "workdir"
    output_dir = build_root / "output"
    build_root.mkdir(parents=True, exist_ok=True)

    template = template_path.read_text(encoding="utf-8")
    replacements = {
        "{{BASE_OS}}": config.base_os,
        "{{PACKAGE_MANAGER}}": config.package_manager,
        "{{PACKAGES}}": " ".join(config.software),
        "{{BOOT_LOGO}}": str(boot_logo_path or ""),
        "{{WALLPAPER}}": str(wallpaper_path or ""),
        "{{BUILD_DIR}}": str(build_dir),
        "{{OUTPUT_DIR}}": str(output_dir),
    }

    for token, value in replacements.items():
        template = template.replace(token, value)

    generated_script = build_root / "build_iso.sh"
    generated_script.write_text(template, encoding="utf-8")
    generated_script.chmod(0o755)
    return generated_script
