# Orchids Website Cloner

A web application that uses AI to create pixel-perfect clones of any website. Built with Next.js, FastAPI, and Claude AI.

## Features

- Website scraping with BeautifulSoup
- AI-powered website cloning using Claude
- Real-time preview in a secure iframe
- Modern, responsive UI with Tailwind CSS

## Prerequisites

- Python 3.13 or higher
- Node.js 18 or higher
- Anthropic API key (for Claude AI)
- uv package manager

## Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment using uv:
```bash
uv venv
```

3. Create a `.env` file in the backend directory:
```bash
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
```
Replace `your_api_key_here` with your actual Anthropic API key.

4. Install dependencies using uv:
```bash
uv pip install -r requirements.txt
```

5. Start the backend server:
```bash
uv run uvicorn app.main:app --reload
```
The backend will be available at http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```
The frontend will be available at http://localhost:3000

## Usage

1. Open http://localhost:3000 in your browser
2. Enter a website URL in the input field
3. Click "Clone Website"
4. View the cloned website in the preview section

## API Documentation

Once the backend is running, you can access the API documentation at:
http://localhost:8000/docs (or http://localhost:8001/docs if you used a different port)

## Technical Details

- **Backend**: FastAPI with BeautifulSoup for scraping
- **Frontend**: Next.js with TypeScript and Tailwind CSS
- **AI**: Claude 3.5 Sonnet for HTML generation
- **Preview**: Secure iframe implementation

## Security Notes

- The application uses sandboxed iframes for secure preview
- API keys should never be committed to version control
- CORS is configured to only allow localhost during development
