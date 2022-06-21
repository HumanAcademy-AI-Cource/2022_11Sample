#!/usr/bin/env python3

# 必要なライブラリをインポート
import sys
import select
import tty
import termios
import rospy
from std_msgs.msg import *

class KeyLedNode(object):
    def __init__(self):
        # ROSの設定
        self.led_pub = rospy.Publisher('/led', ColorRGBA, queue_size=1)

        # キー入力の設定
        self.old_console_setting = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())

    def main(self):
        # 一定周期でループを実行するための変数を定義
        rate = rospy.Rate(10)
        color = ColorRGBA()

        print("--------------------------------------------------")
        print(" r, g, bキーを押すとそれぞれの色にLEDが光ります。")
        print(" 終了するには Ctrl-C を押してください。")
        print("--------------------------------------------------")
        # Whileでキー入力を待ち続ける
        while not rospy.is_shutdown():
            # キー入力があるか確認
            if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
                # 入力されたキーを調べる
                key = sys.stdin.read(1)
                # もしrが入力されていたらLEDを赤色に光らせる
                if key == "r":
                    color.r = 255.0
                    color.g = 0
                    color.b = 0
                    self.led_pub.publish(color)
                    print("r: Red " + "\033[31m" + "●" + "\033[0m")
                # もしgが入力されていたらLEDを緑色に光らせる
                elif key == "g":
                    color.r = 0
                    color.g = 255.0
                    color.b = 0
                    self.led_pub.publish(color)
                    print("g: Green " + "\033[32m"+"●"+"\033[0m")
                # もしbが入力されていたらLEDを青色に光らせる
                elif key == "b":
                    color.r = 0
                    color.g = 0
                    color.b = 255.0
                    self.led_pub.publish(color)
                    print("b: Brue " + "\033[34m"+"●"+"\033[0m")
            rate.sleep()

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_console_setting)


if __name__ == '__main__':
    # ノードを宣言
    rospy.init_node("key_led")
    # クラスのインスタンスを作成し、メイン関数を実行
    KeyLedNode().main()
