# DAREKA_IMASUKA
Bluetoothの電波から在室状況を把握するシステム(バックエンド)です．<br>
Make it possible to know who is in the room from the Bluetooth signal<br>
＊使用によって被った損害に対して一切の責任を負いません．

## Description
### 📶 DAREKA_IMASUKA.py
部屋に入ると自動的に存在を記録します．<br>
Raspberry piの通信範囲内に登録した端末が入ると，`在室`と判定し，データベースへ反映します．<br>
端末の特定はデータベースに保存されたBluetoothのMACアドレスを使用して行います．

テーブル例です．BTアドレスとIDは動作に必要です．<br>
IDは`AUTO_INCREMENT`を設定し，1~の連番にする必要があります．
###### ＊ROOM_Xは各部屋の在室状況を示します．
|ID|NAME|BT_ADDRESS|ROOM_X|ROOM_Y|ROOM_Z|
|:---:|:---:|:---:|:---:|:---:|:---:|
|1|山田太郎|XX:XX:XX:XX:XX:XX|在室|  |  |

### 🖥️ Status.php
状況を表示させるページです．

## Requirements
以下のライブラリを使用しています．(Python)
* sshtunnel
* pymysql
* subprocess

また，定期的に在室状況を得るために`cron`等を使用します．

## Useage
一度実行すれば，登録された全メンバーの在室状況を取得します．<br>
定期的に実行すれば，定期的に情報を収集します．<br>
cronの設定例<br>
`$ cron -e`でエディタに入り，以下のような記述をすれば，7~23時の間に2分間隔で実行されます．
```
*/2 7-23 * * * python3 /hoge/DAREKA_IMASUKA.py
```
