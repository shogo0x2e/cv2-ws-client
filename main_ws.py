import websocket
import _thread
import time
import rel
import cv2
import json

########## CONFIG ##########
SERVER_URI  = "ws://localhost:5001"
CAMERA_ID   = 0
ROLE        = "qrReader"

########### 変数たち ##################
uuid = ""

########### コールバックたち ##########
def on_message(ws, message):
  global uuid 
  obj = json.loads(message)
  
  # 接続初期化だったら、UUID を記憶してデバイスの情報を送る。
  if obj["type"] == "initConnection":
    uuid = json.loads(message)['uuid']
    print("UUID: " + uuid)
    
    obj = {
      "uuid": uuid,
      "type": "initConnection",
      "role": ROLE
    }
    
    ws.send(json.dumps(obj))

def on_error(ws, error):
  print(error)

def on_close(ws, close_status_code, close_msg):
  print("### 切断しました ###")
  
  # 再接続を 1 秒間隔で試みる。

def on_open(ws):
  _thread.start_new_thread(run, ())

########## メインの処理 ###########
def run(*args):
  
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
      
      # ウィンドウ表示
      # cv2.imshow('frame', frame)
      print(str(time.time()) + " | Decoded Data:", data)
      
      if data != read_before and bbox is not None:
        # 左上 (0, 0)
        # → ↓ 増加方向
        obj = {
          "type":           "onQRscan",
          "uuid":           uuid,
          "role":           ROLE,
          "value":          data,
          "topLeft":        bbox[0][0].tolist(),
          "topRight":       bbox[0][1].tolist(),
          "bottomLeft":     bbox[0][2].tolist(),
          "bottomRight":    bbox[0][3].tolist()
        }
        
        ws.send(json.dumps(obj))
        read_before = data
        
        print("Sent!")

if __name__ == "__main__":
  # websocket.enableTrace(True)
  ws = websocket.WebSocketApp(SERVER_URI,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

  ws.run_forever(dispatcher=rel, reconnect=5)
  rel.signal(2, rel.abort)  # Keyboard Interrupt
  rel.dispatch()
