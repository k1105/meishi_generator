"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getAccessToken = getAccessToken;
const node_fetch_1 = __importDefault(require("node-fetch"));
function getAccessToken() {
    return __awaiter(this, void 0, void 0, function* () {
        const clientId = process.env.DROPBOX_CLIENT_ID;
        const clientSecret = process.env.DROPBOX_CLIENT_SECRET;
        const refreshToken = process.env.DROPBOX_REFRESH_TOKEN;
        console.log("getAccessToken内での環境変数の確認:");
        console.log("DROPBOX_CLIENT_ID:", clientId);
        console.log("DROPBOX_CLIENT_SECRET:", clientSecret ? "設定済み" : "未設定");
        console.log("DROPBOX_REFRESH_TOKEN:", refreshToken ? "設定済み" : "未設定");
        if (!clientId || !clientSecret || !refreshToken) {
            throw new Error("Dropboxのクライアント情報が環境変数に設定されていません");
        }
        const params = new URLSearchParams();
        params.append("grant_type", "refresh_token");
        params.append("refresh_token", refreshToken);
        const response = yield (0, node_fetch_1.default)("https://api.dropbox.com/oauth2/token", {
            method: "POST",
            headers: {
                Authorization: "Basic " +
                    Buffer.from(`${clientId}:${clientSecret}`).toString("base64"),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: params.toString(),
        });
        if (!response.ok) {
            const errorText = yield response.text();
            throw new Error(`Dropboxトークン取得に失敗しました: ${errorText}`);
        }
        const json = yield response.json();
        return json.access_token;
    });
}
