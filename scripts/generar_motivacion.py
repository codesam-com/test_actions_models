import os, json, urllib.request, datetime, pathlib

API_URL = "https://models.github.ai/inference/chat/completions"
TOKEN = os.getenv("GITHUB_TOKEN")
MODEL = os.getenv("MODEL_ID", "meta/meta-llama-3.1-8b-instruct")
OUTPUT = os.getenv("OUTPUT_FILE", "data/motivacion.log")

prompt = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "Genera una frase motivadora corta en español."},
        {"role": "user", "content": "Una frase motivadora."}
    ]
}

req = urllib.request.Request(
    API_URL,
    data=json.dumps(prompt).encode(),
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
)

try:
    res = urllib.request.urlopen(req)
    data = json.loads(res.read().decode())
    text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
except:
    text = "Sigue adelante, incluso cuando cueste."

line = f"[{datetime.datetime.utcnow()}] {text.strip()}"

path = pathlib.Path(OUTPUT)
path.parent.mkdir(parents=True, exist_ok=True)
with open(path, "a", encoding="utf-8") as f:
    f.write(line + "\n")

print(line)
