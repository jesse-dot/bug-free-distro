import json
from io import BytesIO

from fastapi.testclient import TestClient

import main


client = TestClient(main.app)


def test_build_endpoint_generates_script(tmp_path, monkeypatch):
    monkeypatch.setattr(main, 'RUNS_DIR', tmp_path / 'runs')

    config = {'base_os': 'debian', 'package_manager': 'apt', 'software': ['firefox']}
    response = client.post(
        '/api/build',
        data={'config': json.dumps(config)},
        files={
            'boot_logo': ('logo.png', BytesIO(b'123'), 'image/png'),
            'wallpaper': ('wall.png', BytesIO(b'456'), 'image/png'),
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert 'build_id' in payload
    assert payload['script_path'].endswith('build_iso.sh')


def test_build_endpoint_rejects_invalid_package_manager(tmp_path, monkeypatch):
    monkeypatch.setattr(main, 'RUNS_DIR', tmp_path / 'runs')

    config = {'base_os': 'arch', 'package_manager': 'apt', 'software': []}
    response = client.post('/api/build', data={'config': json.dumps(config)})

    assert response.status_code == 400
    assert 'package_manager must be' in response.json()['detail']
