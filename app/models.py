from pydantic import BaseModel
from typing import List, Optional

# Modelo para Criptomonedas
class CryptoModel(BaseModel):
    symbol: str
    name: str
    name_full: str
    max_supply: Optional[float]
    icon_url: str

# Modelo para monedas fiat
class FiatModel(BaseModel):
    symbol: str
    name: str

# Modelo principal
class CurrencyModel(BaseModel):
    cryptos: List[CryptoModel]
    fiats: List[FiatModel]

# Modelo AccessKey
class AccessKey(BaseModel):
    new_access_key: str  # Access Key

# --- Modelo para cada tasa de criptomoneda ---
class RateModel(BaseModel):
    symbol: str
    rate: float
    high: Optional[float] = 0
    low: Optional[float] = 0
    vol: Optional[float] = 0
    cap: Optional[float] = 0
    sup: Optional[float] = 0
    change: Optional[float] = 0
    change_pct: Optional[float] = 0

# --- Modelo live data ---
class CurrencyLiveDataModel(BaseModel):
    terms: str
    privacy: str
    timestamp: int
    target: str
    rates: List[RateModel]

# --- Modelo historical data
class CurrencyHistoricalDataModel(BaseModel):
    terms: str
    privacy: str
    timestamp: int
    target: str
    historical: bool
    date: str
    rates: List[RateModel]