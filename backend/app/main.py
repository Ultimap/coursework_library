from fastapi import FastAPI
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from app.routes.books import books
from app.routes.authors import authors
from app.routes.style import styles
from app.routes.auth import auth
from app.routes.users_books import user_book
from app.routes.accounting import accounting
from app.settings import upload_img
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/img/{img}', status_code=200)
async def get_img(img: str):
    return FileResponse(f'{upload_img}/{img}')


app.include_router(books)
app.include_router(authors)
app.include_router(styles)
app.include_router(auth)
app.include_router(user_book)
app.include_router(accounting)


