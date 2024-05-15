const share_check = document.getElementById("id_share");
const share_code = document.getElementById("share-code");
// ページ読み込み時に実行
document.addEventListener('DOMContentLoaded', function() {
  // チェック状態に応じてshare-codeの表示を設定
  toggle();
});
// チェックされているかどうかをチェックする
function isChecked() {
  return share_check.checked;
}
// チェック状態と表示状態を制御する
function toggle() {
  // Aがチェックされていない場合はBをチェック解除する
  if (!isChecked()) {
    document.getElementById("share-code").style.display = "none";
  }else{
    document.getElementById("share-code").style.display = "block";
  }
}
// チェック状態が変更されたときに呼び出される
share_check.addEventListener("change", toggle);
