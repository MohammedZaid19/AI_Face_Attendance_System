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
AI_Face_Attendance_System/
├── app.py # Landing page / entry point
├── main.py # Registration logic (save image + generate embedding)
├── attendance.py # Attendance logic (detect + recognize + mark)
├── attendance_utils.py # Attendance DB helpers (mark, report, CSV export)
├── gemini_chat.py # Gemini AI backend
├── db.py # Shared MySQL connection (reads st.secrets)
├── requirements.txt
├── packages.txt # System-level apt dependencies for OpenCV
├── models/
│ ├── yunet_detector.py
│ ├── sface_recognizer.py
│ ├── face_detection_yunet_2023mar.onnx
│ └── face_recognition_sface_2021dec.onnx
├── pages/
│ ├── stud.py # Registration page (camera capture)
│ ├── attend.py # Attendance page (camera capture)
│ ├── student.py # Registered students list
│ ├── reports.py # Attendance reports
│ ├── settings.py # Settings / system info
│ └── gem_ui.py # Gemini chat UI
└── images/ # Captured student face images


---

## 🔄 How Attendance Works

Browser Camera Capture
↓
YuNet Face Detection
↓
SFace Embedding (128-d)
↓
Compare Against Stored Embeddings (cosine similarity)
↓
Mark Attendance in MySQL


A single photo is captured per action (registration or attendance) — there is no continuous webcam feed, which is what makes this compatible with cloud hosting (cloud servers have no physical camera).

---

## 🔐 Configuration — Streamlit Secrets

Create `.streamlit/secrets.toml` locally (and the equivalent in **Streamlit Cloud → Settings → Secrets** for deployment):

```toml
GEMINI_API_KEY="your_gemini_api_key"

DB_HOST="your_mysql_host"
DB_USER="your_mysql_user"
DB_PASSWORD="your_mysql_password"
DB_NAME="your_database_name"
DB_PORT="your_mysql_port"
```

> ⚠️ Never commit `secrets.toml` to Git. Add `.streamlit/` to `.gitignore`.

---

## 🖥️ Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/MohammedZaid19/AI_Face_Attendance_System.git
cd AI_Face_Attendance_System

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your local secrets
mkdir .streamlit
# create .streamlit/secrets.toml as shown above

# 4. Run the app
streamlit run app.py
```

---

## ☁️ Deployment (Streamlit Cloud)

1. Push the repo to GitHub
2. Create a new app on [share.streamlit.io](https://share.streamlit.io), pointing to `app.py`
3. Add your secrets under **Settings → Secrets**
4. Ensure `packages.txt` is present in the repo root with:

libgl1
libglib2.0-0t64

   (required system libraries for OpenCV on Streamlit Cloud's Debian environment)
5. Deploy / Reboot

### Database
MySQL is hosted on [Railway](https://railway.app) — the local `mysqldump` → import workflow was used to migrate schema and data from a local instance to the cloud.

---

## 🧠 Database Schema (core tables)

| Table | Purpose |
|---|---|
| `students` | student_id, student_name, roll_number, department, image_path |
| `face_embeddings` | student_id, embedding (JSON array, 128 floats) |
| `attendance` | student_id, attendance_date, attendance_time, status |

---

## 🐞 Known Gotchas / Lessons Learned

- **`cv2.VideoCapture(0)` does not work on any cloud host** — cloud servers have no physical webcam. This project uses `st.camera_input()` (browser camera) instead.
- **OpenCV needs `libgl1` and `libglib2.0-0t64`** on Streamlit Cloud's Debian `trixie` base image — add these via `packages.txt`.
- **SFace and ArcFace embeddings are not interchangeable** (128-d vs 512-d) — mixing them in the same database causes a `cv2.error: Sizes of input arguments do not match`.
- **Streamlit secrets vs `.env`** — `st.secrets` (used by `db.py`) is separate from `os.getenv()`; local development needs a `.streamlit/secrets.toml` file even if `.env` also exists.
- Model `.onnx` files must be downloaded as raw binary — GitHub's LFS-tracked files can silently download as small pointer files if not fetched correctly.
