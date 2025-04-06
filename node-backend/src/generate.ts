import {Router, Request, Response} from "express";
import fs from "fs";
import path from "path";
import {exec} from "child_process";
import {uploadToDropbox} from "./dropbox";

interface RequestBody {
  employeeNumber: string;
  name: string;
  office: string;
}

export const generateRoute = Router();

generateRoute.post<{}, {}, RequestBody>(
  "/",
  async (req, res): Promise<void> => {
    const data = req.body;
    const {employeeNumber, name, office} = data;

    // ✅ 日付フォーマット: YYMMDD
    const now = new Date();
    const yymmdd = now.toISOString().slice(2, 10).replace(/-/g, "");

    // ✅ 保存パスの生成
    const baseDir = path.join(__dirname, "../..", "dropbox-storage");
    const safeName = name.toLowerCase().replace(/\s+/g, "_");
    const folderName = `${yymmdd}_${employeeNumber}_${safeName}_${office}`;
    const folderPath = path.join(baseDir, folderName);

    const jsonFilename = `${employeeNumber}_${safeName}.json`;
    const jsonPath = path.join(folderPath, jsonFilename);

    try {
      // フォルダがなければ作成
      if (!fs.existsSync(folderPath)) {
        fs.mkdirSync(folderPath, {recursive: true});
      }

      // JSONファイルとして保存
      fs.writeFileSync(jsonPath, JSON.stringify(data, null, 2), "utf8");
      console.log(`✅ JSONファイルを保存しました: ${jsonPath}`);
    } catch (err) {
      console.error("❌ JSON保存に失敗:", err);
      res.status(500).json({error: "JSON保存に失敗しました"});
      return;
    }

    // ✅ Pythonスクリプトを実行してPDFを生成
    const pythonScriptPath = path.join(
      __dirname,
      "../..",
      "python-generator",
      "main.py"
    );
    const command = `python3 "${pythonScriptPath}" --json "${jsonPath}"`;

    exec(command, async (error, stdout, stderr) => {
      if (error) {
        console.error(`❌ Python実行エラー:\n${stderr}`);
        res.status(500).json({error: "Pythonスクリプトの実行に失敗しました"});
        return;
      }

      console.log(`✅ Python実行完了:\n${stdout}`);

      // PDFファイルのパスを確認
      const pdfFilename = `${employeeNumber}_${safeName}.pdf`;
      const pdfPath = path.join(folderPath, pdfFilename);

      if (!fs.existsSync(pdfPath)) {
        console.error("❌ PDFファイルが見つかりません:", pdfPath);
        res
          .status(500)
          .json({error: "PDF生成後にファイルが見つかりませんでした"});
        return;
      }

      // ✅ Dropboxアップロードパス（スラッシュ対応）
      const dropboxFolder = `/dlt-meishi-data/${folderName}`;
      const dropboxJsonPath = path
        .join(dropboxFolder, jsonFilename)
        .replace(/\\/g, "/");
      const dropboxPdfPath = path
        .join(dropboxFolder, pdfFilename)
        .replace(/\\/g, "/");

      try {
        await uploadToDropbox(jsonPath, dropboxJsonPath);
        await uploadToDropbox(pdfPath, dropboxPdfPath);

        console.log("📦 Dropboxへのアップロード成功");

        res.status(200).json({
          message: "PDF生成＆Dropboxアップロード完了 🎉",
          folderPath,
        });
      } catch (err) {
        console.error("❌ Dropboxアップロード失敗:", err);
        res.status(500).json({error: "Dropboxへのアップロードに失敗しました"});
      }
    });
  }
);
