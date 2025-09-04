# ArxivMind Backend 🧠

**AI-powered research paper analysis and visualization backend using FastAPI and Hugging Face models.**

## 🚀 Features

- **PDF Parsing**: Extract text from research papers using multiple parsing methods
- **AI Analysis**: LLM-powered paper analysis using Hugging Face models
- **Data Visualization**: Generate interactive charts and graphs from analysis results
- **RESTful API**: Clean, documented API endpoints for easy integration
- **Async Processing**: High-performance asynchronous request handling

## 🏗️ Architecture

```
backend/
├── main.py                 # FastAPI application entry point
├── services/              # Core service modules
│   ├── pdf_parser.py      # PDF text extraction service
│   ├── llm_analyzer.py    # AI analysis service
│   └── data_visualizer.py # Chart generation service
└── requirements.txt       # Backend dependencies
```

## 🔧 Setup

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Set Environment Variables
```bash
# Set your Hugging Face token
export HF_TOKEN="your_huggingface_token_here"
```

### 3. Run the Backend
```bash
python run_backend.py
```

## 📡 API Endpoints

### Core Endpoints
- `GET /` - API information and available endpoints
- `GET /health` - Health check endpoint
- `POST /upload-paper` - Upload and parse PDF papers
- `POST /analyze-paper` - Analyze paper content using AI
- `POST /visualize-data` - Generate data visualizations
- `GET /get-insights` - Get AI-generated insights

### API Documentation
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧪 Testing

### Run Backend Tests
```bash
python test_backend.py
```

### Manual Testing
1. Start the backend server
2. Open `http://localhost:8000/docs` in your browser
3. Use the interactive API documentation to test endpoints

## 🔑 Hugging Face Integration

### Required Token Permissions
- ✅ "Make calls to Inference Providers"
- ✅ "Read access to contents of all repos under your personal namespace"

### Supported Models
- **Summarization**: `facebook/bart-large-cnn`
- **Text Generation**: `microsoft/DialoGPT-medium`
- **Question Answering**: `deepset/roberta-base-squad2`
- **Sentiment Analysis**: `cardiffnlp/twitter-roberta-base-sentiment-latest`

## 📊 Data Visualization

### Chart Types
- Bar charts (summary analysis, word frequency)
- Horizontal bar charts (key points)
- Pie charts (methodology analysis)
- Radar charts (metadata overview)
- Custom charts (line, scatter, heatmap)

### Color Schemes
- Professional scientific color palette
- Multiple template options (simple, dark, scientific)

## 🚀 Performance Features

- **Async Processing**: Non-blocking request handling
- **Multiple PDF Parsers**: Fallback parsing methods for reliability
- **Content Truncation**: Smart text truncation for API limits
- **Error Handling**: Comprehensive error handling and logging
- **Retry Logic**: Automatic retry for model loading delays

## 🔍 Troubleshooting

### Common Issues

1. **PDF Parsing Fails**
   - Ensure PDF is not password-protected
   - Check if PDF contains extractable text (not just images)

2. **LLM Analysis Fails**
   - Verify Hugging Face token is valid
   - Check token permissions include "Inference"
   - Ensure models are accessible

3. **Visualization Errors**
   - Check if analysis data is available
   - Verify Plotly installation

### Logs
- Check console output for detailed error messages
- Enable debug logging for troubleshooting

## 🔮 Future Enhancements

- **Batch Processing**: Process multiple papers simultaneously
- **Advanced NLP**: Integration with spaCy for better text analysis
- **Custom Models**: Support for user-uploaded models
- **Caching**: Redis integration for improved performance
- **Authentication**: JWT-based user authentication
- **Rate Limiting**: API rate limiting and quotas

## 📝 License

This project is part of ArxivMind and follows the same license terms.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

**Built with ❤️ using FastAPI, Hugging Face, and modern Python practices.**
