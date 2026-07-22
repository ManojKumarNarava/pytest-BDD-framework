from typing import Any, Optional

import requests
from requests import Response


class APIClient:
    """Reusable client for sending REST API requests."""

    def __init__(self, base_url: str, timeout: int = 15) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

        self.session = requests.Session()

        self.session.headers.update(
            {
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def build_url(self, endpoint: str) -> str:
        """Build a complete API URL."""

        return f"{self.base_url}/{endpoint.lstrip('/')}"

    def get(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
    ) -> Response:
        """Send a GET request."""

        return self.session.get(
            self.build_url(endpoint),
            params=params,
            timeout=self.timeout,
        )

    def post(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> Response:
        """Send a POST request."""

        return self.session.post(
            self.build_url(endpoint),
            json=payload,
            timeout=self.timeout,
        )

    def put(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> Response:
        """Send a PUT request."""

        return self.session.put(
            self.build_url(endpoint),
            json=payload,
            timeout=self.timeout,
        )

    def patch(
        self,
        endpoint: str,
        payload: dict[str, Any],
    ) -> Response:
        """Send a PATCH request."""

        return self.session.patch(
            self.build_url(endpoint),
            json=payload,
            timeout=self.timeout,
        )

    def delete(self, endpoint: str) -> Response:
        """Send a DELETE request."""

        return self.session.delete(
            self.build_url(endpoint),
            timeout=self.timeout,
        )

    def close(self) -> None:
        """Close the reusable HTTP session."""

        self.session.close()