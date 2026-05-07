'use client';

import { useMemo, useState } from 'react';

const BASE_OS_OPTIONS = [
  { value: 'debian', label: 'Debian', packageManager: 'apt' },
  { value: 'ubuntu', label: 'Ubuntu', packageManager: 'apt' },
  { value: 'arch', label: 'Arch Linux', packageManager: 'pacman' },
];

const SOFTWARE_OPTIONS = [
  'firefox',
  'vlc',
  'code',
  'gimp',
  'curl',
  'git',
];
const API_URL = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';

export default function Dashboard() {
  const [baseOs, setBaseOs] = useState('debian');
  const packageManager = useMemo(
    () => BASE_OS_OPTIONS.find((option) => option.value === baseOs)?.packageManager ?? 'apt',
    [baseOs],
  );
  const [software, setSoftware] = useState(['firefox']);
  const [bootLogo, setBootLogo] = useState(null);
  const [wallpaper, setWallpaper] = useState(null);
  const [status, setStatus] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSoftwareToggle = (pkg) => {
    setSoftware((current) =>
      current.includes(pkg) ? current.filter((entry) => entry !== pkg) : [...current, pkg],
    );
  };

  const onSubmit = async () => {
    setLoading(true);
    setStatus('Submitting build request...');

    const config = {
      base_os: baseOs,
      package_manager: packageManager,
      software,
    };

    const formData = new FormData();
    formData.append('config', JSON.stringify(config));
    if (bootLogo) formData.append('boot_logo', bootLogo);
    if (wallpaper) formData.append('wallpaper', wallpaper);

    try {
      const response = await fetch(`${API_URL}/api/build`, {
        method: 'POST',
        body: formData,
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || 'Build request failed');
      }

      setStatus(`Build queued: ${payload.build_id}`);
    } catch (error) {
      setStatus(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen p-4 sm:p-8">
      <section className="mx-auto max-w-3xl rounded-xl border border-slate-800 bg-slate-900 p-6 shadow-lg">
        <h1 className="text-2xl font-bold">DistroForge</h1>
        <p className="mt-2 text-sm text-slate-300">Design your Linux ISO and trigger a build.</p>

        <div className="mt-6 grid gap-6 sm:grid-cols-2">
          <label className="text-sm">
            <span className="mb-2 block font-medium">Base OS</span>
            <select
              className="w-full rounded border border-slate-700 bg-slate-950 p-2"
              value={baseOs}
              onChange={(event) => setBaseOs(event.target.value)}
            >
              {BASE_OS_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>

          <label className="text-sm">
            <span className="mb-2 block font-medium">Package Manager</span>
            <input
              readOnly
              value={packageManager}
              className="w-full rounded border border-slate-700 bg-slate-800 p-2 text-slate-300"
            />
          </label>
        </div>

        <div className="mt-6">
          <p className="mb-2 text-sm font-medium">Software Selection</p>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
            {SOFTWARE_OPTIONS.map((pkg) => (
              <label key={pkg} className="flex items-center gap-2 rounded border border-slate-700 p-2 text-sm">
                <input
                  type="checkbox"
                  checked={software.includes(pkg)}
                  onChange={() => handleSoftwareToggle(pkg)}
                />
                {pkg}
              </label>
            ))}
          </div>
        </div>

        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          <label className="text-sm">
            <span className="mb-2 block font-medium">Custom Boot Logo</span>
            <input
              type="file"
              accept="image/*"
              className="w-full rounded border border-slate-700 bg-slate-950 p-2"
              onChange={(event) => setBootLogo(event.target.files?.[0] ?? null)}
            />
          </label>

          <label className="text-sm">
            <span className="mb-2 block font-medium">Desktop Background</span>
            <input
              type="file"
              accept="image/*"
              className="w-full rounded border border-slate-700 bg-slate-950 p-2"
              onChange={(event) => setWallpaper(event.target.files?.[0] ?? null)}
            />
          </label>
        </div>

        <button
          type="button"
          disabled={loading}
          onClick={onSubmit}
          className="mt-6 rounded bg-indigo-500 px-4 py-2 font-semibold text-white disabled:opacity-60"
        >
          {loading ? 'Building...' : 'Build My OS'}
        </button>

        {status ? <p className="mt-4 text-sm text-slate-200">{status}</p> : null}
      </section>
    </main>
  );
}
