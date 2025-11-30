# CoinlayerApiTest
Este proyecto es una aplicación en Python que maneja datos de criptomonedas y monedas fiduciarias de https://coinlayer.com/, incluyendo datos históricos y en tiempo real. Está diseñado para ser desplegado fácilmente con Docker y tiene una estructura modular para facilitar su mantenimiento y escalabilidad.

Requirements
- Python 3.10+
- Docker

For local deployment install dependencies:
<pre>pip install -r requirements.txt</pre>

Running with Docker
<pre>docker-compose up --build -d</pre>

Stop the service
<pre>docker-compose down</pre>

Api EndPoints:
| Method | Path                  |Description                                                                 |
| ------ | --------------------- | --------------------------------------------------------------------------- |
| GET    | `/currency/list`       | Obtiene toda la información de criptomonedas y monedas fiat disponibles y la guarda localmente en JSON. |
| GET    | `/currency/crypto`     | Obtiene el listado de todas las criptomonedas almacenadas en `crypto_data.json`. |
| GET    | `/currency/fiat`       | Obtiene el listado de todas las monedas fiat almacenadas en `fiat_data.json`. |
| GET    | `/currency/live-data`  | Obtiene la tasa de cambio actualizada de todas las criptomonedas (con opción a filtrar por moneda objetivo y símbolos). |
| GET    | `/currency/historical` | Obtiene datos históricos de tasas de cambio para una fecha dada, con opciones de filtrado. |
| PUT    | `/update-access-key`   | Actualiza la llave de acceso usada para consultar la API externa y la guarda en configuración. |

 