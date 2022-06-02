from fastapi import FastAPI, HTTPException, status, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import endpoints
from core import exceptions
from db.engine import database

app = FastAPI()
app.include_router(endpoints.auth.router, prefix='/auth', tags=['Authentication'])
app.include_router(endpoints.users.router, prefix='/users', tags=['Users'])
app.include_router(endpoints.quizzes.router, prefix='/quizzes', tags=['Quizzes'])
app.include_router(endpoints.helper.router, prefix='/help', tags=['Helpers'])

origins = [
    'http://localhost',
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def on_startup():
    await database.connect()


@app.on_event('shutdown')
async def on_shutdown():
    await database.disconnect()


@app.exception_handler(exceptions.UserDoesNotExist)
async def on_user_does_not_exist_error(
        request: Request,
        exception: exceptions.UserDoesNotExist,
):
    return JSONResponse({'detail': str(exception)}, status.HTTP_404_NOT_FOUND)


@app.exception_handler(exceptions.UserEmailAlreadyUsed)
async def on_user_email_already_used_error(
        request: Request,
        exception: exceptions.UserEmailAlreadyUsed,
):
    return JSONResponse({'detail': str(exception)}, status.HTTP_409_CONFLICT)
