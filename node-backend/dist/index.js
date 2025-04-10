"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
// src/index.ts
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const generate_1 = require("./generate");
const dotenv_1 = __importDefault(require("dotenv"));
const path_1 = __importDefault(require("path"));
// 💡 環境変数の読み込み
dotenv_1.default.config({ path: path_1.default.join(__dirname, "../.env") });
// 💡 環境変数のデバッグ
console.log("環境変数の確認:");
console.log("DROPBOX_CLIENT_ID:", process.env.DROPBOX_CLIENT_ID ? "設定済み" : "未設定");
console.log("DROPBOX_CLIENT_SECRET:", process.env.DROPBOX_CLIENT_SECRET ? "設定済み" : "未設定");
console.log("DROPBOX_REFRESH_TOKEN:", process.env.DROPBOX_REFRESH_TOKEN ? "設定済み" : "未設定");
const app = (0, express_1.default)();
const PORT = 4000;
// 💡 CORS設定はここで！
app.use((0, cors_1.default)());
// 💡 JSONを扱えるようにする
app.use(express_1.default.json());
// 🔁 ルーティング
app.use("/generate", generate_1.generateRoute);
app.listen(PORT, () => {
    console.log(`✅ APIサーバー起動中: http://localhost:${PORT}`);
});
