from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    userpwd_db = [{"username": "james_dey@hotmail.com", "password": "test"},
                 {"username": "scott", "password": "tiger"}]
    current_username_bytes = credentials.username.encode("utf8")
    current_password_bytes = credentials.password.encode("utf8")
    #Loop through all of the stored usernames and passwords to look for a match
    for index in range(len(userpwd_db)):
        user=userpwd_db[index]['username']
        pwd=userpwd_db[index]['password']
        is_correct_username = secrets.compare_digest(current_username_bytes, bytes(user,'utf-8'))
        is_correct_password = secrets.compare_digest(current_password_bytes, bytes(pwd, 'utf-8'))
        #If we've found a match then return the username
        if is_correct_username and is_correct_password:
            return credentials.username
    #If we've not found a match for the username & password then we need to raise an exception
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Basic"},
    )
