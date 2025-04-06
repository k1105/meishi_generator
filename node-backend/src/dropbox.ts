import {Dropbox} from "dropbox";
import fs from "fs";
import {getAccessToken} from "./utils/getAccessToken";
import path from "path";

export async function uploadToDropbox(
  localPath: string,
  dropboxPath: string
): Promise<void> {
  const accessToken = await getAccessToken();
  const dbx = new Dropbox({accessToken});

  const fileContent = fs.readFileSync(localPath);

  await dbx.filesUpload({
    path: dropboxPath,
    contents: fileContent,
    mode: {".tag": "overwrite"},
  });

  console.log(`📦 Dropboxへアップロード完了: ${dropboxPath}`);
}
