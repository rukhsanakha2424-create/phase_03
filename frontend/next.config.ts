// // import type { NextConfig } from 'next'

// // const nextConfig: NextConfig = {
// //   reactStrictMode: true,
// //   typescript: {
// //     tsconfigPath: './tsconfig.json',
// //   },
// //   experimental: {
// //     optimizePackageImports: ['better-auth'],
// //   },
// // }

// // export default nextConfig

// // next.config.js
// /** @type {import('next').NextConfig} */
// const nextConfig = {
//   turbowarp: {
//     root: './fronted', // or wherever your frontend is
//   },
// }

// module.exports = nextConfig

import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true,
  turbopack: {
    root: '../'
  }
}

export default nextConfig