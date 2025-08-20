#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Conversor de Biblias XML a JSON
Este script convierte archivos XML de biblias al formato JSON manteniendo la estructura jerárquica.
"""

import xml.etree.ElementTree as ET
import json
import os
from pathlib import Path

# Mapeo de números de libros a nombres para mejor legibilidad
BOOK_NAMES = {
    # Antiguo Testamento
    1: "Genesis", 2: "Exodus", 3: "Leviticus", 4: "Numbers", 5: "Deuteronomy",
    6: "Joshua", 7: "Judges", 8: "Ruth", 9: "1 Samuel", 10: "2 Samuel",
    11: "1 Kings", 12: "2 Kings", 13: "1 Chronicles", 14: "2 Chronicles", 15: "Ezra",
    16: "Nehemiah", 17: "Esther", 18: "Job", 19: "Psalms", 20: "Proverbs",
    21: "Ecclesiastes", 22: "Song of Songs", 23: "Isaiah", 24: "Jeremiah", 25: "Lamentations",
    26: "Ezekiel", 27: "Daniel", 28: "Hosea", 29: "Joel", 30: "Amos",
    31: "Obadiah", 32: "Jonah", 33: "Micah", 34: "Nahum", 35: "Habakkuk",
    36: "Zephaniah", 37: "Haggai", 38: "Zechariah", 39: "Malachi",
    # Nuevo Testamento
    40: "Matthew", 41: "Mark", 42: "Luke", 43: "John", 44: "Acts",
    45: "Romans", 46: "1 Corinthians", 47: "2 Corinthians", 48: "Galatians", 49: "Ephesians",
    50: "Philippians", 51: "Colossians", 52: "1 Thessalonians", 53: "2 Thessalonians", 54: "1 Timothy",
    55: "2 Timothy", 56: "Titus", 57: "Philemon", 58: "Hebrews", 59: "James",
    60: "1 Peter", 61: "2 Peter", 62: "1 John", 63: "2 John", 64: "3 John",
    65: "Jude", 66: "Revelation"
}

def parse_verse(verse_element):
    """Convierte un elemento verse XML a diccionario."""
    return {
        "number": int(verse_element.get("number")),
        "text": verse_element.text or ""
    }

def parse_chapter(chapter_element):
    """Convierte un elemento chapter XML a diccionario."""
    verses = []
    for verse in chapter_element.findall("verse"):
        verses.append(parse_verse(verse))
    
    return {
        "number": int(chapter_element.get("number")),
        "verses": verses
    }

def parse_book(book_element):
    """Convierte un elemento book XML a diccionario."""
    book_number = int(book_element.get("number"))
    chapters = []
    
    for chapter in book_element.findall("chapter"):
        chapters.append(parse_chapter(chapter))
    
    return {
        "number": book_number,
        "name": BOOK_NAMES.get(book_number, f"Book {book_number}"),
        "chapters": chapters
    }

def parse_testament(testament_element):
    """Convierte un elemento testament XML a diccionario."""
    books = []
    for book in testament_element.findall("book"):
        books.append(parse_book(book))
    
    return {
        "name": testament_element.get("name"),
        "books": books
    }

def convert_xml_to_json(xml_file_path):
    """Convierte un archivo XML de biblia a formato JSON."""
    try:
        # Parsear el archivo XML
        tree = ET.parse(xml_file_path)
        root = tree.getroot()
        
        # Extraer información de la biblia
        bible_data = {
            "name": root.get("name"),
            "abbreviation": root.get("abbreviation"),
            "language": root.get("language"),
            "testaments": []
        }
        
        # Procesar cada testamento
        for testament in root.findall("testament"):
            bible_data["testaments"].append(parse_testament(testament))
        
        return bible_data
        
    except ET.ParseError as e:
        print(f"Error al parsear el archivo XML {xml_file_path}: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado al procesar {xml_file_path}: {e}")
        return None

def convert_all_xml_files(input_directory, output_directory=None):
    """Convierte todos los archivos XML en el directorio especificado a JSON."""
    input_path = Path(input_directory)
    
    if output_directory is None:
        output_directory = input_path.parent / "json_files"
    
    output_path = Path(output_directory)
    output_path.mkdir(exist_ok=True)
    
    xml_files = list(input_path.glob("*.xml"))
    
    if not xml_files:
        print(f"No se encontraron archivos XML en {input_directory}")
        return
    
    print(f"Encontrados {len(xml_files)} archivos XML para convertir...")
    
    for xml_file in xml_files:
        print(f"Procesando: {xml_file.name}")
        
        # Convertir XML a JSON
        json_data = convert_xml_to_json(xml_file)
        
        if json_data is not None:
            # Crear nombre del archivo JSON
            json_filename = xml_file.stem + ".json"
            json_file_path = output_path / json_filename
            
            # Guardar archivo JSON
            try:
                with open(json_file_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                print(f"✓ Convertido exitosamente: {json_filename}")
            except Exception as e:
                print(f"✗ Error al guardar {json_filename}: {e}")
        else:
            print(f"✗ Error al convertir {xml_file.name}")
    
    print(f"\nConversión completada. Archivos JSON guardados en: {output_path}")

def main():
    """Función principal del script."""
    # Directorio de archivos XML
    xml_directory = r"c:\Users\VIDA-SANA\Desktop\Pablo Bahamonde\Apps\Biblias\xml_files"
    
    # Verificar que el directorio existe
    if not os.path.exists(xml_directory):
        print(f"Error: El directorio {xml_directory} no existe.")
        return
    
    print("=== Conversor de Biblias XML a JSON ===")
    print(f"Directorio de entrada: {xml_directory}")
    
    # Convertir todos los archivos
    convert_all_xml_files(xml_directory)

if __name__ == "__main__":
    main()