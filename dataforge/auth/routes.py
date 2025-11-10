# TODO: Re-implement the token endpoint with a proper database backend.
# The following code is commented out because it depends on the removed fake_db.

# from fastapi import APIRouter, Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm
#
# from dataforge.auth import models, security
# from dataforge.db.fake_db import fake_users_db, get_user
#
# router = APIRouter()
#
# @router.post("/token", response_model=models.Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = get_user(fake_users_db, username=form_data.username)
#     if not user or not security.verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = security.create_access_token(
#         data={"sub": user.username}
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

from fastapi import APIRouter

router = APIRouter()
