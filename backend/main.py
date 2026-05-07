from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from build_logic import BuildConfig, render_build_script

app = FastAPI(title="DistroForge API")

BASE_DIR = Path(__file__).resolve().parent
RUNS_DIR = BASE_DIR / "build_runs"
TEMPLATE_PATH = BASE_DIR / "scripts" / "build_iso.sh.template"


@app.get('/health')
def health() -> dict[str, str]:
    return {'status': 'ok'}


@app.post('/api/build')
async def build_os(
    config: str = Form(...),
    boot_logo: UploadFile | None = File(default=None),
    wallpaper: UploadFile | None = File(default=None),
) -> dict[str, str | list[str]]:
    try:
        config_data = BuildConfig.model_validate(json.loads(config))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid config payload: {exc}") from exc

    build_id = str(uuid.uuid4())
    build_dir = RUNS_DIR / build_id
    assets_dir = build_dir / "assets"
    assets_dir.mkdir(parents=True, exist_ok=True)

    boot_logo_path = None
    wallpaper_path = None

    if boot_logo is not None:
        boot_logo_path = assets_dir / boot_logo.filename
        with boot_logo_path.open('wb') as destination:
            shutil.copyfileobj(boot_logo.file, destination)

    if wallpaper is not None:
        wallpaper_path = assets_dir / wallpaper.filename
        with wallpaper_path.open('wb') as destination:
            shutil.copyfileobj(wallpaper.file, destination)

    try:
        script_path = render_build_script(
            config=config_data,
            build_root=build_dir,
            template_path=TEMPLATE_PATH,
            boot_logo_path=boot_logo_path,
            wallpaper_path=wallpaper_path,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "build_id": build_id,
        "script_path": str(script_path),
        "next_step": "Run the generated script inside a privileged Docker build container.",
    }
