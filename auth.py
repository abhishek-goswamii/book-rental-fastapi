from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session 
import database
import schemas
import models
router = APIRouter(tags=['authentication'])
import utils
import oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

@router.post('/login',response_model=schemas.Token)
def login(user_credential:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(database.get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")

    verify = utils.comparePassword(user_credential.password, user.password)

    if not verify:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token,"token_type":"bearer"}


