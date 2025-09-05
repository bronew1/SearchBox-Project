import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",   // ✅ static export aktif
  images: {
    unoptimized: true // ✅ Render'da image optimizer çalışmaz, bu ayarı ekle
  }
};

export default nextConfig;
