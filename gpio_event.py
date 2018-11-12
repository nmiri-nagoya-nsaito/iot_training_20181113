import RPi.GPIO as GPIO
import time
from threading import Timer

# ピンの設定
GPIO.setwarnings(False)  # 警告を無視
GPIO.setmode(GPIO.BOARD) # ピンの番号は物理ピンの番号を使う
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # 10番ピンをプルダウンかつ入力に設定
GPIO.setup(8,GPIO.OUT, initial=GPIO.HIGH)    # ピン番号8番を出力に設定する．初期値はHIGH

# LEDをOFFにする処理
def led_off():
    GPIO.output(8, GPIO.HIGH)

# ボタンが押されたときに実行する関数
def button_callback(channel):
    if(channel==10):
        print("Button was pushed!")
        GPIO.output(8, GPIO.LOW)
        # 1秒後にLEDをOFF
        Timer(1, led_off).start()

# 入力ピンの信号の立ち上がりでイベントを発生させる
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback, bouncetime=1000)

try:
    # キーボード入力待ち
    message = input("Press enter to quit\n\n") 
except KeyboardInterrupt:
    print('Keyboard Interrupted')
finally:
    # GPIO設定を初期化
    GPIO.cleanup()
