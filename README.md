# Proyecto: tablero de posts con votos

Proyecto de clase (sin terminar) que combina una página web con un bot de Discord para publicar ideas y votarlas. La idea original era una interfaz web y un bot de Discord con consejos para cuidar el medio ambiente (ver `Proyecto lol.txt`).

## Qué hace

**Página web (`index.html`)**
- Formulario para crear posts con título y descripción.
- Botones para votar a favor o en contra, editar y eliminar cada post.
- Los posts se guardan en el navegador con `localStorage`.

**Servidor y bot (`main.py`)**
- Servidor **Flask** que sirve la página y expone una pequeña API:
  - `GET /posts` lista los posts.
  - `POST /vote` suma o resta un voto (`{"index": 0, "type": "up"}`).
- Bot de **Discord** (prefijo `!`) que corre en paralelo:
  - `!addpost <título> <descripción>` publica un post y agrega las reacciones ⬆️ ⬇️.
  - `!loadposts` vuelve a cargar los posts desde los últimos 100 mensajes del canal.
  - Las reacciones ⬆️ / ⬇️ suman o restan votos.

## Requisitos

- Python 3.8 o superior
- `flask` y `discord.py`

```bash
pip install flask discord.py
```

## Cómo ejecutarlo

1. Crea un bot en el [Portal de desarrolladores de Discord](https://discord.com/developers/applications) y activa los intents **Message Content** y de reacciones.
2. Reemplaza `'token aqui :vvv'` en `main.py` por el token del bot (no lo subas a GitHub).
3. Ejecuta `python main.py`. La web queda en <http://localhost:5000>.

## Estado

Proyecto incompleto: la página web guarda sus posts en el navegador y todavía no usa la API de Flask, así que lo que se publica en la web y en Discord no está sincronizado.
