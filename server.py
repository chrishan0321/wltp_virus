from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/get_logs', methods=['POST'])
def get_logs():
    logs = request.form['logs']
    timestamped_log = f'{datetime.now()} - {logs}'

    # 콘솔에 출력
    print(timestamped_log)

    # 파일에 저장
    with open('logs.log', 'a') as f:
        f.write(timestamped_log + '\n')

    return {'result': True}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
