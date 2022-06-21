#!/usr/bin/env python3

# 必要なライブラリをインポート
import sys
import select
import tty
import termios
import rospy
import time
from std_msgs.msg import *


if __name__ == "__main__":
    # ROSの設定
    rospy.init_node("move_motor")
    pub = rospy.Publisher("servo", UInt8, queue_size=1)
    rate = rospy.Rate(100)

    # キー入力の設定
    old_console_setting = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    # モータを初期位置まで移動させる
    motor_init_state = 50
    pub.publish(motor_init_state)
    time.sleep(2)
    print("--------------------------------------------------")
    print("Aキー または Dキー を押すとモータが動きます。")
    print("終了するには Ctrl-C を押してください。")
    print("--------------------------------------------------")
    # Whileでキー入力を待ち続ける
    while not rospy.is_shutdown():
        # キー入力があるか確認
        if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
            # 入力されたキーを調べる
            key = sys.stdin.read(1)

            # もし「dキー」が入力されたら
            if key == "d":
                motor_init_state += 1
            # もし「aキー」が入力されたら
            if key == "a":
                motor_init_state -=1

            # モータの移動範囲に上限を設定する
            if motor_init_state < 30:
                motor_init_state = 30
            if motor_init_state > 90:
                motor_init_state = 90

            # モータの位置をパブリッシュする
            pub.publish(motor_init_state)
        rate.sleep()

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_console_setting)