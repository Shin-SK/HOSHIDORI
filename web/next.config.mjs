/** @type {import('next').NextConfig} */
const nextConfig = {
  async headers() {
    return [
      {
        // API routes に CORS ヘッダーを追加
        source: '/api/:path*',
        headers: [
          { key: 'Access-Control-Allow-Credentials', value: 'true' },
          { key: 'Access-Control-Allow-Origin', value: 'https://hoshidori-frontend.vercel.app' },
          { key: 'Access-Control-Allow-Methods', value: 'GET,DELETE,PATCH,POST,PUT,OPTIONS' },
          { key: 'Access-Control-Allow-Headers', value: 'X-Requested-With, Content-Type, Authorization' },
        ],
      },
    ]
  },
};

export default nextConfig;
