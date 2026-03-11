# ⚡ SuperTrend Bot — Bybit

Bot de trading automático con SuperTrend para Bybit. Dashboard web incluido.

## Archivos

| Archivo | Para qué |
|---------|----------|
| `config.py` | **Editar esto** — API keys y parámetros |
| `autobot.py` | Bot automático (SuperTrend, loop continuo) |
| `bot.py` | Servidor Flask (webhook + dashboard) |
| `dashboard.html` | Panel visual (abrir en navegador) |
| `INICIAR_BOT.bat` | Arrancar servidor Flask |
| `INICIAR_AUTOBOT.bat` | Arrancar bot automático |
| `NGROK.bat` | Exponer bot a internet |
| `instalar.bat` | Instalar dependencias |

## Configuración rápida

1. Editá `config.py` con tus API keys de Bybit
2. Ejecutá `instalar.bat`
3. Ejecutá `INICIAR_AUTOBOT.bat` para el bot automático
4. Ejecutá `INICIAR_BOT.bat` + abrí `dashboard.html` para el panel

## Dashboard desde el celular

1. Subir `dashboard.html` a GitHub Pages
2. Ejecutar `NGROK.bat` para obtener URL pública
3. Pegar URL de ngrok en el panel "URL del Bot"

## GitHub Actions (bot en la nube, gratis)

Agregar en GitHub → Settings → Secrets:
- `BYBIT_API_KEY`
- `BYBIT_API_SECRET`
- `TELEGRAM_TOKEN` (opcional)
- `TELEGRAM_CHAT_ID` (opcional)

## ⚠️ Seguridad

- Nunca subas `config.py` con tus API keys al repo público
- Usar TESTNET primero antes de operar con dinero real
