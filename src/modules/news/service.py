"""
NewsAPI Service Module

This module defines the `NewsAPIService` class, which provides asynchronous methods
to interact with the NewsAPI (https://newsapi.org/). It includes functionality for:

- Fetching all articles based on domains
- Fetching and saving the latest top news
- Fetching headlines by country or source
"""

from typing import Optional
from datetime import datetime, timezone
import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import CategorySchema, LanguageSchema, CountrySchema
from .entity import NewsEntity
from ...config import NEWSAPI_API_KEY


class NewsAPIService:
    """
    Service class for interacting with the NewsAPI.

    This class provides methods to fetch news articles, headlines, and sources
    from the NewsAPI using asynchronous HTTP requests.
    """

    EVERYTHING_URL = "https://newsapi.org/v2/everything"
    SOURCES_URL = "https://newsapi.org/v2/top-headlines/sources"
    TOP_HEADLINES_URL = "https://newsapi.org/v2/top-headlines"
    HEADER = {"Authorization": NEWSAPI_API_KEY}

    def __init__(self):
        pass

    @staticmethod
    def parse_datetime(date: str) -> datetime:
        """
        Parses a string date from ISO format
        and returns a timezone-aware datetime object.
        """
        try:
            return datetime.fromisoformat(date.replace("Z", "+00:00"))
        except Exception:
            return datetime.utcnow().replace(tzinfo=timezone.utc)

    async def fetch_all(
        self, domains: str = "bbc.co.uk", skip: int = 1, limit: int = 100
    ):
        """
        Fetch all news with pagination support
        """
        params = {
            # "q"
            # "searchIn"
            # "sources"
            "domains": domains,
            "sortBy": "publishedAt",
            "pageSize": limit,
            "page": skip,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.EVERYTHING_URL, headers=self.HEADER, params=params
            )
            return response.json()

    async def fetch_save_latest(
        self,
        db: AsyncSession,
        domains: str = "bbc.co.uk",
        skip: int = 1,
    ):
        """
        Fetch the latest news and save the top 3
        """
        params = {
            # "q"
            # "searchIn"
            # "sources"
            "to": datetime.utcnow(),
            "sortBy": "publishedAt",
            "pageSize": 3,
            "page": skip,
        }
        if domains:
            params["domains"] = domains
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.EVERYTHING_URL, headers=self.HEADER, params=params
            )
        if response.status_code != 200:
            raise HTTPException(
                status_code=400, detail="Failed to fetch the latest news"
            )
        data = response.json()

        articles = data.get("articles", [])

        for article in articles:
            news = NewsEntity(
                author=article.get("author", "") or "Unknown",
                title=article.get("title", ""),
                description=article.get("description", "") or "",
                url=article.get("url", ""),
                urlToImage=article.get("urlToImage", ""),
                publishedAt=NewsAPIService.parse_datetime(
                    article.get("publishedAt", datetime.utcnow().isoformat())
                ),
                content=article.get("content", "") or "",
            )
            db.add(news)
        await db.commit()
        return data

    async def fetch_headlines_by_country(
        self, country_code: CountrySchema, skip: int = 1, limit: int = 100
    ):
        """
        Fetch top headlines by country code
        """
        params = {"country": country_code.value, "pageSize": limit, "page": skip}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.TOP_HEADLINES_URL, headers=self.HEADER, params=params
            )
            return response.json()

    async def fetch_headlines_by_source(
        self, source_id: str = "bbc-news", skip: int = 1, limit: int = 100
    ):
        """
        Fetch top headlines by source id
        """
        params = {"sources": source_id, "pageSize": limit, "page": skip}
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.TOP_HEADLINES_URL, headers=self.HEADER, params=params
            )
            return response.json()

    async def fetch_sources(
        self,
        category: Optional[CategorySchema] = None,
        language: Optional[LanguageSchema] = None,
        country_code: Optional[CountrySchema] = None,
    ):
        """
        Fetch all sources
        """
        params = {}
        if category:
            params["category"] = category.value
        if language:
            params["language"] = language.value
        if country_code:
            params["country"] = country_code.value

        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.SOURCES_URL, headers=self.HEADER, params=params
            )
            return response.json()
