from fastapi import FastAPI,UploadFile,File
from fastapi.middleware.cors import CORSMiddleware
import whisper,tempfile,requests,pyttsx3

app=FastAPI()

app.add_middleware(
 CORSMiddleware,
 allow_origins=["*"],
 allow_methods=["*"],
 allow_headers=["*"]
)

m=whisper.load_model("base")
engine=pyttsx3.init()

@app.post("/voice")
async def voice(f:UploadFile=File(...)):
 b=await f.read()
 t=tempfile.NamedTemporaryFile(delete=False,suffix=".wav")
 t.write(b);t.close()

 tx=m.transcribe(t.name)["text"]

 ll=requests.post(
  "http://localhost:11434/api/generate",
  json={"model":"llama3","prompt":tx,"stream":False}
 ).json()["response"]

 out=t.name+"_reply.wav"
 engine.save_to_file(ll,out)
 engine.runAndWait()

 return {"reply":ll,"audio":open(out,"rb").read().hex()}
