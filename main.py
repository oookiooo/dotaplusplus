import pathlib

from fastapi import FastAPI, Request, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import db

db.Base.metadata.create_all(db.engine)


def get_session():
    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


app = FastAPI()

ROOT_DIR = pathlib.Path.cwd()
app.mount("/static", StaticFiles(directory=ROOT_DIR / "static"), name="static")
templates = Jinja2Templates(directory=ROOT_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.email = {"value": "", "error": None}
        self.password = {"value": "", "error": None}

    async def load_data(self):
        form = await self.request.form()
        self.email["value"] = form.get("email")
        self.password["value"] = form.get("password")

    async def is_valid(self):
        if not self.email["value"]:
            self.email["error"] = "Invalid email"
        if not self.password["value"]:
            self.password["error"] = "Invalid password"
        if not self.email["error"] and not self.password["error"]:
            return True
        return False


@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    form_data = {
        "email": {"value": "", "error": None},
        "password": {"value": "", "error": None}
    }
    return templates.TemplateResponse("login.html", {
        "request": request,
        "form_data": form_data
    })


@app.post("/login", response_class=HTMLResponse)
async def handle_login(request: Request):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response: Response = templates.TemplateResponse(
                "login-form.html",
                {"request": request, "form_data": form.__dict__}
            )
            response.set_cookie(key="accessToken",
                                value="jakis-access-token-123")
            response.headers["HX-Redirect"] = "/"
            return response
        except HTTPException:
            return templates.TemplateResponse(
                "login-form.html",
                {"request": request, "form_data": form.__dict__}
            )
    return templates.TemplateResponse(
        "login-form.html",
        {"request": request, "form_data": form.__dict__}
    )


@app.get("/register", response_class=HTMLResponse)
async def read_register(request: Request):
    form_data = {
        "email": {"value": ""},
        "password": {"value": ""}
    }
    return templates.TemplateResponse("register.html", {
        "request": request,
        "form_data": form_data,
    })


@app.post("/register", response_class=HTMLResponse)
async def handle_register(request: Request):
    form_data = {
        "email": {"value": ""},
        "password": {"value": ""}
    }
    return templates.TemplateResponse("register-form.html", {
        "request": request,
        "form_data": form_data,
    })
