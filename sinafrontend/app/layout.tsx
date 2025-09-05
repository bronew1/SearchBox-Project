import "./globals.css";

export const metadata = {
  title: "Sina Pırlanta CXP",
  description: "Müşteri Deneyim Platformu",
  icons: {
    icon: "/vercel.svg", // public/vercel.svg
  },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="tr">
      <body>{children}</body>
    </html>
  );
}
