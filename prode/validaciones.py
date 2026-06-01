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

@partidos_db.route("/",methods=["GET"])
def obtener_partidos():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT id_fixture,local,visitante,fecha,fase FROM fixture"
        condiciones=[]
        parametros_filtros=[]

        local=request.args.get('local')
        visitante=request.args.get('visitante')
        fecha=request.args.get('fecha')
        fase=request.args.get('fase')

        if local:
            if not tiene_formato_string(local):
                return jsonify({"error": "Equipo local mal ingresado"}), 400
            condiciones.append("local = %s")
            parametros_filtros.append(local)

        if visitante:
            if not tiene_formato_string(visitante):
                return jsonify({"error": "Equipo visitante mal ingresado"}), 400
            condiciones.append("visitante = %s")
            parametros_filtros.append(visitante)

        if fecha:
            if not es_fecha_correcta(fecha):
                return jsonify({"error": "Fecha inválida"}), 400
            condiciones.append("fecha = %s")
            parametros_filtros.append(fecha)

        if fase:
            condiciones.append("fase = %s")
            parametros_filtros.append(fase)

        # si hay condiciones, las agrego a la query hecha
        if condiciones:
            query += " WHERE " + " AND ".join(condiciones)

        #PAGINACION
        contador = "SELECT COUNT(*) as total FROM fixture"
        if condiciones:
            contador += " WHERE " + " AND ".join(condiciones)

        cursor.execute(contador, parametros_filtros)
        total = cursor.fetchone()["total"]

        limit = request.args.get('_limit',default=10,type=int)
        offset = request.args.get('_offset',default=0,type=int)

        parametros_query=parametros_filtros.copy()

        if limit is not None:
            if not es_entero(limit) or not es_positivo(int(limit)):
                return jsonify({"error": "Valor inválido"}), 400
            query += " LIMIT %s"
            parametros_query.append(limit)

        if offset is not None:
            if not es_entero(offset) or not es_positivo(int(offset)):
                return jsonify({"error": "Valor inválido"}), 400
            query += " OFFSET %s"
            parametros_query.append(offset)

        cursor.execute(query, parametros_query)
        # ejemplo de como funciona el execute
        # query = "SELECT * FROM fixture WHERE local = %s AND fase = %s"
        # params = ["Boca", "final"]
        # el execute haria algo asi: SELECT * FROM fixture WHERE local = 'Boca' AND fase = 'final'

        partidos = cursor.fetchall()

        #armo el HATEOAS
        #cada pagina ocupa limit posiciones. (avanzar->sumar limit) (retroceder->restar limit)

        base_url = request.base_url

        ultimo_offset = max(total - limit,0)

        links = {
            "_first": f"{base_url}?_limit={limit}&_offset=0",
            "_prev": f"{base_url}?_limit={limit}&_offset={max(offset - limit, 0)}",
            "_next": f"{base_url}?_limit={limit}&_offset={offset + limit}",
            "_last": f"{base_url}?_limit={limit}&_offset={ultimo_offset}"
        }
        cursor.close()
        conn.close()

        #no hay contenido, quizas por un parametro ingresado incorrectamente
        if not partidos:
            return '', 204

        # Todo salió correctamente
        return jsonify({"data":partidos,"links":links}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500



@partidos_db.route("/",methods=["POST"])
def crear_partido():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "Body vacío"}), 400

        local=data.get("local")
        visitante=data.get("visitante")
        fecha=data.get("fecha")
        fase=data.get("fase")
        
        #validaciones 400
        if not local or not visitante or not tiene_formato_string(local) or not tiene_formato_string(visitante):
            return jsonify({"error": "Faltan equipos"}), 400

        if not es_fecha_correcta(fecha):
            return jsonify({"error": "Fecha inválida"}), 400

        #una vez validado todo
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        #validaciones 409 - local-visitante-fecha ya existe en el db
        #filtro por local,visitante y fecha ingresado por el cliente
        cursor.execute("""SELECT * FROM fixture WHERE local = %s AND visitante = %s AND fecha = %s""",(local,visitante,fecha))
        partido_existente= cursor.fetchone()

        if partido_existente:
            #ya se hizo el partido
            cursor.close()
            conn.close()
            return jsonify({"error": "ya existe un partido con esos equipos y fecha"}), 409

        cursor.execute("""
                       INSERT INTO fixture (local, visitante, fecha, fase)
                       VALUES (%s, %s, %s, %s)
                       """, (local, visitante,fecha, fase))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje":"Equipo agregado correctamente"}), 201
    except Exception as e:
        print(e)
        return jsonify({"error": "Error interno del servidor"}), 500


    
#PARTIDOS POR ID
@partidos_db.route('/<id_fixture>', methods=['GET'])
def obtener_partido(id_fixture):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if not id_fixture.isdigit():
            cursor.close()
            conn.close()
            return respuesta_error(code=400, message='Bad Request', level='error', description='No es id')
        id = int(id_fixture)
        cursor.execute("SELECT * FROM fixture WHERE id_fixture = %s ", (id,))
        partido = cursor.fetchone()
        if partido is None:
            cursor.close()
            conn.close()
            return respuesta_error(code=404, message='Not found', level = 'error', description=f"No se encuentra el partido con el id: {id}")
        cursor.close()
        conn.close()
        return jsonify({'id_fixture': partido['id_fixture'],
                        'equipo_local': partido['local'],
                        'equipo_visitante': partido['visitante'],
                        'fecha': partido['fecha'],
                        'fase': partido['fase'],
                        'resultado':{
                            'local': partido['goles_local'],
                            'visitante': partido['goles_visitante']
                        }}),200

    except Exception:

        return respuesta_error(code=500, message='Internal Server Error', level = 'error', description = 'error server')

#ELIMINAR PARTIDO
@partidos_db.route('/<id_fixture>', methods=['DELETE'])
def eliminar_partido(id_fixture):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if not id_fixture.isdigit():
            cursor.close()
            conn.close()
            return respuesta_error(code=400, message='Bad Request', level='error', description='No es id')
        id = int(id_fixture)
        cursor.execute("DELETE FROM fixture WHERE id_fixture = %s ", (id,))
        conn.commit()
        partido = cursor.rowcount
        if partido == 0:
            cursor.close()
            conn.close()
            return respuesta_error(code=404, message='Not found', level='error',
                                   description=f"No se encuentra el partido con el id: {id}")
        if partido == 1:
            cursor.close()
            conn.close()
            return '', 204
    except Exception:
        return respuesta_error(code=500, message='Internal Server Error', level='error', description='error server')

#RESULTADOS
@partidos_db.route('/<id_fixture>/resultado', methods=['PUT'])
def actualizar_resultado(id_fixture):

    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if not id_fixture.isdigit():
            cursor.close()
            conn.close()
            return respuesta_error(code=400, message='Bad Request', level='error', description='No es id')
        id = int(id_fixture)
        data = request.get_json()
        if not data:
            cursor.close()
            conn.close()
            return respuesta_error(code=400, message='Bad Request', level='error', description='Faltan datos')
        local = data.get('local')
        visitante = data.get('visitante')
        if local is None or visitante is None:
            cursor.close()
            conn.close()
            return respuesta_error(code=400, message='Bad Request', level='error', description='Faltan datos')
        try:
            local = int(local)
            visitante = int(visitante)
        except (ValueError, TypeError):
            cursor.close()
            conn.close()
            return respuesta_error(code=400, message='Bad Request', level='error', description='Datos incorrectos')
        if local < 0 or visitante < 0:
            cursor.close()
            conn.close()
            return respuesta_error(code=400, message='Bad Request', level='error', description='Datos incorrectos')
        cursor.execute("UPDATE fixture SET goles_local = %s, goles_visitante = %s WHERE id_fixture = %s ", (local, visitante,id))
        conn.commit()
        resultado = cursor.rowcount

        if resultado == 0:
            cursor.close()
            conn.close()
            return respuesta_error(code=404, message='Not found', level='error',
                                   description=f"No se encuentra el partido con el id: {id}")
        cursor.close()
        conn.close()
        return '', 204
    except Exception:
        return respuesta_error(code=500, message='Internal Server Error', level='error', description='error server')


#Opcional

@partidos_db.route("/<int:id_fixture>", methods=['PUT'])
def put_partido(id_fixture):
    data = request.get_json()

    campos = ["equipo_local", "equipo_visitante", "fecha", "fase"]

    for campo in campos:
        if campo not in data:
            return {"error": f"Falta {campo}"}, 400


    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        UPDATE partidos
        SET equipo_local=?, equipo_visitante=?, fecha=?, fase=?
        WHERE id_fixture=?
    """, (
        data["equipo_local"],
        data["equipo_visitante"],
        data["fecha"],
        data["fase"],
        id_fixture
    ))

    if cursor.rowcount == 0:
        conn.close()
        return {"error": "No existe"}, 404

    conn.commit()
    conn.close()

    return {
        "data": {
            "id_fixture": id_fixture,
            **data
        }
    }, 200


#Opcional
@partidos_db.route("/<int:id_fixture>", methods=['PATCH'])
def patch_partido(id_fixture):
    data = request.get_json()

    campos_validos = ["equipo_local", "equipo_visitante", "fecha", "fase"]

    sets = []
    valores = []

    for clave, valor in data.items():
        if clave in campos_validos:
            sets.append(f"{clave}=?")
            valores.append(valor)

    if not sets:
        return {"error": "Nada para actualizar"}, 400

    valores.append(id_fixture)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    query = f"UPDATE partidos SET {', '.join(sets)} WHERE id_fixture=?"
    cursor.execute(query, valores)

    if cursor.rowcount == 0:
        conn.close()
        return {"error": "No existe"}, 404

    conn.commit()

    # obtener actualizado (esto lo pide swagger indirectamente)
    cursor.execute("SELECT * FROM partidos WHERE id_fixture=?", (id_fixture,))
    f = cursor.fetchone()

    conn.close()

    return {
        "data": {
            "id_fixture": f[0],
            "equipo_local": f[1],
            "equipo_visitante": f[2],
            "fecha": f[3],
            "fase": f[4]
        }
    }, 200


