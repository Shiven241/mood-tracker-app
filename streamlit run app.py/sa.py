# FastAPI backend for AI Mood Tracker

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

# OPTIONAL: Replace with your real OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY") or "sk-your-api-key"

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data model
class MoodEntry(BaseModel):
    mood_score: int
    journal_text: str

# GPT prompt template
def generate_prompt(entry: MoodEntry):
    return (
        f"A user rated their mood as {entry.mood_score}/10 today. "
        f"They wrote: '{entry.journal_text}'.\n"
        f"Summarize their emotional state in 2 sentences and suggest 1 helpful tip."
    )

@app.post("/analyze")
async def analyze_mood(entry: MoodEntry):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a supportive mental health assistant."},
                {"role": "user", "content": generate_prompt(entry)}
            ]
        )
        summary = response.choices[0].message.content.strip()
        return {"summary": summary}
    except Exception as e:
        return {"summary": "Error generating AI response.", "error": str(e)}


// === FILE: frontend/src/App.jsx ===
import React, { useState } from 'react';
import './App.css';

function App() {
  const [mood, setMood] = useState(5);
  const [journal, setJournal] = useState('');
  const [aiResponse, setAiResponse] = useState('');
  const [loading, setLoading] = useState(false);

  const submitMood = async () => {
    setLoading(true);
    const res = await fetch('http://localhost:8000/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ mood_score: mood, journal_text: journal })
    });
    const data = await res.json();
    setAiResponse(data.summary);
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-r from-purple-200 to-blue-200 flex flex-col items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-6 w-full max-w-md">
        <h1 className="text-2xl font-bold text-center mb-4">AI Mood Tracker</h1>
        <label className="block mb-2 font-semibold">Mood (1-10): {mood}</label>
        <input
          type="range"
          min="1"
          max="10"
          value={mood}
          onChange={e => setMood(parseInt(e.target.value))}
          className="w-full mb-4"
        />
        <textarea
          value={journal}
          onChange={e => setJournal(e.target.value)}
          placeholder="Write how you're feeling..."
          className="w-full p-2 border border-gray-300 rounded mb-4"
          rows={4}
        ></textarea>
        <button
          onClick={submitMood}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 w-full"
          disabled={loading}
        >
          {loading ? 'Analyzing...' : 'Submit'}
        </button>
        {aiResponse && (
          <div className="mt-4 p-3 bg-gray-100 rounded shadow">
            <p><strong>AI Summary:</strong></p>
            <p>{aiResponse}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;


// === FILE: frontend/src/index.js ===
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);


// === FILE: frontend/src/index.css ===
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}


// === FILE: frontend/tailwind.config.js ===
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [],
  
};