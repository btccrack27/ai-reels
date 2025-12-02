import type { Metadata } from 'next';
import '../globals.css';

export const metadata: Metadata = {
  title: 'AI Reels Generator',
  description: 'Generate engaging video reels using AI',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
