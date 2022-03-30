from fastapi import FastAPI,Depends,status, Request
from fastapi.responses import RedirectResponse,HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager #Loginmanager Class
from fastapi_login.exceptions import InvalidCredentialsException #Exception class
from fastapi.templating import Jinja2Templates

app= FastAPI()

SECRET = "cb93455406156db1326efcb6c3420394faace244b45b9161"
# To obtain a suitable secret key you can run | import os; print(os.urandom(24).hex())
templates = Jinja2Templates(directory="templates")

manager = LoginManager(SECRET,token_url="/auth/login",use_cookie=True)
manager.cookie_name = "some-name"

DB = {"aamirshuaib":{"password":"Optimal.01"},
      "salmankhan":{"password":"Optimal.01"},
      "shubhamverma":{"password":"Optimal.01"},
      "nisheethsoni":{"password":"Optimal.01"}}

@manager.user_loader
def load_user(username:str):
    user = DB.get(username)
    return user

@app.post("/auth/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    username = data.username
    password = data.password
    user = load_user(username)
    if not user:
        raise InvalidCredentialsException
    elif password != user['password']:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(
        data={"sub":username}
    )
    resp = RedirectResponse(url="/private",status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp,access_token)
    return resp

@app.get("/private")
def getPrivateendpoint(_=Depends(manager)):
    return "You are an authentciated user"

@app.get("/",response_class=HTMLResponse)
def loginwithCreds(request:Request):
    return templates.TemplateResponse("login_page.html", {'request': request})