# CareMate-AI

**CareMate-AI** is an AI-powered healthcare chatbot built using Python and Streamlit.  
This project was developed during my internship at **Edunet Foundation**.

---

## 🚀 Setup Instructions

Follow the steps below to configure and run the project on your local machine — compatible with **Windows**, **macOS**, and **Linux (including Kali)**.

---

### 📋 Prerequisites

- Python **3.10+**
- Pip (Python package manager)
- Git (for cloning)
- Internet connection (to use the Gemini API)
- Streamlit

---

### 📦 Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/bhola-dev58/CareMate-AI.git
cd CareMate-AI
```

#### 2. Create a Virtual Environment (Recommended)

- **Linux/macOS**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Windows**:
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

---

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

#### 4. Configure the API Key

Create a `.env` file in the root directory of the project:

- **Linux/macOS**:
  ```bash
  touch .env
  ```

- **Windows**:
  ```cmd
  notepad .env
  ```

Then add the following line inside `.env`:

```env
GEMINI_API_KEY="Keep-Your-API-KEY-here"
```

Save and close the file.

---

### ▶️ Running the Application

To launch the chatbot:

```bash
streamlit run app.py
```

Once started, open your browser and go to:

```
http://localhost:8501
```

---

## ⚙️ Platform-Specific Notes

- ✅ **Windows**:
  - Run commands in **Command Prompt** or **PowerShell**
  - Make sure Python is added to your PATH

- ✅ **macOS**:
  - Use the built-in **Terminal**
  - Ensure you're using Python 3.10 or higher

- ✅ **Kali Linux / Ubuntu**:
  - If you face issues, install pip/venv using:
    ```bash
    sudo apt install python3-pip python3-venv
    ```

---

## 📌 Note

> 🔧 **Some new features are currently under development... Stay tuned for smarter healthcare conversations with CareMate-AI!**
