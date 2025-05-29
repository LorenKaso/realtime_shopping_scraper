from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from scraper import scrape

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scrape")
def api_scrape(
    site: str = Query(..., description="amazon/bestbuy/walmart/newegg"),
    query: str = Query(..., description="Product name")
):
    return scrape(site, query)
