from fastapi import FastAPI, Request, Form
from starlette.middleware.sessions import SessionMiddleware
import secrets
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import random

app = FastAPI()

# Add a session middleware with a secret key
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(16))

# Set up the templates directory
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Our "secret" number (later we could randomize this!)

@app.get("/", response_class=HTMLResponse)
async def guess_form(request: Request):
    # If this is a new session, pick a number
    if "secret_number" not in request.session:
        request.session["secret_number"] = random.randint(1, 10)
        print("Secret number for session:", request.session["secret_number"])  # optional: debug

    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def handle_guess(request: Request, number: int = Form(...)):
    secret = request.session.get("secret_number")
    if secret is None:
        message = "Something went wrong — no number set!"
        link_text = "Start Over"
    elif number < secret:
        message = f"Too low! You guessed {number}."
        link_text = "Try again"
    elif number > secret:
        message = f"Too high! You guessed {number}."
        link_text = "Try again"
    else:
        message = f"🎉 Correct! The number was {secret}."
        link_text = "Play again"
         # Reset the number for a new round
        request.session["secret_number"] = random.randint(1, 10)
        print("Secret number for session:", request.session["secret_number"])  # optional: debug

    return templates.TemplateResponse("result.html", {
        "request": request,
        "message": message,
        "guess": number,
        "link_text": link_text,
    })