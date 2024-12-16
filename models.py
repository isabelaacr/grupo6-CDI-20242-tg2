#onde configuro as tabelas do banco de dados models.py

import mariadb
from db import get_db_connection
from datetime import datetime

# Função para buscar todos os pacientes
def get_all_pacientes():
    conn = get_db_connection()
    if conn is None:
        return None
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pacientes")
    pacientes = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return [
        {
            "ID": paciente[0],
            "Nome": paciente[1],
            "Cpf": paciente[2],
            "Restricoes": paciente[3],
            "quartosID": paciente[4]
        }
        for paciente in pacientes
    ]

def insert_paciente(data):
    conn = get_db_connection()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO pacientes (ID, Nome, Cpf, Restricoes, quartosID) VALUES (%s, %s, %s, %s, %s)",
        (data['ID'], data['Nome'], data['Cpf'], data['Restricoes'], data['quartosID'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return True

def get_count_pacientes():
    conn = get_db_connection()

    if conn is None:
        return None
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM pacientes") 
    count = cursor.fetchone()[0]  
    cursor.close()
    conn.close()

    return count

def get_count_pacientes_por_quarto():

    conn = get_db_connection()

    if conn is None:
        return None
    
    cursor = conn.cursor()
    cursor.execute("""
        SELECT quartosID, COUNT(*) 
        FROM pacientes 
        GROUP BY quartosID
    """)

    dados= cursor.fetchall()
    cursor.close()
    conn.close()

    return [{"quartoID": dado[0], "total_pacientes": dado[1]} for dado in dados]
    
def get_consultorios():
    
    conn = get_db_connection()

    if conn is None:
        return None
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consultorio")
    consultorios = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "ID"   : consultorio[0],
            "CNPJ" : consultorio[1]
        } for consultorio in consultorios
    ]

def get_all_receitas():

    conn = get_db_connection()

    if conn is None:
        return None
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM receita")

    receitas = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "receitaID" : receitas[0],
            "medicamento" : receitas[1]
        } for receita in receitas
    ]

def get_all_empregados():

    conn = get_db_connection()

    if conn is None:
        return None

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM empregados")

    empregados = cursor.fetchall()
    cursor.close()
    conn.close()

    return [
        {
            "empregadoID" : empregado[0],
            "nome"        : empregado[1],
            "CPF"         : empregado[2],
            "tipo"        : empregado[3]
        } for empregado in empregados
    ]

def insert_empregado(data):
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO empregados (ID, Nome, CPF, Tipo) VALUES (%s, %s, %s, %s)",
            (data['ID'], data['Nome'], data['CPF'], data['Tipo'])
        )
        conn.commit()
    except mariadb.Error as e:
        print(f"Erro ao inserir empregado: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

    return True

def insert_quarto(data):
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO quartos (ID, numero, consultorioID) VALUES (%s, %s, %s)",
            (data['ID'], data['numero'], data['consultorioID'])
        )
        conn.commit()
    except mariadb.Error as e:
        print(f"Erro ao inserir quarto: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

    return True

def insert_consulta(data):
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        # Garantir que a data está no formato correto (YYYY-MM-DD)
        data_consulta = data.get('data', None)
        if data_consulta:
            try:
                # Validar o formato da data
                datetime.strptime(data_consulta, "%Y-%m-%d")
            except ValueError:
                print("Formato de data inválido")
                return False

        
        preco = data['Preco'] if data['Preco'] is not None else None

        
        cursor.execute(
            """
            INSERT INTO simpleclinic.consulta (ID, pacientesID, medicaID, `data`, Preco) 
            VALUES (%s, %s, %s, %s, %s)
            """,
            (data['ID'], data['pacientesID'], data['medicaID'], data_consulta, preco)
        )
        conn.commit()
    except mariadb.Error as e:
        print(f"Erro ao inserir consulta: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

    return True

def insert_consultorio(data):
    conn = get_db_connection()
    if conn is None:
        return False

    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO consultorio (ID, CNPJ) 
            VALUES (%s, %s)
            """,
            (data['ID'], data['CNPJ'])
        )
        conn.commit()
    except mariadb.Error as e:
        print(f"Erro ao inserir consultório: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

    return True


