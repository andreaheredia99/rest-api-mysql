def borrar_tildes(text: str):
    text = text.lower()
    text_replace = text.replace("á", "a")
    text_replace = text_replace.replace("é", "e")
    text_replace = text_replace.replace("í", "i")
    text_replace = text_replace.replace("ó", "o")
    text_replace = text_replace.replace("ú", "u")
    return text_replace
