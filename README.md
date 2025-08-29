# API de Biblias

Una API REST para acceder a biblias en español e inglés, junto con comentarios bíblicos.

## Características

- Acceso a múltiples versiones de la Biblia en español e inglés
- Comentarios bíblicos de reconocidos teólogos
- Búsqueda de versículos por texto
- Endpoints RESTful bien estructurados
- Soporte para CORS

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/PabloB1988/Biblias.git
cd Biblias
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la API:
```bash
python app.py
```

La API estará disponible en `http://localhost:5000`

## Endpoints Disponibles

### Información General

#### `GET /`
Retorna información general sobre la API y sus endpoints disponibles.

**Respuesta:**
```json
{
  "message": "API de Biblias - Bienvenido",
  "version": "1.0.0",
  "endpoints": {
    "/bibles": "Lista de biblias disponibles",
    "/bible/<name>": "Contenido completo de una biblia",
    "/bible/<name>/<book>": "Contenido de un libro específico",
    "/bible/<name>/<book>/<chapter>": "Contenido de un capítulo específico",
    "/commentaries": "Lista de comentarios disponibles",
    "/commentary/<name>/<book>": "Comentario de un libro específico"
  }
}
```

### Biblias

#### `GET /bibles`
Obtiene la lista de todas las biblias disponibles.

**Respuesta:**
```json
{
  "count": 7,
  "bibles": [
    {
      "name": "SpanishRVR1960Bible",
      "filename": "SpanishRVR1960Bible.json",
      "language": "Spanish"
    },
    {
      "name": "EnglishAmplifiedBible",
      "filename": "EnglishAmplifiedBible.json",
      "language": "English"
    }
  ]
}
```

#### `GET /bible/<bible_name>`
Obtiene el contenido completo de una biblia específica.

**Parámetros:**
- `bible_name`: Nombre de la biblia (ej: `SpanishRVR1960Bible`)

**Ejemplo:**
```
GET /bible/SpanishRVR1960Bible
```

#### `GET /bible/<bible_name>/<book>`
Obtiene el contenido de un libro específico de una biblia.

**Parámetros:**
- `bible_name`: Nombre de la biblia
- `book`: Nombre o abreviación del libro (ej: `GEN`, `Genesis`)

**Ejemplo:**
```
GET /bible/SpanishRVR1960Bible/GEN
```

#### `GET /bible/<bible_name>/<book>/<chapter>`
Obtiene el contenido de un capítulo específico.

**Parámetros:**
- `bible_name`: Nombre de la biblia
- `book`: Nombre o abreviación del libro
- `chapter`: Número del capítulo

**Ejemplo:**
```
GET /bible/SpanishRVR1960Bible/GEN/1
```

**Respuesta:**
```json
{
  "book": "Génesis",
  "chapter": 1,
  "verses": [
    "En el principio creó Dios los cielos y la tierra.",
    "Y la tierra estaba desordenada y vacía..."
  ]
}
```

### Comentarios

#### `GET /commentaries`
Obtiene la lista de comentarios disponibles.

**Respuesta:**
```json
{
  "count": 3,
  "commentaries": [
    {
      "name": "matthew-henry",
      "books": ["GEN", "EXO", "LEV", ...]
    },
    {
      "name": "jamieson-fausset-brown",
      "books": ["GEN", "EXO", "LEV", ...]
    }
  ]
}
```

#### `GET /commentary/<commentary_name>/<book>`
Obtiene el comentario de un libro específico.

**Parámetros:**
- `commentary_name`: Nombre del comentario (ej: `matthew-henry`)
- `book`: Abreviación del libro (ej: `GEN`)

**Ejemplo:**
```
GET /commentary/matthew-henry/GEN
```

### Búsqueda

#### `GET /search`
Busca versículos que contengan un texto específico.

**Parámetros de consulta:**
- `q`: Texto a buscar (requerido)
- `bible`: Nombre de la biblia donde buscar (requerido)

**Ejemplo:**
```
GET /search?q=amor&bible=SpanishRVR1960Bible
```

**Respuesta:**
```json
{
  "query": "amor",
  "bible": "SpanishRVR1960Bible",
  "count": 25,
  "results": [
    {
      "book": "Juan",
      "chapter": 3,
      "verse": 16,
      "text": "Porque de tal manera amó Dios al mundo..."
    }
  ]
}
```

## Biblias Disponibles

### Español
- **SpanishRVR1960Bible**: Reina-Valera 1960
- **SpanishNVIBible**: Nueva Versión Internacional
- **SpanishDHHBible**: Dios Habla Hoy
- **SpanishLBLABible**: La Biblia de las Américas
- **SpanishTLABible**: Traducción en Lenguaje Actual

### Inglés
- **EnglishAmplifiedBible**: Amplified Bible
- **EnglishYLTBible**: Young's Literal Translation

## Comentarios Disponibles

- **matthew-henry**: Comentario de Matthew Henry
- **jamieson-fausset-brown**: Comentario de Jamieson, Fausset y Brown
- **keil-delitzsch**: Comentario de Keil y Delitzsch

## Códigos de Error

- `400`: Solicitud incorrecta (parámetros faltantes)
- `404`: Recurso no encontrado (biblia, libro o comentario)
- `500`: Error interno del servidor

## Ejemplos de Uso

### Python
```python
import requests

# Obtener lista de biblias
response = requests.get('http://localhost:5000/bibles')
bibles = response.json()

# Obtener un capítulo específico
response = requests.get('http://localhost:5000/bible/SpanishRVR1960Bible/GEN/1')
chapter = response.json()

# Buscar versículos
response = requests.get('http://localhost:5000/search?q=amor&bible=SpanishRVR1960Bible')
results = response.json()
```

### JavaScript
```javascript
// Obtener lista de biblias
fetch('http://localhost:5000/bibles')
  .then(response => response.json())
  .then(data => console.log(data));

// Obtener un capítulo específico
fetch('http://localhost:5000/bible/SpanishRVR1960Bible/GEN/1')
  .then(response => response.json())
  .then(data => console.log(data));
```

### cURL
```bash
# Obtener lista de biblias
curl http://localhost:5000/bibles

# Obtener un capítulo específico
curl http://localhost:5000/bible/SpanishRVR1960Bible/GEN/1

# Buscar versículos
curl "http://localhost:5000/search?q=amor&bible=SpanishRVR1960Bible"
```

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Archivos y Directorios

### Directorios principales:
- `json_files/`: Contiene todas las biblias en formato JSON
- `json_files/commentaries/`: Contiene todos los comentarios bíblicos en formato JSON
- `xml_files/`: Contiene las biblias en formato XML original
- `archive/`: Contiene archivos innecesarios o de desarrollo que han sido archivados

### Archivos importantes:
- `app.py`: Aplicación principal de la API
- `requirements.txt`: Dependencias del proyecto

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Pablo - [@PabloB1988](https://github.com/PabloB1988)

Link del Proyecto: [https://github.com/PabloB1988/Biblias](https://github.com/PabloB1988/Biblias)