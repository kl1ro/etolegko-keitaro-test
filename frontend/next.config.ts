import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  output: "standalone",
  cacheComponents: true,
  partialPrefetching: true,

  rewrites() {
    return Promise.resolve([
      { source: "/api/:path*", destination: `${API_URL}/:path*` },
    ]);
  },

  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;

const API_URL = process.env.API_URL ?? "http://api:8000";
