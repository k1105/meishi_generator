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
exports.generateRoute = void 0;
const express_1 = require("express");
const fs_1 = __importDefault(require("fs"));
const path_1 = __importDefault(require("path"));
const child_process_1 = require("child_process");
const dropbox_1 = require("./dropbox");
const archiver_1 = __importDefault(require("archiver"));
exports.generateRoute = (0, express_1.Router)();
exports.generateRoute.post("/", (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    const data = req.body;
    const { employeeNumber, name, office } = data;
    // ✅ 日付フォーマット: YYMMDD
    const now = new Date();
    const yymmdd = now.toISOString().slice(2, 10).replace(/-/g, "");
    // ✅ 保存パスの生成
    const baseDir = path_1.default.join(__dirname, "../..", "dropbox-storage");
    const safeName = name.toLowerCase().replace(/\s+/g, "_");
    const folderName = `${yymmdd}_${employeeNumber}_${safeName}_${office}`;
    const folderPath = path_1.default.join(baseDir, folderName);
    // サブディレクトリの作成
    const aiDir = path_1.default.join(folderPath, "ai");
    const pdfDir = path_1.default.join(folderPath, "pdf");
    const scriptsDir = path_1.default.join(aiDir, "scripts");
    const linksDir = path_1.default.join(aiDir, "links");
    const variablesDir = path_1.default.join(aiDir, "variables");
    try {
        // フォルダがなければ作成
        if (!fs_1.default.existsSync(folderPath)) {
            fs_1.default.mkdirSync(folderPath, { recursive: true });
        }
        fs_1.default.mkdirSync(aiDir, { recursive: true });
        fs_1.default.mkdirSync(pdfDir, { recursive: true });
        fs_1.default.mkdirSync(scriptsDir, { recursive: true });
        fs_1.default.mkdirSync(linksDir, { recursive: true });
        fs_1.default.mkdirSync(variablesDir, { recursive: true });
        // ファイルの複製
        const assetsDir = path_1.default.join(__dirname, "../../node-backend/assets");
        const templateAiPath = path_1.default.join(assetsDir, "front_template.ai");
        const generateJsxPath = path_1.default.join(assetsDir, "generate_front.jsx");
        console.log("📁 アセットディレクトリ:", assetsDir);
        console.log("📄 AIテンプレートパス:", templateAiPath);
        console.log("📄 JSXスクリプトパス:", generateJsxPath);
        if (!fs_1.default.existsSync(templateAiPath)) {
            throw new Error(`front_template.aiが見つかりません: ${templateAiPath}`);
        }
        if (!fs_1.default.existsSync(generateJsxPath)) {
            throw new Error(`generate_front.jsxが見つかりません: ${generateJsxPath}`);
        }
        // ファイルを非同期でコピー
        yield Promise.all([
            fs_1.default.promises.copyFile(templateAiPath, path_1.default.join(aiDir, "front_template.ai")),
            fs_1.default.promises.copyFile(generateJsxPath, path_1.default.join(scriptsDir, "generate_front.jsx")),
        ]);
        console.log("✅ テンプレートファイルの複製が完了しました");
        // JSONファイルとして保存
        const jsonFilename = `${employeeNumber}_${safeName}.json`;
        const jsonPath = path_1.default.join(folderPath, jsonFilename);
        fs_1.default.writeFileSync(jsonPath, JSON.stringify(data, null, 2), "utf8");
        console.log(`✅ JSONファイルを保存しました: ${jsonPath}`);
        // CSVファイルの生成
        const csvFilename = "data.csv";
        const csvPath = path_1.default.join(variablesDir, csvFilename);
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
        fs_1.default.writeFileSync(csvPath, csvData, "utf8");
        console.log(`✅ CSVファイルを生成しました: ${csvPath}`);
        // ✅ Pythonスクリプトを実行してPDFを生成
        const pythonScriptPath = path_1.default.join(__dirname, "../..", "python-generator", "main.py");
        const command = `python3 "${pythonScriptPath}" --json "${jsonPath}"`;
        (0, child_process_1.exec)(command, (error, stdout, stderr) => __awaiter(void 0, void 0, void 0, function* () {
            if (error) {
                console.error(`❌ Python実行エラー:\n${stderr}`);
                res.status(500).json({ error: "Pythonスクリプトの実行に失敗しました" });
                return;
            }
            console.log(`✅ Python実行完了:\n${stdout}`);
            // PDFファイルのパスを確認
            const pdfFilename = `${employeeNumber}_${safeName}_back.pdf`;
            const pdfPath = path_1.default.join(pdfDir, pdfFilename);
            if (!fs_1.default.existsSync(pdfPath)) {
                console.error("❌ PDFファイルが見つかりません:", pdfPath);
                res
                    .status(500)
                    .json({ error: "PDF生成後にファイルが見つかりませんでした" });
                return;
            }
            try {
                // ZIPファイルの作成
                const zipFilename = `${folderName}.zip`;
                const zipPath = path_1.default.join(baseDir, zipFilename);
                const output = fs_1.default.createWriteStream(zipPath);
                const archive = (0, archiver_1.default)("zip", {
                    zlib: { level: 9 }, // 最高圧縮率
                });
                output.on("close", () => __awaiter(void 0, void 0, void 0, function* () {
                    console.log(`✅ ZIPファイル作成完了: ${zipPath} (${archive.pointer()} bytes)`);
                    // ZIPファイルをDropboxにアップロード
                    const dropboxPath = `/dlt-meishi-data/${zipFilename}`;
                    try {
                        yield (0, dropbox_1.uploadToDropbox)(zipPath, dropboxPath);
                        console.log("📦 Dropboxへのアップロード完了");
                        // ローカルのZIPファイルを削除
                        fs_1.default.unlinkSync(zipPath);
                        console.log("🗑️ ローカルのZIPファイルを削除しました");
                        res.status(200).json({
                            message: "PDF生成＆Dropboxアップロード完了 🎉",
                            folderPath,
                        });
                    }
                    catch (err) {
                        console.error("❌ Dropboxアップロード失敗:", err);
                        res
                            .status(500)
                            .json({ error: "Dropboxへのアップロードに失敗しました" });
                    }
                }));
                archive.on("error", (err) => {
                    throw err;
                });
                archive.pipe(output);
                // フォルダ内のすべてのファイルをZIPに追加
                archive.directory(folderPath, folderName);
                yield archive.finalize();
            }
            catch (err) {
                console.error("❌ ZIPファイル作成失敗:", err);
                res.status(500).json({ error: "ZIPファイルの作成に失敗しました" });
            }
        }));
    }
    catch (err) {
        console.error("❌ ディレクトリ構造のセットアップに失敗:", err);
        res
            .status(500)
            .json({ error: "ディレクトリ構造のセットアップに失敗しました" });
    }
}));
