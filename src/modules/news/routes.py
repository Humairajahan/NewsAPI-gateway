"""
Defines the API routes under the `/news` prefix to interact with the
NewsAPI through the `NewsAPIService`.
"""

from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from .schema import CategorySchema, LanguageSchema, CountrySchema
from .service import NewsAPIService
from ...common.jwt_auth_guard import get_user
from ...utils.dependencies import get_db


router = APIRouter(prefix="/news", tags=["News"])


@router.get("")
async def fetch_all(
    domains: str = "bbc.co.uk",
    skip: int = 1,
    limit: int = 100,
    token: HTTPAuthorizationCredentials = Depends(get_user),
):
    """
    Fetch all news with pagination support
    """
    return await NewsAPIService().fetch_all(domains=domains, skip=skip, limit=limit)


@router.post("/save-latest")
async def fetch_save_latest(
    domains: str = "bbc.co.uk",
    skip: int = 1,
    token: HTTPAuthorizationCredentials = Depends(get_user),
    session: AsyncSession = Depends(get_db),
):
    """
    Fetch the latest news and save the top 3
    """
    return await NewsAPIService().fetch_save_latest(
        db=session, skip=skip, domains=domains
    )


@router.get("/headlines/country/{country_code}")
async def fetch_headlines_by_country(
    country_code: CountrySchema,
    skip: int = 1,
    limit: int = 3,
    token: HTTPAuthorizationCredentials = Depends(get_user),
):
    """
    Fetch top headlines by country code
    """
    return await NewsAPIService().fetch_headlines_by_country(
        country_code=country_code, skip=skip, limit=limit
    )


@router.get("/headlines/source/{source_id}")
async def fetch_headlines_by_source(
    source_id: str,
    skip: int = 1,
    limit: int = 100,
    token: HTTPAuthorizationCredentials = Depends(get_user),
):
    """
    Fetch top headlines by source id
    """
    return await NewsAPIService().fetch_headlines_by_source(
        source_id=source_id, skip=skip, limit=limit
    )


@router.get("/sources")
async def fetch_sources(
    category: Optional[CategorySchema] = None,
    language: Optional[LanguageSchema] = None,
    country_code: Optional[CountrySchema] = None,
    token: HTTPAuthorizationCredentials = Depends(get_user),
):
    """
    Fetch all sources
    """
    return await NewsAPIService().fetch_sources(
        category=category, language=language, country_code=country_code
    )
