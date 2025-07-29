# 🏥 Rxplain Backend - Medical AI Assistant

A FastAPI-based medical AI assistant backend that provides safe, educational medical information using Google Gemini and OpenAI GPT models.

## 🚀 Features

- **Medical AI Assistant**: Professional medical information and guidance
- **Dual AI Support**: Google Gemini (default) + OpenAI GPT (optional)
- **Image Analysis**: Upload prescription images for medication identification and analysis
- **Safety First**: Comprehensive safety warnings and medical disclaimers
- **Query Classification**: Automatic detection of medical query types
- **Structured Responses**: Well-formatted medical information
- **API Key Management**: Secure handling of AI service API keys
- **Health Monitoring**: Built-in health check endpoints

## 📋 Requirements

- Python 3.8+
- Google Gemini API Key (required)
- OpenAI API Key (optional, for GPT model)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   cd fast-backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   ```
   
   Edit `.env` file with your API keys:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the application**
   ```bash
   python run.py
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes | - |
| `OPENAI_API_KEY` | OpenAI API key | No | - |
| `HOST` | Server host | No | 0.0.0.0 |
| `PORT` | Server port | No | 8000 |
| `DEBUG` | Debug mode | No | True |

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### POST `/api/chat`
Chat with the medical AI assistant (supports text and image uploads).

**Request (FormData):**
```
prompt: "What medications are in this prescription?"
model: "gemini"
api_key: "optional_openai_key" (for GPT model)
image: [image file] (optional, max 5MB)
```

**Response:**
```json
{
  "response": "Medical information...",
  "model": "gemini",
  "is_medical_query": true,
  "conversation_id": "unique_conversation_id",
  "medical_context": {}
}
```

**Image Upload Features:**
- **Supported formats**: JPEG, PNG, GIF, WebP
- **Size limit**: 5MB maximum
- **Use cases**: Prescription analysis, medication identification, medical document review
- **Safety**: Educational information only, no diagnostic interpretations

#### POST `/api/validate-api-key`
Validate OpenAI API key.

**Request Body:**
```json
{
  "api_key": "sk-...",
  "model": "gpt"
}
```

#### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Rxplain Medical AI Assistant",
  "version": "1.0.0",
  "models": {
    "gemini": "Available",
    "gpt": "Available (requires API key)"
  }
}
```

#### GET `/api/medical-keywords`
Get medical keywords for frontend validation.

## 🏗️ Project Structure

```
fast-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── routes/
│   │   ├── __init__.py
│   │   └── chat.py          # Chat API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini.py        # Google Gemini service
│   │   └── gpt.py           # OpenAI GPT service
│   └── utils/
│       ├── __init__.py
│       ├── medical_prompts.py  # Medical prompt templates
│       └── formatter.py        # Response formatting utilities
├── requirements.txt
├── run.py
├── env.example
└── README.md
```

## 🔒 Safety Features

### Medical Safety Guidelines
- **Never provides medical diagnoses**
- **Never recommends specific treatments or dosages**
- **Always encourages consulting healthcare professionals**
- **Includes appropriate safety warnings**
- **Clear disclaimers on every response**

### Image Analysis Safety
- **Educational information only**: No diagnostic interpretations
- **Prescription analysis**: Identify medications and provide general information
- **Safety disclaimers**: Always include appropriate warnings
- **Professional consultation**: Always recommend consulting healthcare providers
- **No medical advice**: Images are for educational purposes only

### Query Classification
- **Medication queries**: Drug information, side effects, interactions
- **Symptom queries**: Symptom analysis, red flags, when to seek help
- **General health**: Wellness, prevention, lifestyle advice
- **Emergency detection**: Automatic emergency response guidance

## 🚨 Emergency Handling

The system automatically detects emergency-related queries and provides appropriate guidance:

- **Emergency keywords**: chest pain, difficulty breathing, severe symptoms
- **Automatic warnings**: Emergency disclaimers and immediate action guidance
- **Professional referral**: Always directs to emergency services when appropriate

## 🧪 Testing

### Manual Testing
```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test chat endpoint
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is Aspirin?", "model": "gemini"}'
```

### Example Queries
- "What is Metformin used for?"
- "Side effects of Ibuprofen"
- "Can I take Aspirin with blood pressure medication?"
- "What are the symptoms of diabetes?"
- "How to manage stress and anxiety?"

### Image Upload Examples
- Upload prescription image: "What medications are in this prescription?"
- Upload pill image: "What pill is this?"
- Upload medical document: "Explain this lab report"
- Upload symptom image: "What could this rash be?" (with safety disclaimers)

## 🔧 Development

### Running in Development Mode
```bash
python run.py
```

### Running with Uvicorn
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive API documentation.

## 📝 Logging

The application includes comprehensive logging:
- Request/response logging
- Error tracking
- Medical query classification logging
- API key validation logging

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

**Medical Disclaimer**: This AI assistant provides educational information only and should not replace professional medical advice. Always consult healthcare professionals for medical decisions.

## 🆘 Support

For support or questions:
- Check the API documentation at `/docs`
- Review the health endpoint at `/api/health`
- Ensure your API keys are properly configured 