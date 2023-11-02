import websocket
import _thread
import time
import rel

def on_message(ws, message):
  print("受信: " + message)

def on_error(ws, error):
  print(error)

def on_close(ws, close_status_code, close_msg):
  print("### 切断しました ###")
  
  # 再接続を 1 秒間隔で試みる。

def on_open(ws):
  def run(*args):
    for i in range(10):
      time.sleep(1)
      print("送信: \"" + ("こんにちは %d" % i) + "\"")
      ws.send("こんにちは %d" % i)
    time.sleep(1)
    # print("スレッドを終了中です...")
    # ws.close()
  _thread.start_new_thread(run, ())

if __name__ == "__main__":
  websocket.enableTrace(True)
  ws = websocket.WebSocketApp("ws://localhost:13254",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

  ws.run_forever(dispatcher=rel, reconnect=5)
  rel.signal(2, rel.abort)  # Keyboard Interrupt
  rel.dispatch()  