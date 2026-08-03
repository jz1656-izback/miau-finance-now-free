"""
🔒 COMPREHENSIVE INPUT VALIDATORS
All user input must be validated against these schemas
Prevents: SQL injection, XSS, buffer overflow, command injection, etc.
"""

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import re

# 🔒 REGEX PATTERNS FOR VALIDATION
TICKER_PATTERN = re.compile(r'^[A-Z0-9]{1,5}$')
EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
SAFE_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9\s\-_.()]{1,255}$')
NUMERIC_PATTERN = re.compile(r'^[0-9]+(\.[0-9]{1,10})?$')


class TickerValidator(BaseModel):
    """Validate ticker symbols"""
    ticker: str = Field(..., min_length=1, max_length=5)

    @field_validator('ticker')
    def validate_ticker(cls, v):
        if not TICKER_PATTERN.match(v.upper()):
            raise ValueError('Invalid ticker format (A-Z, 0-9 only, max 5 chars)')
        return v.upper()


class PortfolioCreateSchema(BaseModel):
    """Validate portfolio creation input"""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    portfolio_type: str = Field(..., pattern='^(equity|fixed_income|crypto|commodity|mixed)$')
    
    @field_validator('name')
    def validate_name(cls, v):
        if not SAFE_NAME_PATTERN.match(v):
            raise ValueError('Invalid characters in portfolio name')
        return v
    
    @field_validator('description')
    def validate_description(cls, v):
        if v and '<' in v or '>' in v or 'javascript:' in v.lower():
            raise ValueError('XSS attempt detected in description')
        return v


class TradeCreateSchema(BaseModel):
    """Validate trade input"""
    ticker: str = Field(..., min_length=1, max_length=5)
    trade_type: str = Field(..., pattern='^(buy|sell)$')
    quantity: float = Field(..., gt=0, le=1_000_000_000)
    price: float = Field(..., gt=0, le=1_000_000)
    trade_date: Optional[datetime] = None
    
    @field_validator('ticker')
    def validate_ticker(cls, v):
        if not TICKER_PATTERN.match(v.upper()):
            raise ValueError('Invalid ticker')
        return v.upper()
    
    @field_validator('quantity', 'price')
    def validate_numeric(cls, v):
        if not (isinstance(v, (int, float)) and v > 0):
            raise ValueError('Must be positive number')
        return v


class PriceDataSchema(BaseModel):
    """Validate price data"""
    ticker: str = Field(..., min_length=1, max_length=5)
    price: float = Field(..., gt=0)
    change_pct: float = Field(..., ge=-100, le=100)
    volume: Optional[int] = Field(None, ge=0)
    
    @field_validator('ticker')
    def validate_ticker(cls, v):
        if not TICKER_PATTERN.match(v.upper()):
            raise ValueError('Invalid ticker')
        return v.upper()


class SearchQuerySchema(BaseModel):
    """Validate search input"""
    query: str = Field(..., min_length=1, max_length=255)
    limit: int = Field(10, ge=1, le=100)  # Max 100 results
    offset: int = Field(0, ge=0)
    
    @field_validator('query')
    def validate_query(cls, v):
        # Remove dangerous characters
        dangerous_chars = ['<', '>', '"', "'", ';', '--', '/*', '*/']
        for char in dangerous_chars:
            if char in v:
                raise ValueError(f'Invalid character: {char}')
        return v


class OptimizerSchema(BaseModel):
    """Validate portfolio optimization input"""
    tickers: List[str] = Field(..., min_length=2, max_length=100)
    method: str = Field('sharpe', pattern='^(sharpe|min_variance|equal_weight|black_litterman)$')
    risk_free_rate: Optional[float] = Field(0.02, ge=0, le=1)
    
    @field_validator('tickers')
    def validate_tickers(cls, v):
        unique_tickers = set()
        for ticker in v:
            if not TICKER_PATTERN.match(ticker.upper()):
                raise ValueError(f'Invalid ticker: {ticker}')
            if ticker.upper() in unique_tickers:
                raise ValueError(f'Duplicate ticker: {ticker}')
            unique_tickers.add(ticker.upper())
        return [t.upper() for t in v]


class RiskAnalysisSchema(BaseModel):
    """Validate risk analysis input"""
    ticker: str = Field(..., min_length=1, max_length=5)
    confidence_level: Optional[float] = Field(0.95, ge=0.5, le=0.99)
    periods: Optional[int] = Field(252, ge=1, le=3650)  # Max 10 years
    
    @field_validator('ticker')
    def validate_ticker(cls, v):
        if not TICKER_PATTERN.match(v.upper()):
            raise ValueError('Invalid ticker')
        return v.upper()


class PaginationSchema(BaseModel):
    """Validate pagination parameters"""
    limit: int = Field(20, ge=1, le=500)  # Max 500 items per page
    offset: int = Field(0, ge=0, le=1_000_000)
    sort_by: Optional[str] = Field(None, max_length=50)
    sort_order: Optional[str] = Field('asc', pattern='^(asc|desc)$')
    
    @field_validator('sort_by')
    def validate_sort_by(cls, v):
        if v:
            # Only allow alphanumeric and underscore
            if not re.match(r'^[a-zA-Z0-9_]+$', v):
                raise ValueError('Invalid sort field')
        return v


class NewsSearchSchema(BaseModel):
    """Validate news search input"""
    ticker: Optional[str] = Field(None, min_length=1, max_length=5)
    query: Optional[str] = Field(None, min_length=1, max_length=255)
    limit: int = Field(20, ge=1, le=100)
    
    @field_validator('ticker')
    def validate_ticker(cls, v):
        if v and not TICKER_PATTERN.match(v.upper()):
            raise ValueError('Invalid ticker')
        return v.upper() if v else None
    
    @model_validator(mode='before')
    @classmethod
    def validate_at_least_one(cls, data):
        if not data.get('ticker') and not data.get('query'):
            raise ValueError('Either ticker or query must be provided')
        return data


# Standalone validator function for safe strings (used by ontology & finance schemas)
def safe_string_validator(v: str) -> str:
    """Validate and sanitize a string value"""
    if not isinstance(v, str):
        raise ValueError('Must be a string')
    if len(v) > 1000:
        raise ValueError('String too long (max 1000 chars)')
    # Strip HTML tags and dangerous content
    import re as _re
    cleaned = _re.sub(r'<[^>]*>', '', v)
    cleaned = _re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', cleaned)
    if 'javascript:' in cleaned.lower():
        raise ValueError('XSS attempt detected')
    return cleaned


# Utility function for list input validation
def validate_tickers_list(tickers: List[str], max_count: int = 50) -> List[str]:
    """Validate list of tickers"""
    if not isinstance(tickers, list):
        raise ValueError('Tickers must be a list')
    
    if len(tickers) > max_count:
        raise ValueError(f'Too many tickers (max {max_count})')
    
    validated = []
    seen = set()
    
    for ticker in tickers:
        if not isinstance(ticker, str):
            raise ValueError('All tickers must be strings')
        
        if not TICKER_PATTERN.match(ticker.upper()):
            raise ValueError(f'Invalid ticker: {ticker}')
        
        upper_ticker = ticker.upper()
        if upper_ticker in seen:
            raise ValueError(f'Duplicate ticker: {ticker}')
        
        seen.add(upper_ticker)
        validated.append(upper_ticker)
    
    return validated


# Sanitize output data
def sanitize_output(data: Any) -> Any:
    """Remove potentially dangerous characters from output"""
    if isinstance(data, str):
        # Remove null bytes and control characters
        return ''.join(char for char in data if ord(char) >= 32 or char == '\n')
    elif isinstance(data, dict):
        return {k: sanitize_output(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_output(item) for item in data]
    return data
