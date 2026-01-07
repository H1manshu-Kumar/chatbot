# 🤖 AI Assistant

> **Intelligent Data Assistant** - Upload your data files and chat with your data using AI

A modern, responsive web application that transforms your spreadsheet data into an interactive chatbot experience. Simply upload your Excel files and start asking questions in natural language.

## ✨ Features

- 🎯 **Smart Data Search** - Ask questions in natural language
- 📊 **Excel File Support** - Works with .xlsx and .xls files
- 🎨 **Modern UI** - Beautiful, responsive design with gradient themes
- 🔐 **Secure Login** - Session-based authentication
- 📱 **Mobile Friendly** - Works perfectly on all devices
- ⚡ **Real-time Chat** - Instant responses with typing indicators
- 🔍 **Intelligent Matching** - Advanced keyword-based search

## 🚀 Quick Start

### Option 1: Frontend Only
```bash
# Clone the repository
git clone <your-repo-url>
cd ai-assistant

# Open in browser
open login.html
# or
python -m http.server 8000
```

### Option 2: Full Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run minimal version (no LLM required)
uvicorn minimal_main:app --reload --host 0.0.0.0 --port 8000

# OR run with OpenAI integration
export OPENAI_API_KEY="your-api-key"
uvicorn rag_main:app --reload --host 0.0.0.0 --port 8000
```

## 🎮 How to Use

1. **Login**: Use demo credentials (`admin` / `password`)
2. **Upload Data**: Drag & drop your Excel file or click to browse
3. **Start Chatting**: Ask questions about your data in natural language
4. **Get Answers**: Receive instant, relevant responses

## 📋 Demo Credentials

- **Username**: `admin`
- **Password**: `password`

## 📊 Example Queries

Try these sample questions with the included `example.xlsx`:

- What are your business hours?
- How do I reset my password?
- What is your return policy?
- Do you offer free shipping?

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Data Processing**: SheetJS (xlsx library)
- **Backend**: FastAPI, Python

## 📁 Project Structure

```
ai-assistant/
├── login.html          # Login page
├── dashboard.html      # Main chat interface
├── example.xlsx        # Sample data file
├── backend/            # Optional backend services
├── frontend/           # Additional frontend assets
└── README.md          # This file
```

## 🎨 Screenshots

### Login Page
Clean, modern login interface with gradient design

### Dashboard
Interactive chat interface with file upload and real-time messaging

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
---

⭐ **Star this repo** if you find it helpful!

Made with ❤️ for the developer community
