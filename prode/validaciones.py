from datetime import datetime

def es_texto_no_vacio(texto):
    return isinstance(texto, str) and texto.strip() != ""

def es_email_basico(email):
    return isinstance(email, str) and "@" in email and "." in email and email.strip() != ""

def tiene_formato_string(cadena):
    """ Valido que sea string y que no sea string vacio"""
    return isinstance(cadena, str) and cadena.strip() != "" and cadena.isalpha()

def es_entero(goles):
    try:
        int(goles)
        return True
    except ValueError:
        return False

def es_fecha_correcta(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def es_positivo(numero):
    return numero>=0

@usuarios_db.route("/<id>", methods=["PUT"])
def reemplazar_usuario(id):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        if not id.isdigit():
            cursor.close()
            conn.close()
            return respuesta_error(400, "Bad Request", "No es id")

        id = int(id)
        data = request.json

        if not data:
            cursor.close()
            conn.close()
            return respuesta_error(400, "Bad Request", "Body vacío")

        nombre = data.get("nombre")
        email = data.get("email")

        if not es_texto_no_vacio(nombre) or not es_texto_no_vacio(email):
            cursor.close()
            conn.close()
            return respuesta_error(400, "Bad Request", "Faltan campos obligatorios")

        if not es_email_basico(email):
            cursor.close()
            conn.close()
            return respuesta_error(400, "Bad Request", "Email inválido")

        nombre = nombre.strip()
        email = email.strip().lower()

        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE email = %s AND id_usuario <> %s",
            (email, id)
        )
        conflicto = cursor.fetchone()

        if conflicto:
            cursor.close()
            conn.close()
            return respuesta_error(409, "Conflict", "Ya existe otro usuario con ese email")

        cursor.execute(
            "SELECT id_usuario FROM usuarios WHERE id_usuario = %s",
            (id,)
        )
        existe = cursor.fetchone()

        if existe:
            cursor.execute(
                "UPDATE usuarios SET nombre = %s, email = %s WHERE id_usuario = %s",
                (nombre, email, id)
            )
        else:
            cursor.execute(
                "INSERT INTO usuarios (id_usuario, nombre, email) VALUES (%s, %s, %s)",
                (id, nombre, email)
            )

        conn.commit()
        cursor.close()
        conn.close()

        return "", 204

    except Exception as e:
        print(e)
        return respuesta_error(500, "Internal Server Error", "error server")


