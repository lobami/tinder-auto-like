# Tinder Auto Like Bot

Bot que abre Tinder en el navegador y después de un delay configurable empieza a dar like automáticamente usando la tecla de flecha derecha.

## Requisitos

- Python 3.8+
- Google Chrome o Brave
- Node.js (para playwright)

## Instalación

```bash
pip install -r requirements.txt
playwright install chromium
```

## Configuración

Copia `.env.example` a `.env` y completa tus credenciales:

```bash
cp .env.example .env
```

## Variables de entorno

| Variable     | Descripción                              | Default |
|-------------|------------------------------------------|---------|
| `EMAIL`     | Email de Facebook para login            | -       |
| `PASSWORD`  | Contraseña de Facebook                  | -       |
| `BROWSER`   | `chrome` o `brave`                      | `chrome`|
| `DELAY`     | Segundos de espera antes de empezar     | `60`    |
| `LIKE_DELAY`| Segundos entre cada like                | `0.5`   |

## Uso

```bash
python main.py
```

Presiona `Ctrl+C` para detener.

## Disclaimer

Usar responsablemente y en accordance con los términos de servicio de Tinder.
