from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Permitir CORS para todas las rutas

# Configuración
JSON_FILES_DIR = Path('json_files')
XML_FILES_DIR = Path('xml_files')

# Función auxiliar para cargar archivos JSON
def load_json_file(file_path):
    """Carga un archivo JSON y retorna su contenido"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

# Función auxiliar para obtener lista de biblias
def get_available_bibles():
    """Obtiene la lista de biblias disponibles en formato JSON"""
    bibles = []
    if JSON_FILES_DIR.exists():
        for file in JSON_FILES_DIR.glob('*.json'):
            bible_name = file.stem
            bibles.append({
                'name': bible_name,
                'filename': file.name,
                'language': 'Spanish' if bible_name.startswith('Spanish') else 'English'
            })
    return bibles

# Función auxiliar para obtener comentarios disponibles
def get_available_commentaries():
    """Obtiene la lista de comentarios disponibles"""
    commentaries = []
    commentaries_dir = JSON_FILES_DIR / 'commentaries'
    if commentaries_dir.exists():
        for commentary_dir in commentaries_dir.iterdir():
            if commentary_dir.is_dir():
                books = []
                for book_file in commentary_dir.glob('*.json'):
                    books.append(book_file.stem)
                commentaries.append({
                    'name': commentary_dir.name,
                    'books': books
                })
    return commentaries

@app.route('/', methods=['GET'])
def home():
    """Endpoint principal con información de la API"""
    return jsonify({
        'message': 'API de Biblias - Bienvenido',
        'version': '1.0.0',
        'endpoints': {
            '/bibles': 'Lista de biblias disponibles',
            '/bible/<name>': 'Contenido completo de una biblia',
            '/bible/<name>/<book>': 'Contenido de un libro específico',
            '/bible/<name>/<book>/<chapter>': 'Contenido de un capítulo específico',
            '/commentaries': 'Lista de comentarios disponibles',
            '/commentary/<name>/<book>': 'Comentario de un libro específico'
        }
    })

@app.route('/bibles', methods=['GET'])
def get_bibles():
    """Obtiene la lista de todas las biblias disponibles"""
    bibles = get_available_bibles()
    return jsonify({
        'count': len(bibles),
        'bibles': bibles
    })

@app.route('/bible/<bible_name>', methods=['GET'])
def get_bible(bible_name):
    """Obtiene el contenido completo de una biblia específica"""
    file_path = JSON_FILES_DIR / f'{bible_name}.json'
    bible_data = load_json_file(file_path)
    
    if bible_data is None:
        return jsonify({'error': 'Biblia no encontrada'}), 404
    
    return jsonify(bible_data)

@app.route('/bible/<bible_name>/<book>', methods=['GET'])
def get_bible_book(bible_name, book):
    """Obtiene el contenido de un libro específico de una biblia"""
    file_path = JSON_FILES_DIR / f'{bible_name}.json'
    bible_data = load_json_file(file_path)
    
    if bible_data is None:
        return jsonify({'error': 'Biblia no encontrada'}), 404
    
    # Buscar el libro en la biblia
    book_upper = book.upper()
    for book_data in bible_data.get('books', []):
        if book_data.get('abbrev', '').upper() == book_upper or book_data.get('name', '').upper() == book_upper:
            return jsonify(book_data)
    
    return jsonify({'error': 'Libro no encontrado'}), 404

@app.route('/bible/<bible_name>/<book>/<int:chapter>', methods=['GET'])
def get_bible_chapter(bible_name, book, chapter):
    """Obtiene el contenido de un capítulo específico"""
    file_path = JSON_FILES_DIR / f'{bible_name}.json'
    bible_data = load_json_file(file_path)
    
    if bible_data is None:
        return jsonify({'error': 'Biblia no encontrada'}), 404
    
    # Buscar el libro y capítulo
    book_upper = book.upper()
    for book_data in bible_data.get('books', []):
        if book_data.get('abbrev', '').upper() == book_upper or book_data.get('name', '').upper() == book_upper:
            chapters = book_data.get('chapters', [])
            if 1 <= chapter <= len(chapters):
                return jsonify({
                    'book': book_data.get('name'),
                    'chapter': chapter,
                    'verses': chapters[chapter - 1]
                })
            else:
                return jsonify({'error': 'Capítulo no encontrado'}), 404
    
    return jsonify({'error': 'Libro no encontrado'}), 404

@app.route('/commentaries', methods=['GET'])
def get_commentaries():
    """Obtiene la lista de comentarios disponibles"""
    commentaries = get_available_commentaries()
    return jsonify({
        'count': len(commentaries),
        'commentaries': commentaries
    })

@app.route('/commentary/<commentary_name>/<book>', methods=['GET'])
def get_commentary(commentary_name, book):
    """Obtiene el comentario de un libro específico"""
    file_path = JSON_FILES_DIR / 'commentaries' / commentary_name / f'{book.upper()}.json'
    commentary_data = load_json_file(file_path)
    
    if commentary_data is None:
        return jsonify({'error': 'Comentario no encontrado'}), 404
    
    return jsonify(commentary_data)

@app.route('/search', methods=['GET'])
def search_verses():
    """Busca versículos que contengan un texto específico"""
    query = request.args.get('q', '').strip()
    bible_name = request.args.get('bible', '')
    
    if not query:
        return jsonify({'error': 'Parámetro de búsqueda requerido'}), 400
    
    if not bible_name:
        return jsonify({'error': 'Nombre de biblia requerido'}), 400
    
    file_path = JSON_FILES_DIR / f'{bible_name}.json'
    bible_data = load_json_file(file_path)
    
    if bible_data is None:
        return jsonify({'error': 'Biblia no encontrada'}), 404
    
    results = []
    query_lower = query.lower()
    
    for book in bible_data.get('books', []):
        book_name = book.get('name', '')
        for chapter_idx, chapter in enumerate(book.get('chapters', []), 1):
            for verse_idx, verse in enumerate(chapter, 1):
                if query_lower in verse.lower():
                    results.append({
                        'book': book_name,
                        'chapter': chapter_idx,
                        'verse': verse_idx,
                        'text': verse
                    })
    
    return jsonify({
        'query': query,
        'bible': bible_name,
        'count': len(results),
        'results': results[:100]  # Limitar a 100 resultados
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)