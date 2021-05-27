# coding: utf8
from sshtunnel import SSHTunnelForwarder
import pymysql
import subprocess

# SSHを介してDB接続
class DBHelper:
    def __init__(self):
        # DBログイン情報
        self.db_host = "localhost"
        self.db_user = "hoge"
        self.db_password = "hoge"
        self.db_name = "hoge"
        
        # SSH/MySQL接続情報
        self.ssh_host = 'hoge.hoge.jp'
        self.ssh_port = 00000
        self.ssh_user = 'hoge'
        self.ssh_pkey = '~/.hoge/hogehoge.key'
        self.ssh_password = 'hoge'
        self.ssh_mysql_host = 'hoge.hoge.jp'
        self.ssh_mysql_port = 00000
        
    def __connect__(self):
        self.server = SSHTunnelForwarder(
            (self.ssh_host, self.ssh_port),
            ssh_username=self.ssh_user,
            ssh_pkey=self.ssh_pkey,
            ssh_password=self.ssh_password,
            remote_bind_address=(self.ssh_mysql_host,self.ssh_mysql_port),
        )
        self.server.start()
        self.con = pymysql.connect(
            host=self.db_host,
            port=self.server.local_bind_port,
            user=self.db_user,
            passwd=self.db_password,
            db=self.db_name,
            # Select結果をタブルで受け取る
            cursorclass=pymysql.cursors.Cursor
        )
        self.cur = self.con.cursor()

    def __disconnect__(self):
        self.con.close()
        self.server.stop()

    def fetch(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def execute(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        self.__disconnect__()
        
    def commit(self, sql):
        self.__connect__()
        self.cur.execute(sql)
        self.con.commit()
        self.__disconnect__()

# 在室情報取得
# DBのBTアドレスを配列に渡す
db = DBHelper()
sql = "SELECT BT_ADDRESS FROM CurrentStatus"
Qbt = db.fetch(sql)
bt = []
for a in Qbt:
    bt.append(a[0])
#print(bt)

# 各端末へPingを送る
print('Looking for people in the room...')
i = 0
status = []
for person in bt:
    # コマンドをターミナルで実行
    cmd = 'sudo l2ping -c 1 '+bt[i]
    try:
        proc = subprocess.check_output(cmd.split()).decode()
        if '1 received' in proc:
            status.append('在室')
        else:
            status.append('')
        i += 1
    except:
        status.append('')
        i += 1
        continue

# 在室情報をアップデート(ROOM_Xはraspberry piの設置場所に応じて変更)
sql = "UPDATE CurrentStatus SET ROOM_X = %s WHERE ID = %s"
db.__connect__()
w = 1
while i >= w:
    r = db.cur.execute(sql,(status[w-1],w))
    print(status[w-1])
    w += 1
db.con.commit()
db.__disconnect__()
