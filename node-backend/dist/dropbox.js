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
exports.uploadToDropbox = uploadToDropbox;
const dropbox_1 = require("dropbox");
const fs_1 = __importDefault(require("fs"));
const getAccessToken_1 = require("./utils/getAccessToken");
function uploadToDropbox(localPath, dropboxPath) {
    return __awaiter(this, void 0, void 0, function* () {
        const accessToken = yield (0, getAccessToken_1.getAccessToken)();
        const dbx = new dropbox_1.Dropbox({ accessToken });
        const fileContent = fs_1.default.readFileSync(localPath);
        yield dbx.filesUpload({
            path: dropboxPath,
            contents: fileContent,
            mode: { ".tag": "overwrite" },
        });
        console.log(`📦 Dropboxへアップロード完了: ${dropboxPath}`);
    });
}
