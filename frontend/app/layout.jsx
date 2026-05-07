import './globals.css';

export const metadata = {
  title: 'DistroForge MVP',
  description: 'Build a custom Linux distro ISO.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
