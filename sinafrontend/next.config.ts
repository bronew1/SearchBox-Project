import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // Eğer auth gibi dinamik route'ların static export ile problemi olmasın istiyorsan
  experimental: {
    typedRoutes: true,
  },
};

export default nextConfig;
