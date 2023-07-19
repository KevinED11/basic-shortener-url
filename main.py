from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import string
import random
from fastapi.responses import RedirectResponse

app = FastAPI()


class URL(BaseModel):
    long_url: str


url_mapping = {}
BASE_URL = "http://localhost:8000/"
CHARACTERS = string.ascii_letters + string.digits + string.punctuation


@app.post("/shorten/")
async def create_short_url(url: URL):
    short_url = ''.join(random.choices(CHARACTERS, k=5))
    url_mapping[short_url] = url.long_url

    return {"short_url": BASE_URL+short_url}


@app.get("/{short_url}", response_class=RedirectResponse)
async def redirect_short_url(short_url: str):
    if long_url := url_mapping.get(short_url): 
        return RedirectResponse(long_url, status_code=status.HTTP_302_FOUND)
            
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Short URL not found")
