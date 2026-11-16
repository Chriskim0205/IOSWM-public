from flask import Flask, jsonify
import os
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

app = Flask(__name__)

# 전역 변수로 실행 중인 프로세스를 저장
running_process = None

@app.route('/')
def index():
    # 버튼 클릭 시 문구 출력 기능이 추가된 HTML 내용
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Run Python Script</title>
        <style>
            body, html {
                height: 100%;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }
            button {
                margin: 5px;
                padding: 10px;
            }
            #output {
                margin-top: 20px;
                border: 1px solid #ccc;
                padding: 10px;
                width: 80%;
                max-width: 600px;
                word-wrap: break-word;
            }
        </style>
    </head>
    <body>
        <h1>Run Python Script from Web</h1>
        <button id="runScript">Run Script</button>
        <button id="stopScript">Stop Script</button>
        <pre id="output"></pre>

        <script>
            document.getElementById("runScript").addEventListener("click", function() {
                fetch("/run-script")
                    .then(response => response.json())
                    .then(data => {
                        // 'Script is running...' 문구를 출력합니다.
                        document.getElementById("output").textContent = 'Script is running...';
                    })
                    .catch(error => console.error("Error:", error));
            });

            document.getElementById("stopScript").addEventListener("click", function() {
                fetch("/stop-script")
                    .then(response => response.json())
                    .then(data => {
                        // 'Script stopped.' 문구를 출력합니다.
                        document.getElementById("output").textContent = 'Script stopped.';
                    })
                    .catch(error => console.error("Error:", error));
            });
        </script>
    </body>
    </html>
    '''
    return html_content

@app.route('/run-script', methods=['GET'])
def run_script():
    global running_process
    command = [sys.executable, os.path.join(PROJECT_ROOT, "run_checklist.py")]
    running_process = subprocess.Popen(command, cwd=PROJECT_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = running_process.communicate()
    output = stdout if stdout else stderr
    # 실제 스크립트 실행 결과는 반환하지만, 프론트엔드에서는 사용하지 않음
    return jsonify(output=output)

@app.route('/stop-script', methods=['GET'])
def stop_script():
    global running_process
    if running_process:
        running_process.terminate()  # 프로세스 종료
        running_process = None
        return jsonify({"message": "Script stopped."})
    else:
        return jsonify({"error": "No running script to stop."})

if __name__ == '__main__':
    app.run(debug=True, port=5005)
