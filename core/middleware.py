"""Custom middleware for the core application."""
import time
from collections import defaultdict
from threading import Lock
from typing import Callable

from django.http import HttpRequest, HttpResponse, JsonResponse


class RateLimitMiddleware:
    """Простой rate limiter для POST-запросов на основе IP.

    Ограничивает количество POST-запросов с одного IP.
    По умолчанию: 5 запросов в 60 секунд.
    """

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response
        self.requests: dict[str, list[float]] = defaultdict(list)
        self.lock = Lock()
        self.max_requests = 5
        self.window_seconds = 60

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Проверяет rate limit для POST-запросов."""
        if request.method == "POST":
            ip = self._get_client_ip(request)
            if not self._is_allowed(ip):
                return JsonResponse(
                    {"error": "Слишком много запросов. Попробуйте позже."},
                    status=429,
                )
        return self.get_response(request)

    def _get_client_ip(self, request: HttpRequest) -> str:
        """Извлекает IP клиента с учётом прокси."""
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "unknown")

    def _is_allowed(self, ip: str) -> bool:
        """Проверяет, не превышен ли лимит запросов для IP."""
        now = time.monotonic()
        with self.lock:
            timestamps = self.requests[ip]
            # Удаляем устаревшие записи
            self.requests[ip] = [
                t for t in timestamps if now - t < self.window_seconds
            ]
            if len(self.requests[ip]) >= self.max_requests:
                return False
            self.requests[ip].append(now)
            return True
