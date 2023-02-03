# MouseDB （マウス管理確認用）

## How to open app
    cd ~/Dropbox/mouseDB/ 
    python mouseDB_App.py

## Environment
1. python 3.6 くらい
2. tkinter (for GUI)
3. sqlite3
4. pandas

## Files
1. mouseDB_App.py #メイン
2. ./View/select_sql.py #SQL 関係
3. ./View/register.py #DB 操作関係
4. ./View/window.py #GUI 表示関係

## Button Menu
### Buy
マウスの購入登録（交配以外での登録）．個体 ID が振られる．
### Mate
マウスの交配，♂，♀ の ID と交配日を登録，Mate ID が振られる．♀ の Status が M （Mating) に変更
### Pregnancy
交配後の♀マウスの妊娠登録．Mate ID から該当する pair を選んで，Success/Fail を登録．Succress の場合は，PregID が振られ，♀ の Status が P (Pregnancy) に変更
### Birth
出産の登録．Preg ID から該当する pair を選んで，仔マウスの数と生年月日を入力，数は適当でも可．♀ の Status が W(Weaning) に変更．失敗の場合は，仔マウスの数を 0, 0 のまま Register．Status は B に戻る．
### Wean
離乳マウスの登録．実際に離乳したマウスの数を ♂, ♀ ごとに登録，離乳した各個体に ID が振られる．
### Retire
殺処分，自然死したマウスの登録．Status が R (Retire) に変更．メインメニューの下にでる殺処分数は Retire の日から算出している．

