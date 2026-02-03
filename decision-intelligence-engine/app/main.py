from fastapi import FastAPI

app = FastAPI(title="ScriptMyNetwork – Organizational Memory")

@app.get("/")
def health():
    return {"status": "ok"}
