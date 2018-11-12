import cv2

# cv2 を使ってカメラからキャプチャし，毎フレーム毎の画像を表示する
# ウィンドウが開き，キャプチャした映像が表示される
# ESCキーで停止する．
# Jupyter Notebookではウィンドウが閉じずに固まるため，スクリプトで実行する．

def capture_camera(mirror=True, size=None):
    """Capture video from camera"""
    # カメラをキャプチャする
    cap = cv2.VideoCapture(0) # 0はカメラのデバイス番号

    while True:
        # retは画像を取得成功フラグ
        ret, frame = cap.read()

        # 鏡のように映るか否か
        if mirror is True:
            frame = frame[:,::-1]

        # フレームをリサイズ
        # sizeは例えば(800, 600)
        if size is not None and len(size) == 2:
            frame = cv2.resize(frame, size)

        # フレームを表示する
        cv2.imshow('camera capture', frame)

        k = cv2.waitKey(1) # 1msec待つ
        if k == 27: # ESCキーで終了
            break
    
    # キャプチャを解放する
    cap.release()
    cv2.destroyAllWindows()

# プログラム開始
capture_camera()
