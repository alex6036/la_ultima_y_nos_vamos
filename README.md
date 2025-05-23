https://github.com/alex6036/la_ultima_y_nos_vamos.git
no puede crear un chatbot me daba muchos error y me decia que me hacia falta espacio
# la_ultima_y_nos_vamos

Plataforma de votaciones en vivo para streamers, con soporte para encuestas simples, múltiples y ponderadas, autenticación de usuarios y emisión de tokens NFT como comprobantes de voto. Incluye interfaz gráfica con Gradio y CLI.

## Características

- Registro e inicio de sesión de usuarios
- Creación y gestión de encuestas en vivo
- Votación con distintos tipos de encuestas (simple, múltiple, ponderada)
- Resultados parciales y cierre de encuestas
- Emisión y transferencia de tokens NFT por voto
- Chatbot integrado para interacción básica
- Interfaz gráfica (Gradio) y de línea de comandos (CLI)
- Persistencia en archivos JSON

## Instalación

1. Clona el repositorio:
   ```sh
   git clone https://github.com/alex6036/la_ultima_y_nos_vamos.git
   cd la_ultima_y_nos_vamos
   ```

2. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```

## Uso

### Interfaz Gráfica (Gradio)

Ejecuta:
```sh
python app.py
```
Abre tu navegador en [http://localhost:7860](http://localhost:7860).

### Interfaz de Línea de Comandos (CLI)

Puedes adaptar el archivo `app.py` para usar el controlador CLI en vez de Gradio.

## Estructura del Proyecto

- `app.py`: Punto de entrada principal.
- `config.py`: Configuración de rutas y tipo de almacenamiento.
- `data/`: Archivos JSON de persistencia (usuarios, encuestas, votos, NFTs).
- `src/`
  - `controllers/`: Controladores para CLI y UI.
  - `models/`: Modelos de dominio (Usuario, Encuesta, Voto, TokenNFT).
  - `repositories/`: Acceso a datos y persistencia.
  - `services/`: Lógica de negocio (usuarios, encuestas, NFTs, chatbot).
  - `patterns/`: Patrones de diseño (Factory, Strategy, Observer).
  - `ui/`: Interfaz gráfica con Gradio.
- `tests/`: Pruebas unitarias.

## Créditos

Desarrollado por [alex6036](https://github.com/alex6036).

---
Repositorio: https://github.com/alex6036/la_ultima_y_nos_vamos.git
