import unittest
from unittest.mock import patch, AsyncMock, Mock
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.news.service import NewsAPIService
from src.modules.news.schema import CountrySchema, CategorySchema, LanguageSchema


class TestNewsAPIService(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.service = NewsAPIService()
        self.db = AsyncMock(spec=AsyncSession)

    @patch("src.modules.news.service.httpx.AsyncClient")
    async def test_fetch_all_success(self, mock_client_class):
        # Setup mock client and response
        mock_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok"}

        # Assign mock to context manager
        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client

        # Call the method
        result = await self.service.fetch_all()
        self.assertEqual(result["status"], "ok")

    @patch("src.modules.news.service.httpx.AsyncClient")
    async def test_fetch_save_latest_success(self, mock_client_class):
        mock_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "ok",
            "articles": [
                {
                    "author": "John Doe",
                    "title": "Sample News",
                    "description": "Description",
                    "url": "https://example.com",
                    "urlToImage": "https://image.com",
                    "publishedAt": "2024-04-01T00:00:00Z",
                    "content": "Sample content",
                }
            ],
        }

        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client

        result = await self.service.fetch_save_latest(self.db)
        self.assertEqual(result["status"], "ok")
        self.db.add.assert_called_once()
        self.db.commit.assert_awaited_once()

    @patch("src.modules.news.service.httpx.AsyncClient")
    async def test_fetch_save_latest_failure(self, mock_client_class):
        mock_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {}

        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client

        with self.assertRaises(HTTPException):
            await self.service.fetch_save_latest(self.db)
    
    @patch("src.modules.news.service.httpx.AsyncClient")
    async def test_fetch_headlines_by_country_success(self, mock_client_class):
        mock_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"status": "ok", "country": "us"}

        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client

        result = await self.service.fetch_headlines_by_country(CountrySchema.US)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["country"], "us")
        mock_client.get.assert_awaited_once()

    @patch("src.modules.news.service.httpx.AsyncClient")
    async def test_fetch_headlines_by_source_success(self, mock_client_class):
        mock_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "ok",
            "source": "bbc-news"
        }

        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client

        result = await self.service.fetch_headlines_by_source(source_id="bbc-news")
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["source"], "bbc-news")
        mock_client.get.assert_awaited_once()

    @patch("src.modules.news.service.httpx.AsyncClient")
    async def test_fetch_sources_with_all_filters(self, mock_client_class):
        mock_client = AsyncMock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "ok",
            "sources": []
        }

        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client

        result = await self.service.fetch_sources(
            category=CategorySchema.TECHNOLOGY,
            language=LanguageSchema.EN,
            country_code=CountrySchema.US
        )
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["sources"], [])
        mock_client.get.assert_awaited_once()