Here's a complete GitHub README.md for your project:

```markdown
# 🔥 Activity Logger - Real-Time Keystroke Monitoring System

A Python-based desktop activity monitoring system that captures keyboard input and sends logs to a local server with a **hacker-themed real-time dashboard**.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey)

## ⚡ Features

- 🎯 **Real-time keystroke logging** across all applications
- 🌐 **Live web dashboard** with cyberpunk/hacker UI
- 📊 **Server-Sent Events (SSE)** for instant log updates
- 💾 **Automatic log saving** to text files
- 🖥️ **Cross-platform support** (Windows & macOS)
- 🔒 **Local-only operation** (localhost server)
- 📦 **Convert to standalone EXE** (Windows only)

## 🎨 Dashboard Preview

The web dashboard features:
- Matrix-style green terminal aesthetic
- Real-time log streaming without page refresh
- Glowing animations and effects
- Live timestamp and statistics
- Auto-scrolling log entries

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation

### Clone Repository

```
git clone https://github.com/jjgowda/activity-logger.git
cd activity-logger
```

### Install Dependencies

**For Windows:**
```
pip install keyboard requests flask
```

**For macOS:**
```
pip install pynput requests flask
```

## 📁 Project Structure

```
activity-logger/
├── server.py                 # Flask server with web dashboard
├── activity_logger.py        # Keystroke logger (Windows)
├── activity_logger_mac.py    # Keystroke logger (macOS)
├── logs/                     # Auto-generated log storage
├── README.md                 # This file
└── requirements.txt          # Python dependencies
```

## 🖥️ Usage

### Step 1: Start the Server

Open a terminal and run:

```
python server.py
```

You should see:
```
🔥 HACKER MONITORING SYSTEM INITIALIZED 🔥
Server: http://localhost:8000
Dashboard: http://localhost:8000/
```

### Step 2: Open Dashboard

Open your web browser and navigate to:
```
http://localhost:8000
```

### Step 3: Start Activity Logger

**On Windows:**

Open a **second terminal as Administrator** and run:
```
python activity_logger.py
```

**On macOS:**

1. First, grant Accessibility permissions:
   - Go to **System Settings → Privacy & Security → Accessibility**
   - Click the **lock** icon and enter your password
   - Click **+** button
   - Add **Terminal** app (or `/opt/anaconda3/bin/python` if using Anaconda)
   - Enable the checkbox

2. Run the logger:
```
python activity_logger_mac.py
```

### Step 4: Monitor Logs

- Type anything on your keyboard
- Logs appear **instantly** on the web dashboard
- All logs are also saved in the `logs/` folder

## ⚙️ Configuration

Edit these variables in the logger script:

```
SEND_REPORT_EVERY = 10    # Send logs every 10 seconds
SERVER_URL = "http://localhost:8000/api/logs"
```

## 📦 Convert to Standalone EXE (Windows Only)

### Install PyInstaller

```
pip install pyinstaller
```

### Create EXE with Custom Icon

1. Download or create a `.ico` icon file
2. Save it as `logger_icon.ico` in the project folder
3. Run:

```
pyinstaller --onefile --noconsole --icon=logger_icon.ico activity_logger.py
```

4. Find your EXE in the `dist/` folder

### Run Without Python

Double-click `activity_logger.exe` (requires admin privileges)

## 🔧 Troubleshooting

### Windows Issues

**"Access Denied" or logger not capturing keys:**
- Run Command Prompt or PowerShell as Administrator
- Right-click the EXE → "Run as Administrator"

### macOS Issues

**"This process is not trusted!" error:**
- Follow Step 3 in the Usage section to grant Accessibility permissions
- Restart Terminal after granting permissions

**403 Forbidden error:**
- macOS blocks port 5000 (AirPlay Receiver)
- The code uses port 8000 by default
- Or disable AirPlay: **System Settings → AirDrop & Handoff → Turn off AirPlay Receiver**

**Bus Error:**
- Make sure you're using `activity_logger_mac.py` (with `pynput` library)
- Don't use the Windows version on macOS

### General Issues

**Server connection error:**
- Ensure `server.py` is running before starting the logger
- Check that you're using the correct port (8000)

**No logs appearing:**
- Wait for the interval time (default: 10 seconds)
- Make sure you're actually typing something
- Check console output for error messages

## ⚠️ Legal & Ethical Notice

**IMPORTANT:** This software is intended for:
- ✅ Educational purposes
- ✅ Monitoring your own devices
- ✅ Testing and development
- ✅ Parental control with proper authorization

**DO NOT use this software for:**
- ❌ Unauthorized surveillance
- ❌ Spying on others without consent
- ❌ Any illegal activities
- ❌ Violating privacy laws

**Always:**
- Obtain proper authorization before deployment
- Comply with local privacy and surveillance laws
- Use responsibly and ethically
- Inform users if monitoring is active

The developers assume no liability for misuse of this software.

## 🛡️ Privacy & Security

- All data stays on **localhost** (your machine only)
- No external network connections
- Logs stored locally in the `logs/` folder
- No cloud storage or third-party services

## 📝 Requirements.txt

```
flask==3.0.0
requests==2.31.0
keyboard==0.13.5        # Windows only
pynput==1.7.6           # macOS only
pyinstaller==6.3.0      # Optional: for creating EXE
```

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Flask for web server
- Uses `keyboard` library for Windows
- Uses `pynput` library for macOS
- Inspired by cyberpunk/hacker aesthetics

## 📧 Contact

**Jeevan Gowda** - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/jjgowda/activity-logger](https://github.com/jjgowda/activity-logger)

---

⭐ **Star this repo if you find it useful!** ⭐

Made with 💚 by [Jeevan Gowda]
```

## Create requirements.txt file:

```txt
flask==3.0.0
requests==2.31.0
keyboard==0.13.5
pynput==1.7.6
pyinstaller==6.3.0
```

