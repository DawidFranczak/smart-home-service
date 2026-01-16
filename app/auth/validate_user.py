from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

from app.models.user import UserModel
from app.settings.access_token import AccessTokenPublicKey
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
public_key = AccessTokenPublicKey().PUBLIC_KEY


def get_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserModel:
    try:
        data = jwt.decode(token, public_key, algorithms=["RS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = data.get("user_id")
    home_id = data.get("home_id")
    if not user_id or not home_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    if not isinstance(user_id, int) or not isinstance(home_id, int):
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return UserModel(id=user_id, home_id=home_id)


User = Annotated[UserModel, Depends(get_user)]
