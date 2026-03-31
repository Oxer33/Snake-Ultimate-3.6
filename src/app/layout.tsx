/**
 * ============================================
 * SNAKE ULTIMATE 3.6 - Layout Principale
 * ============================================
 * Layout root dell'applicazione Next.js.
 * Configura:
 * - Metadata SEO
 * - Font
 * - Stili globali
 * - Viewport per responsive
 */

import type { Metadata, Viewport } from 'next';
import './globals.css';

/**
 * Metadata per SEO e social sharing
 */
export const metadata: Metadata = {
  title: {
    default: 'Snake Ultimate 3.6 - Il Gioco Snake Più Bello Mai Creato',
    template: '%s | Snake Ultimate',
  },
  description: 'Gioca al miglior gioco Snake mai creato! Grafica moderna, modalità multiple, effetti visivi straordinari. Disponibile su desktop e mobile.',
  keywords: ['snake', 'gioco', 'snake game', 'retro', 'arcade', 'browser game', 'mobile game'],
  authors: [{ name: 'Snake Ultimate Team' }],
  creator: 'Snake Ultimate',
  publisher: 'Snake Ultimate',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://snake-ultimate.vercel.app'),
  openGraph: {
    title: 'Snake Ultimate 3.6',
    description: 'Il gioco Snake più bello mai creato!',
    url: 'https://snake-ultimate.vercel.app',
    siteName: 'Snake Ultimate',
    locale: 'it_IT',
    type: 'website',
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  icons: {
    icon: '/favicon.ico',
    shortcut: '/favicon-16x16.png',
    apple: '/apple-touch-icon.png',
  },
};

/**
 * Configurazione viewport per mobile
 */
export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: [
    { media: '(prefers-color-scheme: dark)', color: '#010409' },
  ],
};

/**
 * Componente Root Layout
 */
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="it" className="dark">
      <body className="antialiased bg-snake-dark-400 text-white">
        {children}
      </body>
    </html>
  );
}
