from fastapi import FastAPI, HTTPException, Query
from app.models import AccessKey, CryptoModel, FiatModel, CurrencyModel, CurrencyLiveDataModel, RateModel, CurrencyHistoricalDataModel
from pathlib import Path as FilePath
import httpx
import json
from typing import List, Optional

app = FastAPI(
    title="Crypto Coinlayer API",
    description="""
    API para consultar información sobre las tasas de cambio de cryptomonedas y fiat
    """,
    version="1.1.0",
)

CONFIG_PATH = FilePath(__file__).parent / "app_settings.json"
try:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        settings = json.load(f)
except FileNotFoundError:
    raise RuntimeError("El archivo app_settings.json no existe. Crea uno antes de iniciar la app.")

API_URL = settings.get("API_URL")
ACCESS_KEY = settings.get("ACCESS_KEY")
CRYPTO_JSON_FILE = FilePath(__file__).parent / "crypto_data.json"
FIAT_JSON_FILE = FilePath(__file__).parent / "fiat_data.json"
LIVE_DATA_JSON_FILE = FilePath(__file__).parent / "live_data.json"
HISTORICAL_DATA_JSON_FILE = FilePath(__file__).parent / "historical_data.json"

#Obtiene toda la informacion de las cryptomonedas y monedas fiat disponibles
@app.get(
        "/currency/list", 
        response_model=CurrencyModel,
        summary="Obtiene toda la informacion de las cryptomonedas y monedas fiat disponibles"
)
async def get_currency_data():
    params  = { "access_key": f"{ACCESS_KEY}" }

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/list", params =params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error al consultar el API externo")
    
    data = response.json()

    # --- Mapeo de cryptos ---
    cryptos = []
    for crypto_data in data["crypto"].values():
        if crypto_data.get("max_supply") == "N/A":
            crypto_data["max_supply"] = None
        cryptos.append(CryptoModel(**crypto_data))
    
    # --- Mapeo de fiats ---
    fiats = [FiatModel(symbol=symbol, name=name) for symbol, name in data["fiat"].items()]

    currencyModel = CurrencyModel(cryptos=cryptos, fiats=fiats)

    # --- Guardar crypto ---
    with open(CRYPTO_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump([crypto.model_dump() for crypto in currencyModel.cryptos], f, ensure_ascii=False, indent=4)

    #--- Guardar fiat ---
    with open(FIAT_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump([fiat.model_dump() for fiat in currencyModel.fiats], f, ensure_ascii=False, indent=4)

    return currencyModel

#Obtiene el listado de todas las criptomonedas
@app.get(
    "/currency/crypto",
    response_model=List[CryptoModel],
    summary="Obtener todas las criptomonedas almacenados en el JSON"
)
async def get_saved_crypto():
    if not CRYPTO_JSON_FILE.exists():
        raise HTTPException(status_code=404, detail="El archivo crypto_data.json aún no existe.")

    try:
        with open(CRYPTO_JSON_FILE, "r", encoding="utf-8") as f:
            crypto_data = json.load(f)

        if not crypto_data:
            raise HTTPException(status_code=404, detail="No hay criptomonedas almacenadas aún.")

        return crypto_data

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error al leer el archivo crypto_data.json.")
    
#Obtiene el listado de todas las monedas fiat
@app.get(
    "/currency/fiat",
    response_model=List[FiatModel],
    summary="Obtener todas las monedas fiat almacenadas en el JSON"
)
async def get_saved_fiat():
    if not FIAT_JSON_FILE.exists():
        raise HTTPException(status_code=404, detail="El archivo fiat_data.json aún no existe.")

    try:
        with open(FIAT_JSON_FILE, "r", encoding="utf-8") as f:
            fiat_data = json.load(f)

        if not fiat_data:
            raise HTTPException(status_code=404, detail="No hay monedas fiat almacenadas aún.")

        return fiat_data

    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Error al leer el archivo fiat_data.json.")

#Obtiene la tasa cambio actual de todas las cryptomonedas
@app.get(
        "/currency/live-data", 
        response_model=CurrencyLiveDataModel,
        summary="Obtiene la tasa de cambio actualizada de todas las criptomonedas"
)
async def get_currency_live_data(
    target: str = Query("USD", description="Moneda objetivo"),
    symbols: Optional[List[str]] = Query(None, description="Lista de símbolos de criptomonedas separados por coma"),
    expand: bool = Query(False, description="Si se deben devolver detalles extendidos")
):
    params  = { 
        "access_key": f"{ACCESS_KEY}",
        "target": target,
        "expand": 1 if expand else 0
    }
    if symbols:
        params["symbols"] = ",".join(symbols)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/live", params =params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error al consultar el API externo")
    
    data = response.json()

    rates_list = []
    for symbol, value in data["rates"].items():
        if isinstance(value, dict):
            rates_list.append(RateModel(symbol=symbol, **value))
        else:
            rates_list.append(RateModel(symbol=symbol, rate=float(value)))

    currencyLiveDataModel = CurrencyLiveDataModel(
        terms=data.get("terms", ""),
        privacy=data.get("privacy", ""),
        timestamp=data.get("timestamp", 0),
        target=data.get("target", target),
        rates=rates_list
    )

    live_data_list = []
    if LIVE_DATA_JSON_FILE.exists():
        with open(LIVE_DATA_JSON_FILE, "r", encoding="utf-8") as f:
            live_data_list = json.load(f)
    
    live_data_list.append(currencyLiveDataModel.model_dump())
    
    with open(LIVE_DATA_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(live_data_list, f, ensure_ascii=False, indent=4)

    return currencyLiveDataModel

#Obtiene los datos historicos a partir de la fecha definida
@app.get(
        "/currency/historical", 
        response_model=CurrencyHistoricalDataModel,
        summary="Obtiene los datos historicos a partir de la fecha definida"
)
async def get_currency_historical_data(
    date: str = Query(..., description="Fecha de los datos históricos en formato YYYY-MM-DD"),
    target: str = Query("USD", description="Moneda objetivo"),
    symbols: Optional[List[str]] = Query(None, description="Lista de símbolos de criptomonedas separados por coma"),
    expand: bool = Query(False, description="Si se deben devolver detalles extendidos")
):
    params  = { 
        "access_key": f"{ACCESS_KEY}",
        "date": date,
        "target": target,
        "expand": 1 if expand else 0
    }
    if symbols:
        params["symbols"] = ",".join(symbols)

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/live", params =params)
    
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error al consultar el API externo")
    
    data = response.json()

    rates_list = []
    for symbol, value in data["rates"].items():
        if isinstance(value, dict):
            rates_list.append(RateModel(symbol=symbol, **value))
        else:
            rates_list.append(RateModel(symbol=symbol, rate=float(value)))

    currencyHistoricalDataModel = CurrencyHistoricalDataModel(
        terms=data.get("terms", ""),
        privacy=data.get("privacy", ""),
        timestamp=data.get("timestamp", 0),
        target=data.get("target", target),
        historical=data.get("historical", True),
        date=data.get("date", date),
        rates=rates_list
    )

    historical_data_list = []
    if HISTORICAL_DATA_JSON_FILE.exists():
        with open(HISTORICAL_DATA_JSON_FILE, "r", encoding="utf-8") as f:
            historical_data_list = json.load(f)
    
    historical_data_list.append(currencyHistoricalDataModel.model_dump())
    
    with open(HISTORICAL_DATA_JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(historical_data_list, f, ensure_ascii=False, indent=4)

    return currencyHistoricalDataModel

#Actualiza access-key
@app.put("/update-access-key")
async def update_access_key(access_key: AccessKey):
    global ACCESS_KEY

    new_access_key = access_key.new_access_key.strip()
    if not new_access_key:
        raise HTTPException(status_code=400, detail="La nueva llave de acceso no puede estar vacía.")
    
    ACCESS_KEY = new_access_key
    settings["ACCESS_KEY"] = new_access_key

    # Guardar cambio en app_settings.json
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar el archivo de configuración: {str(e)}")
