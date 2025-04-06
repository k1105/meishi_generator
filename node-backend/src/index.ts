// src/index.ts
import express from "express";
import cors from "cors";
import {generateRoute} from "./generate";
import dotenv from "dotenv";
import path from "path";

// 💡 環境変数の読み込み
dotenv.config({path: path.join(__dirname, "../.env")});

// 💡 環境変数のデバッグ
console.log("環境変数の確認:");
console.log(
  "DROPBOX_CLIENT_ID:",
  process.env.DROPBOX_CLIENT_ID ? "設定済み" : "未設定"
);
console.log(
  "DROPBOX_CLIENT_SECRET:",
  process.env.DROPBOX_CLIENT_SECRET ? "設定済み" : "未設定"
);
console.log(
  "DROPBOX_REFRESH_TOKEN:",
  process.env.DROPBOX_REFRESH_TOKEN ? "設定済み" : "未設定"
);

const app = express();
const PORT = 4000;

// 💡 CORS設定はここで！
app.use(cors());

// 💡 JSONを扱えるようにする
app.use(express.json());

// 🔁 ルーティング
app.use("/generate", generateRoute);

app.listen(PORT, () => {
  console.log(`✅ APIサーバー起動中: http://localhost:${PORT}`);
});
