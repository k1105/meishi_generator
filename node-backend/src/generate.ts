import {Router, Request, Response} from "express";
import fs from "fs";
import path from "path";
import {exec} from "child_process";
import {uploadToDropbox} from "./dropbox";
import archiver from "archiver";

interface RequestBody {
  employeeNumber: string;
  name: string;
  nameJa: string;
  office: string;
  roll: string;
  secondRoll?: string;
  tel: string;
  email: string;
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

    // サブディレクトリの作成
    const aiDir = path.join(folderPath, "ai");
    const pdfDir = path.join(folderPath, "pdf");
    const scriptsDir = path.join(aiDir, "scripts");
    const linksDir = path.join(aiDir, "links");
    const variablesDir = path.join(aiDir, "variables");

    try {
      // フォルダがなければ作成
      if (!fs.existsSync(folderPath)) {
        fs.mkdirSync(folderPath, {recursive: true});
      }
      fs.mkdirSync(aiDir, {recursive: true});
      fs.mkdirSync(pdfDir, {recursive: true});
      fs.mkdirSync(scriptsDir, {recursive: true});
      fs.mkdirSync(linksDir, {recursive: true});
      fs.mkdirSync(variablesDir, {recursive: true});

      // ファイルの複製
      const assetsDir = path.join(__dirname, "../../node-backend/assets");
      const templateAiPath = path.join(assetsDir, "front_template.ai");
      const generateJsxPath = path.join(assetsDir, "generate_front.jsx");

      console.log("📁 アセットディレクトリ:", assetsDir);
      console.log("📄 AIテンプレートパス:", templateAiPath);
      console.log("📄 JSXスクリプトパス:", generateJsxPath);

      if (!fs.existsSync(templateAiPath)) {
        throw new Error(`front_template.aiが見つかりません: ${templateAiPath}`);
      }
      if (!fs.existsSync(generateJsxPath)) {
        throw new Error(
          `generate_front.jsxが見つかりません: ${generateJsxPath}`
        );
      }

      // ファイルを非同期でコピー
      await Promise.all([
        fs.promises.copyFile(
          templateAiPath,
          path.join(aiDir, "front_template.ai")
        ),
        fs.promises.copyFile(
          generateJsxPath,
          path.join(scriptsDir, "generate_front.jsx")
        ),
      ]);

      console.log("✅ テンプレートファイルの複製が完了しました");

      // JSONファイルとして保存
      const jsonFilename = `${employeeNumber}_${safeName}.json`;
      const jsonPath = path.join(folderPath, jsonFilename);
      fs.writeFileSync(jsonPath, JSON.stringify(data, null, 2), "utf8");
      console.log(`✅ JSONファイルを保存しました: ${jsonPath}`);

      // CSVファイルの生成
      const csvFilename = "data.csv";
      const csvPath = path.join(variablesDir, csvFilename);

      // businessTitleの生成
      const roll = data.roll || "";
      const secondRoll = data.secondRoll || "";
      const businessTitle = secondRoll ? `${roll} / ${secondRoll}` : roll;

      // CSVヘッダーとデータの準備
      const csvData = [
        "employeeNumber,nameJa,name,businessTitle,tel,email,office",
        [
          data.employeeNumber,
          data.nameJa,
          data.name,
          businessTitle,
          data.tel,
          data.email,
          data.office,
        ].join(","),
      ].join("\n");

      fs.writeFileSync(csvPath, csvData, "utf8");
      console.log(`✅ CSVファイルを生成しました: ${csvPath}`);

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
        const pdfFilename = `${employeeNumber}_${safeName}_back.pdf`;
        const pdfPath = path.join(pdfDir, pdfFilename);

        if (!fs.existsSync(pdfPath)) {
          console.error("❌ PDFファイルが見つかりません:", pdfPath);
          res
            .status(500)
            .json({error: "PDF生成後にファイルが見つかりませんでした"});
          return;
        }

        try {
          // ZIPファイルの作成
          const zipFilename = `${folderName}.zip`;
          const zipPath = path.join(baseDir, zipFilename);
          const output = fs.createWriteStream(zipPath);
          const archive = archiver("zip", {
            zlib: {level: 9}, // 最高圧縮率
          });

          output.on("close", async () => {
            console.log(
              `✅ ZIPファイル作成完了: ${zipPath} (${archive.pointer()} bytes)`
            );

            // ZIPファイルをDropboxにアップロード
            const dropboxPath = `/dlt-meishi-data/${zipFilename}`;
            try {
              await uploadToDropbox(zipPath, dropboxPath);
              console.log("📦 Dropboxへのアップロード完了");

              // ローカルのZIPファイルを削除
              fs.unlinkSync(zipPath);
              console.log("🗑️ ローカルのZIPファイルを削除しました");

              res.status(200).json({
                message: "PDF生成＆Dropboxアップロード完了 🎉",
                folderPath,
              });
            } catch (err) {
              console.error("❌ Dropboxアップロード失敗:", err);
              res
                .status(500)
                .json({error: "Dropboxへのアップロードに失敗しました"});
            }
          });

          archive.on("error", (err: Error) => {
            throw err;
          });

          archive.pipe(output);

          // フォルダ内のすべてのファイルをZIPに追加
          archive.directory(folderPath, folderName);

          await archive.finalize();
        } catch (err) {
          console.error("❌ ZIPファイル作成失敗:", err);
          res.status(500).json({error: "ZIPファイルの作成に失敗しました"});
        }
      });
    } catch (err) {
      console.error("❌ ディレクトリ構造のセットアップに失敗:", err);
      res
        .status(500)
        .json({error: "ディレクトリ構造のセットアップに失敗しました"});
    }
  }
);
