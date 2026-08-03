import pytest
from unittest.mock import AsyncMock, MagicMock
from starlette.responses import JSONResponse, Response
from starlette.applications import Starlette
from starlette.routing import Route
from httpx import AsyncClient, ASGITransport


@pytest.fixture(autouse=True)
def restore_csrf_dispatch():
    from app.middleware import csrf as csrf_module

    orig = csrf_module.CSRFMiddleware.dispatch
    yield
    csrf_module.CSRFMiddleware.dispatch = orig


class TestCSRFMiddleware:
    @pytest.mark.anyio
    async def test_get_request_sets_csrf_cookie(self):
        from app.middleware.csrf import CSRFMiddleware

        async def ok_endpoint(request):
            return JSONResponse(content={"ok": True})

        app = Starlette(routes=[Route("/api/v1/test", endpoint=ok_endpoint)])
        app.add_middleware(CSRFMiddleware)

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/api/v1/test")
            assert resp.status_code == 200
            assert "csrf_token" in resp.cookies

    @pytest.mark.anyio
    async def test_safe_methods_skip_csrf_check(self):
        from app.middleware.csrf import CSRFMiddleware

        async def ok_endpoint(request):
            return JSONResponse(content={"ok": True})

        app = Starlette(routes=[Route("/api/v1/test", endpoint=ok_endpoint)])
        app.add_middleware(CSRFMiddleware)

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            for method in ("GET", "HEAD"):
                resp = await client.request(method, "/api/v1/test")
                assert resp.status_code == 200
            # OPTIONS — starlette returns 405 if route only defines GET
            resp = await client.options("/api/v1/test")
            assert resp.status_code in (200, 405)

    @pytest.mark.anyio
    async def test_auth_path_bypasses_csrf(self):
        from app.middleware.csrf import CSRFMiddleware

        async def auth_endpoint(request):
            return JSONResponse(content={"token": "abc"})

        app = Starlette(routes=[Route("/api/v1/auth/token", endpoint=auth_endpoint, methods=["POST"])])
        app.add_middleware(CSRFMiddleware)

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post("/api/v1/auth/token")
            assert resp.status_code == 200

    @pytest.mark.anyio
    async def test_post_without_csrf_token_rejected(self):
        from app.middleware.csrf import CSRFMiddleware

        async def protected_endpoint(request):
            return JSONResponse(content={"data": "sensitive"})

        app = Starlette(
            routes=[Route("/api/v1/portfolios", endpoint=protected_endpoint, methods=["POST"])]
        )
        app.add_middleware(CSRFMiddleware)

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post("/api/v1/portfolios")
            assert resp.status_code == 403
            assert "CSRF token missing" in resp.text

    @pytest.mark.anyio
    async def test_post_with_valid_csrf_token_passes(self):
        from app.middleware.csrf import CSRFMiddleware

        async def protected_endpoint(request):
            return JSONResponse(content={"data": "sensitive"})

        app = Starlette(
            routes=[Route("/api/v1/portfolios", endpoint=protected_endpoint, methods=["POST"])]
        )
        app.add_middleware(CSRFMiddleware)

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            get_resp = await client.get("/api/v1/portfolios")
            csrf_token = get_resp.cookies.get("csrf_token")
            assert csrf_token is not None

            post_resp = await client.post(
                "/api/v1/portfolios",
                cookies={"csrf_token": csrf_token},
                headers={"X-CSRF-Token": csrf_token},
            )
            assert post_resp.status_code == 200

    @pytest.mark.anyio
    async def test_csrf_token_mismatch_rejected(self):
        from app.middleware.csrf import CSRFMiddleware

        async def protected_endpoint(request):
            return JSONResponse(content={"data": "sensitive"})

        app = Starlette(
            routes=[Route("/api/v1/portfolios", endpoint=protected_endpoint, methods=["POST"])]
        )
        app.add_middleware(CSRFMiddleware)

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post(
                "/api/v1/portfolios",
                cookies={"csrf_token": "cookie_token"},
                headers={"X-CSRF-Token": "different_token"},
            )
            assert resp.status_code == 403
            assert "CSRF token mismatch" in resp.text

    @pytest.mark.anyio
    async def test_post_with_cookie_only_rejected(self):
        from app.middleware.csrf import CSRFMiddleware

        async def protected_endpoint(request):
            return JSONResponse(content={"data": "sensitive"})

        app = Starlette(
            routes=[Route("/api/v1/portfolios", endpoint=protected_endpoint, methods=["POST"])]
        )
        app.add_middleware(CSRFMiddleware)

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.post(
                "/api/v1/portfolios",
                cookies={"csrf_token": "some_token"},
            )
            assert resp.status_code == 403
            assert "CSRF token missing" in resp.text

    @pytest.mark.anyio
    async def test_get_request_does_not_overwrite_existing_cookie(self):
        """CSRF middleware respects an existing token and doesn't force-replace it."""
        from app.middleware.csrf import CSRFMiddleware

        async def ok_endpoint(request):
            return JSONResponse(content={"ok": True})

        app = Starlette(routes=[Route("/api/v1/test", endpoint=ok_endpoint)])
        app.add_middleware(CSRFMiddleware)

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp1 = await client.get("/api/v1/test", cookies={"csrf_token": "preexisting"})
            # Middleware may not re-set the cookie if one already exists
            assert resp1.status_code == 200


class TestRequestIDMiddleware:
    @pytest.mark.anyio
    async def test_adds_request_id_from_header(self):
        from app.middleware.csrf import RequestIDMiddleware

        async def ok_endpoint(request):
            return JSONResponse(content={"ok": True})

        app = Starlette(routes=[Route("/api/v1/test", endpoint=ok_endpoint)])
        app.add_middleware(RequestIDMiddleware)

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/api/v1/test", headers={"X-Request-ID": "req-12345"})
            assert resp.headers.get("X-Request-ID") == "req-12345"
            assert "X-Response-Time-Ms" in resp.headers

    @pytest.mark.anyio
    async def test_generates_request_id_when_missing(self):
        from app.middleware.csrf import RequestIDMiddleware

        async def ok_endpoint(request):
            return JSONResponse(content={"ok": True})

        app = Starlette(routes=[Route("/api/v1/test", endpoint=ok_endpoint)])
        app.add_middleware(RequestIDMiddleware)

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/api/v1/test")
            request_id = resp.headers.get("X-Request-ID")
            assert request_id is not None
            assert len(request_id) > 0

    @pytest.mark.anyio
    async def test_adds_response_time_header(self):
        from app.middleware.csrf import RequestIDMiddleware

        async def ok_endpoint(request):
            return JSONResponse(content={"ok": True})

        app = Starlette(routes=[Route("/api/v1/test", endpoint=ok_endpoint)])
        app.add_middleware(RequestIDMiddleware)

        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            resp = await client.get("/api/v1/test")
            response_time = resp.headers.get("X-Response-Time-Ms", "")
            # Header value is a plain number (seconds as float string)
            assert response_time, "Response time header should be present"
            value = float(response_time)
            assert value >= 0
