import fetch from "node-fetch";

export async function getAccessToken(): Promise<string> {
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

  const response = await fetch("https://api.dropbox.com/oauth2/token", {
    method: "POST",
    headers: {
      Authorization:
        "Basic " +
        Buffer.from(`${clientId}:${clientSecret}`).toString("base64"),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: params.toString(),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Dropboxトークン取得に失敗しました: ${errorText}`);
  }

  const json = await response.json();
  return json.access_token;
}
