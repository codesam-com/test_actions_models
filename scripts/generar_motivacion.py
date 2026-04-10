import os, json, urllib.request, datetime, pathlib, re

API_URL = "https://models.github.ai/inference/chat/completions"
TOKEN = os.getenv("GITHUB_TOKEN")
MODEL = os.getenv("MODEL_ID", "meta/meta-llama-3.1-8b-instruct")
OUTPUT = os.getenv("OUTPUT_FILE", "data/motivacion.log")

def limpiar(texto: str) -> str:
    if not texto:
        return ""
    texto = texto.replace("\n", " ").replace("\r", " ")
    texto = re.sub(r"\s+", " ", texto).strip()
    texto = texto.strip('"“”\' ')
    return texto

prompt = {
    "model": MODEL,
    "messages": [
        {
            "role": "system",
            "content": "Genera una única frase motivadora en español, corta, clara y sin comillas."
        },
        {
            "role": "user",
            "content": "Una frase motivadora."
        }
    ],
    "max_tokens": 60,
    "temperature": 0.9
}

req = urllib.request.Request(
    API_URL,
    data=json.dumps(prompt).encode(),
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github+json"
    }
)

try:
    with urllib.request.urlopen(req, timeout=30) as res:
        data = json.loads(res.read().decode())
        text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        text = limpiar(text)

        if not text or len(text) < 10:
            text = "Sigue avanzando, incluso cuando parezca difícil."

except Exception as e:
    print("Error:", e)
    text = "Sigue avanzando, incluso cuando parezca difícil."

timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
line = f"[{timestamp}] {text}"

path = pathlib.Path(OUTPUT)
path.parent.mkdir(parents=True, exist_ok=True)

with open(path, "a", encoding="utf-8") as f:
    f.write(line + "\n")

print(line)
