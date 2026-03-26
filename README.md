# CCTV-Threat-Detection-System-SIEM
CCTV threat detection system that uses computer vision to identify motion and color-based events, generating severity-based alerts and integrating with Splunk for real-time monitoring, alerting, and incident analysis

## 📌 Overview
This project detects motion and color-based threats from CCTV feed and generates alerts using SIEM (Splunk).

## 🚀 Features
- Motion Detection
- Red Object Detection (High Severity)
- Green Object Detection (Normal)
- Snapshot Capture
- Log Generation (SIEM Ready)
- Splunk Integration
- Email Alerts

## 🛠️ Tech Stack
- Python
- OpenCV
- Splunk SIEM

## 📊 Architecture
Camera → Python Detection → Logs → Splunk → Alerts

## 💼 Use Case
Simulates real SOC monitoring and alerting workflow.

## ▶️ How to Run
```bash
pip install opencv-python numpy imutils
python main.py
