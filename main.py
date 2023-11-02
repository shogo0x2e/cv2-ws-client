import requests
import cv2
import json
import time

########## CONFIG ##########
WEBHOOK_URI = "https://webhook.site/5995a36a-ab17-44f5-b257-4759d90eed9b"
CAMERA_ID   = 0

# Webhook 接続 (切れたら再接続)
def send_hook(obj):
    requests.post(
        WEBHOOK_URI,
        data=json.dumps(obj),
        headers={
            'Content-Type':'application/json'
        }
    )

# カメラデバイス取得
cap = cv2.VideoCapture(CAMERA_ID)
# QRCodeDetectorを生成
detector = cv2.QRCodeDetector()

# 同じものは繰り返し送らない
read_before = ""

while True:
    # カメラから1フレーム読み取り
    ret, frame = cap.read()

    # QRコードを認識
    data, bbox, _ = detector.detectAndDecode(frame)

    # 読み取れたらデコードした内容と隅のマーカーの座標をprint
    if data:
        
        print(str(time.time()) + " | Decoded Data:", data)
        
        if data != read_before and bbox is not None:
            
            # 左上 (0, 0)
            # → ↓ 増加方向
            obj = {
                "type":           "onQRscan",
                "value":          data,
                "topLeft":        bbox[0][0].tolist(),
                "topRight":       bbox[0][1].tolist(),
                "bottomLeft":     bbox[0][2].tolist(),
                "bottomRight":    bbox[0][3].tolist()
            }
            
            send_hook(obj)
            read_before = data
            
            print("Sent!")

    # ウィンドウ表示
    cv2.imshow('frame', frame)

    # Qキー押すと終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 終了処理
cap.release()
cv2.destroyAllWindows()
