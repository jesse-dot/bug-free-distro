from pathlib import Path

import pytest

from build_logic import BuildConfig, render_build_script, validate_package_manager


@pytest.mark.parametrize(
    'base_os,package_manager',
    [
        ('debian', 'apt'),
        ('ubuntu', 'apt'),
        ('arch', 'pacman'),
    ],
)
def test_validate_package_manager_accepts_supported_pairs(base_os: str, package_manager: str) -> None:
    validate_package_manager(BuildConfig(base_os=base_os, package_manager=package_manager, software=[]))


def test_validate_package_manager_rejects_invalid_pairing() -> None:
    with pytest.raises(ValueError):
        validate_package_manager(BuildConfig(base_os='arch', package_manager='apt', software=[]))


def test_render_build_script_replaces_tokens(tmp_path: Path) -> None:
    template_path = tmp_path / 'template.sh'
    template_path.write_text(
        'BASE={{BASE_OS}} PM={{PACKAGE_MANAGER}} PKGS={{PACKAGES}} LOGO={{BOOT_LOGO}} WALL={{WALLPAPER}}',
        encoding='utf-8',
    )

    script = render_build_script(
        config=BuildConfig(base_os='debian', package_manager='apt', software=['firefox', 'vlc']),
        build_root=tmp_path / 'run',
        template_path=template_path,
        boot_logo_path=tmp_path / 'logo.png',
        wallpaper_path=tmp_path / 'wallpaper.png',
    )

    content = script.read_text(encoding='utf-8')
    assert 'BASE=debian' in content
    assert 'PM=apt' in content
    assert 'PKGS=firefox vlc' in content
    assert 'logo.png' in content
    assert 'wallpaper.png' in content
