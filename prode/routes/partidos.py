from flask import jsonify, Blueprint, request
from db import get_connection
from validaciones import es_fecha_correcta,tiene_formato_string,es_entero,es_positivo

partidos_db= Blueprint("partidos",__name__)







@partidos_db.route("/<id_fixture>/prediccion", methods=['POST'])
def predecir_partido(id_fixture):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    data = request.get_json(silent=True)
#Si no se manda nada
    if data is None:
       return jsonify({'code':'400','message':'Falta json (none)','Descripcion':'Bad request'}), 400
    if data=={}:
        return jsonify({'Error':'Json vacio'}),400
    if (
    data.get("id_usuario") is None or
    data.get("goles_local") is None or
    data.get("goles_visitante") is None
    ):
     return jsonify({'code':'400','message':'Todos los datos son obligatorios','Descripcion':'Bad request'}), 400
    
    id_usuario= data.get("id_usuario")
    goles_local= data.get("goles_local")
    goles_visitante= data.get("goles_visitante")


#Si no esxiste el partido y si goles_local y goles_visitante tienen resultados(valores)

    cursor.execute("""SELECT * FROM fixture WHERE id_fixture=%s"""
                   ,(id_fixture,))
    partido= cursor.fetchone()
    if not partido:
        return jsonify({'code':'404','message':'Partido inexistente o no encontrado','Descripcion':'Not Found'}), 404
    if partido["goles_local"] is not None and partido["goles_visitante"] is not None:
        return jsonify({'code':'400','message':'El partido ya se jugó','Descripcion':'Bad request'}), 400
    
#Si un usuario predice el mismo partido mas de una vez

    cursor.execute(""" SELECT * FROM Predicciones WHERE id_fixture= %s AND id_usuario= %s"""
                   ,(id_fixture,id_usuario))
    repetido= cursor.fetchone()
    if repetido:
        return jsonify({'code':'409','message':'El usuario ya hizo prediccion de este partido','Descripcion':'Conflict'}), 409
    
    
#Si se manda la solicitud correctamente

    cursor.execute("""
                   INSERT INTO Predicciones (id_fixture, id_usuario, goles_local, goles_visitante)
                   VALUES (%s, %s, %s, %s)
                   """, (id_fixture, id_usuario, goles_local, goles_visitante))
    
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return ('Prediccion agregada correctamente'), 201


def respuesta_error(code, message, description, level = 'error'):
    return jsonify({
        "errors" : [
            {
                "code" : str(code),
                "message" : message,
                "level" : level,
                "description" : description
            }
        ]
    }), code
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


