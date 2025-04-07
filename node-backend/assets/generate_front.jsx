// generate_front_by_textlayer.jsx

var doc = app.activeDocument;
var csvFile = File(doc.path + "/variables/data.csv");

if (!csvFile.exists) {
  alert("CSVファイルが見つかりません: variables/data.csv");
  exit();
}
csvFile.open("r");
var lines = [];
while (!csvFile.eof) {
  var line = csvFile.readln();
  if (line !== "") lines.push(line);
}
csvFile.close();

// CSVヘッダー
var headers = lines[0].split(",");
function parseLine(line) {
  var values = line.split(",");
  var result = {};
  for (var i = 0; i < headers.length; i++) {
    result[headers[i]] = values[i];
  }
  return result;
}

// 出力先フォルダのパスを取得
var outputFolder = doc.path + "/../pdf";
$.writeln("📁 出力先フォルダ: " + outputFolder);

// フォルダが存在しない場合は作成
var folder = new Folder(outputFolder);
if (!folder.exists) {
  folder.create();
  $.writeln("✅ 出力フォルダを作成: " + outputFolder);
}

// 各レコードを処理
for (var i = 1; i < lines.length; i++) {
  var row = parseLine(lines[i]);

  // ✏️ 対象のテキストオブジェクトを名前で取得し、値をセット
  try {
    var nameJaFrame = doc.textFrames.getByName("name_ja");
    nameJaFrame.contents = row["nameJa"];

    var nameEnFrame = doc.textFrames.getByName("name_en");
    nameEnFrame.contents = row["name"];

    // name_jaの位置とサイズを取得
    var nameJaPos = nameJaFrame.position;
    var nameJaBounds = nameJaFrame.geometricBounds;
    // name_jaの幅を計算
    var nameJaWidth = nameJaBounds[2] - nameJaBounds[0];
    // name_enの元の位置を取得
    var nameEnPos = nameEnFrame.position;
    // name_enの位置を設定（x座標のみ変更）
    nameEnFrame.position = [nameJaPos[0] + nameJaWidth + 9.5, nameEnPos[1]];

    // name_containerグループのスケール調整
    var nameContainer = doc.groupItems.getByName("name_container");
    var containerBounds = nameContainer.geometricBounds;
    var containerWidth = containerBounds[2] - containerBounds[0];
    var originalLeft = containerBounds[0]; // 元の左端の位置を保存

    if (containerWidth > 160) {
      var scaleFactor = 160 / containerWidth;
      nameContainer.resize(scaleFactor * 100, scaleFactor * 100);

      // スケール後の位置を取得
      var newBounds = nameContainer.geometricBounds;
      // 左端の位置を元の位置に戻す
      nameContainer.position = [originalLeft, nameContainer.position[1]];
    }

    // その他のテキスト情報を設定
    doc.textFrames.getByName("tel").contents = row["tel"];
    doc.textFrames.getByName("business_title").contents = row["businessTitle"];
    doc.textFrames.getByName("email").contents = row["email"];
  } catch (e) {
    alert(
      "オブジェクトが見つかりませんでした。レイヤー or オブジェクト名を確認してください。"
    );
    throw e;
  }

  // 保存ファイル名生成
  var nameFormatted = row["name"].replace(/\s+/g, "_").toLowerCase();
  var emp = row["employeeNumber"];
  var pdfName = emp + "_" + nameFormatted + "_front.pdf";

  // 保存
  var saveFile = new File(outputFolder + "/" + pdfName);
  var saveOpts = new PDFSaveOptions();
  saveOpts.compatibility = PDFCompatibility.ACROBAT6;
  saveOpts.preserveEditability = false;

  doc.saveAs(saveFile, saveOpts);
  $.writeln("✅ PDF保存: " + pdfName);
}

alert("名刺PDFの書き出しが完了しました。");
