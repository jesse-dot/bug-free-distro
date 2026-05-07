# DistroForge MVP

This repository contains a minimum viable product for **DistroForge**, a web app that accepts Linux distribution build preferences and generates a shell build script for ISO creation workflows.

## Directory Structure

```text
.
├── backend
│   ├── build_logic.py
│   ├── main.py
│   ├── scripts/build_iso.sh.template
│   ├── tests
│   │   ├── test_api.py
│   │   └── test_build_logic.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend
│   ├── app
│   │   ├── globals.css
│   │   ├── layout.jsx
│   │   └── page.jsx
│   ├── next.config.mjs
│   ├── package.json
│   ├── postcss.config.js
│   └── tailwind.config.js
└── docker-compose.yml
```

## Part 1: Frontend (Next.js + Tailwind)

The frontend dashboard includes:
- Base OS dropdown (Debian, Ubuntu, Arch)
- Package manager field automatically locked to the selected base OS
- Software checklist (Firefox, VLC, VS Code, GIMP, curl, git)
- Upload inputs for boot logo and desktop wallpaper
- **Build My OS** action that posts `multipart/form-data` to `http://localhost:8000/api/build`

## Part 2: Backend (FastAPI)

### Endpoint
`POST /api/build`
- Receives `config` JSON in form-data plus optional files:
  - `boot_logo`
  - `wallpaper`
- Validates base OS and package manager pairing.
- Saves uploads to a per-build directory.
- Renders an executable build script from `backend/scripts/build_iso.sh.template`.

### Example API payload

```json
{
  "base_os": "debian",
  "package_manager": "apt",
  "software": ["firefox", "vlc"]
}
```

## Part 3: Build Engine Logic (Shell/Docker)

`backend/scripts/build_iso.sh.template` demonstrates how build parameters are consumed to:
1. Prepare build dependencies (`live-build` or `archiso`)
2. Bootstrap/configure a live build root
3. Install selected packages in chroot
4. Inject branding assets (boot logo/wallpaper)
5. Produce an ISO artifact path in the output directory

This is intentionally an MVP template and can be expanded into full distro-specific workflows.

## Local Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`, backend on `http://localhost:8000`.

### Docker Compose

```bash
docker compose up --build
```

## Tests

```bash
cd backend
pytest -q
```
