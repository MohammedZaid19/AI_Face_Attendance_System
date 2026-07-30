# 🎓 AI Face Attendance System

A real-time, browser-camera-based face recognition attendance system built with **Streamlit**, **OpenCV**, **MySQL**, and **Google Gemini AI** — fully deployed on Streamlit Cloud.

---

## ✨ Features

- 👨‍🎓 **Student Registration** — capture a face via the browser camera, generate a facial embedding, and store it securely in MySQL
- 📸 **Live Attendance** — take a photo in-browser; the system detects, recognizes, and automatically marks attendance
- 📄 **Attendance Reports** — search, filter, and export attendance records as CSV
- 🤖 **Gemini AI Assistant** — ask natural-language questions about attendance data ("Who was absent today?")
- ⚙️ **Settings Dashboard** — live system info, database status, and maintenance tools

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| Frontend / App | [Streamlit](https://streamlit.io) |
| Face Detection | OpenCV **YuNet** (`cv2.FaceDetectorYN`) |
| Face Recognition | OpenCV **SFace** (`cv2.FaceRecognizerSF`) — lightweight ONNX, no TensorFlow |
| Database | MySQL, hosted on [Railway](https://railway.app) |
| AI Chat | Google **Gemini API** (`google-genai`) |
| Hosting | [Streamlit Community Cloud](https://streamlit.io/cloud) |
| Version Control | GitHub |

> **Why SFace instead of DeepFace/ArcFace?** DeepFace's TensorFlow backend consistently exceeded Streamlit Cloud's free-tier memory limit (~1GB), causing silent crashes. SFace produces a smaller 128-d embedding, runs on plain OpenCV with no deep learning framework, and comfortably fits within free-tier resources.

---

## 🗂️ Project Structure
