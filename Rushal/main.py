from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def root():
    return {"message": "AI Interview API"}

@app.post("/interview/")
async def interview(audio_text: str):
    # Call Ollama here
    return {"response": "AI analysis..."}