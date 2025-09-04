# 🧠 ArXiv Mind - AI-Powered Research Paper Analysis

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-API-purple.svg)](https://openrouter.ai/)

An intelligent research assistant that leverages RAG (Retrieval Augmented Generation) and free AI models to analyze, compare, and extract insights from research papers.

## 🌟 Features

### Core Capabilities
- **📄 Paper Analysis**: Deep analysis of research papers using Mistral AI
- **🔍 Smart Search**: Search and discover relevant papers from arXiv
- **📊 Comparative Analysis**: Compare multiple papers side-by-side
- **💡 Insight Generation**: Extract key insights and research directions
- **📝 PDF Processing**: Upload and analyze PDF research papers
- **🎯 RAG-Powered**: Context-aware responses using vector similarity

### AI Models Used
- **Mistral Small 3.1 24B** (Free) - Primary analysis model
- **Nous DeepHermes 3 Llama 3.8B** (Free) - Alternative model
- **Sentence Transformers** - For embeddings generation
- **ChromaDB** - Vector database for similarity search

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Windows 10/11 (tested environment)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AnirudhNarayan/ArXiv-Mind-Gen-AI-App.git
   cd ArXiv-Mind-Gen-AI-App
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv "arXiv Mind"
   # Activate on Windows
   "arXiv Mind\Scripts\activate"
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure OpenRouter API** (Optional)
   - Get your free API key from [OpenRouter](https://openrouter.ai/)
   - Set environment variable: `OPENROUTER_KEY=your_api_key_here`

### Running the Application

#### Option 1: Full Stack (Recommended)
```bash
# Terminal 1 - Start Backend
cd backend
python -m uvicorn main:app --reload

# Terminal 2 - Start Frontend
cd frontend
streamlit run app.py
```

#### Option 2: Using Batch Files
```bash
# For full system
start_arxivmind.bat

# For simple version
start_simple_system.bat
```

#### Option 3: Individual Components
```bash
# Backend only
python run_backend.py

# Simple backend
python run_simple_backend.py

# Frontend only
start_frontend.bat
```

### Access Points
- **Frontend UI**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📁 Project Structure

```
ArXiv-Mind-Gen-AI-App/
├── 📁 backend/                 # FastAPI backend
│   ├── 📁 services/           # Core services
│   │   ├── rag_service.py     # RAG implementation
│   │   ├── vector_store.py    # ChromaDB integration
│   │   ├── paper_ingestion.py # arXiv paper processing
│   │   └── ...
│   ├── main.py               # Main FastAPI app
│   └── requirements.txt      # Backend dependencies
├── 📁 frontend/               # Streamlit frontend
│   ├── app.py                # Main Streamlit app
│   └── requirements.txt      # Frontend dependencies
├── 📁 data/                   # Data storage
│   └── vectordb/             # ChromaDB storage
├── 📄 requirements.txt        # Project dependencies
├── 📄 README.md              # This file
└── 🚀 start_*.bat           # Launch scripts
```

## 🔧 API Endpoints

### Core Endpoints
- `GET /health` - Health check
- `POST /analyze` - Analyze paper content
- `POST /compare` - Compare multiple papers
- `POST /insights` - Generate insights
- `POST /upload-paper` - Upload PDF files

### Paper Management
- `POST /papers/search` - Search arXiv papers
- `GET /papers/analyze/{paper_id}` - Analyze by ID
- `GET /papers/recent` - Get recent papers

## 🎯 Usage Examples

### 1. Analyze a Research Paper
```python
import requests

# Upload and analyze a paper
response = requests.post(
    "http://localhost:8000/analyze",
    json={
        "paper_content": "Your paper content here...",
        "paper_title": "Paper Title"
    }
)
analysis = response.json()
```

### 2. Compare Multiple Papers
```python
papers = [
    {"title": "Paper 1", "abstract": "Abstract 1..."},
    {"title": "Paper 2", "abstract": "Abstract 2..."}
]

response = requests.post(
    "http://localhost:8000/compare",
    json=papers
)
comparison = response.json()
```

### 3. Search arXiv Papers
```python
response = requests.post(
    "http://localhost:8000/papers/search",
    params={"query": "large language models", "max_results": 10}
)
papers = response.json()
```

## 🧪 Testing

Run the test suite to verify installation:

```bash
# Test backend
python test_backend.py

# Test simple system
python test_simple_system.py

# Test integration
python test_integration.py

# Test OpenRouter connection
python test_openrouter.py
```

## 🎨 Features in Detail

### RAG Implementation
- **Vector Storage**: ChromaDB for efficient similarity search
- **Embeddings**: Sentence-transformers for semantic understanding
- **Context Retrieval**: Find related papers automatically
- **Smart Analysis**: Context-aware paper analysis

### AI Models
- **Free Models**: Utilizes OpenRouter's free tier
- **Cost Optimization**: Intelligent token usage
- **Multi-Model**: Fallback options for reliability
- **GPU Support**: Optional CUDA acceleration

### User Interface
- **Streamlit Dashboard**: Intuitive web interface
- **Real-time Analysis**: Live paper processing
- **Comparative Views**: Side-by-side paper comparison
- **Export Options**: Save analysis results

## 🛠️ Configuration

### Environment Variables
```bash
OPENROUTER_KEY=your_openrouter_api_key
HF_TOKEN=your_huggingface_token (optional)
```

### Model Configuration
Edit `backend/services/rag_service.py` to customize:
- Model selection
- Token limits
- Response formats

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Requirements

### System Requirements
- **OS**: Windows 10/11, macOS, Linux
- **Python**: 3.11 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 2GB free space

### Key Dependencies
- `fastapi>=0.104.1` - Backend framework
- `streamlit>=1.28.1` - Frontend framework
- `chromadb>=0.4.22` - Vector database
- `sentence-transformers>=2.2.2` - Embeddings
- `arxiv>=2.2.0` - arXiv API client
- `requests>=2.31.0` - HTTP client

## 🐛 Troubleshooting

### Common Issues

1. **Backend not starting**
   ```bash
   # Check if port 8000 is in use
   netstat -an | findstr :8000
   
   # Kill existing processes
   taskkill /f /im python.exe
   ```

2. **Dependencies issues**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

3. **OpenRouter API issues**
   ```bash
   # Test API connection
   python test_openrouter.py
   ```

### Performance Tips
- Use GPU acceleration when available
- Limit paper length for faster processing
- Cache frequently accessed papers
- Monitor API usage to stay within limits

## 📚 Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenRouter API](https://openrouter.ai/docs)
- [ChromaDB Documentation](https://docs.trychroma.com/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenRouter](https://openrouter.ai/) for free AI model access
- [arXiv](https://arxiv.org/) for research paper database
- [Hugging Face](https://huggingface.co/) for transformer models
- [Streamlit](https://streamlit.io/) for the amazing web framework

## 📞 Support

- **GitHub Issues**: [Create an issue](https://github.com/AnirudhNarayan/ArXiv-Mind-Gen-AI-App/issues)
- **Email**: anidev0102@gmail.com
- **Documentation**: Check the `/docs` endpoint when running

---

**Made with ❤️ by [Anirudh Narayan](https://github.com/AnirudhNarayan)**

*Empowering researchers with AI-driven insights*