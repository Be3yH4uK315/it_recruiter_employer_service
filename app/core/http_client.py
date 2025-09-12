import httpx
from app.core.config import CANDIDATE_SERVICE_URL

class CandidateHttpClient:
    def __init__(self, base_url: str = CANDIDATE_SERVICE_URL):
        self.base_url = base_url

    async def get_candidate_profile(self, candidate_id: str) -> dict | None:
        async with httpx.AsyncClient(
                http2=False, trust_env=False, timeout=10.0
        ) as client:
            try:
                response = await client.get(f"{self.base_url}/candidates/{candidate_id}")
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                print(f"Request error: {e}")
                return None
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    return None
                raise

http_client = CandidateHttpClient()