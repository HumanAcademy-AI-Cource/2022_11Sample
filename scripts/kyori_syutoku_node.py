#!/usr/bin/env python3

# 必要なライブラリをインポート
import rospy
from std_msgs.msg import *

class KyoriSyutokuNode(object):
    def __init__(self):
        # ROSの設定
        rospy.Subscriber("/sensor", UInt16, self.sensor_callback)
        self.sensor_data = 0

    def sensor_callback(self, msg):
        # 距離センサから距離データを取得
        self.sensor_data = msg.data
        # 取得した距離データを表示
        print(self.sensor_data)

    def main(self):
        # 一定周期でループを実行するための変数を定義
        rate = rospy.Rate(10)
        # ループを実行
        while not rospy.is_shutdown():
            rate.sleep()


if __name__ == '__main__':
    # ノードを宣言
    rospy.init_node("kyori_syutoku")
    # クラスのインスタンスを作成し、メイン関数を実行
    KyoriSyutokuNode().main()
