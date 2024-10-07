import os
from fastapi import HTTPException, Header, status
import jwt


def auth_middleware(x_auth_token: str = Header()):
    try:
        #get the user token from the header's
        if not x_auth_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No auth token, Access Denied"
            )
        #validate the token
        verified_token = jwt.decode(x_auth_token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])

        if not verified_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token verification failed, Autherization Denied"
            )
        #get the id from the token
        uid = verified_token.get("id")
        return {'uid': uid, 'token': x_auth_token}
        #postgress database get the user information
    except jwt.PyJWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token verification failed, Autherization Denied"
        )