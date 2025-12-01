// src/lib/prisma.js
import { PrismaClient } from '@prisma/client'

// 開発中にHot Reloadでクライアントが増えないようにするおまじない
let prisma

if (!global._prisma) {
  global._prisma = new PrismaClient()
}

prisma = global._prisma

export default prisma