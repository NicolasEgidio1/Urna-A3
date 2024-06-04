import mysql.connector as banco
import bcrypt


 
class usuario:  
    def realiza_login(email, senha):
        sql_select = "SELECT id,nome, senha FROM usuario WHERE email = %s"
        connection = banco.connect(
            host="localhost", 
            user="root", 
            password="admin", 
            database="urna"
        )
        cursor = connection.cursor()
        cursor.execute(sql_select, (email,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        if result is None:
            return None
        id,nome, senha_hash = result
        cripto = Criptografia()
        if cripto.verifica_criptografia(senha, senha_hash):
            return nome
        return None  
    
    def insere_usuario(nome, sexo, telefone, cpf, cep, email, senha, logradouro, bairro, localidade, uf):
            sql_insert = "INSERT INTO usuario (nome, sexo, telefone, cpf, cep, email, senha, logradouro, bairro, localidade, uf) VALUES (%s, %s,'55' %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            connection = banco.connect(
                host="localhost", 
                user="root", 
                password="admin", 
                database="urna"
            )
            cripto = Criptografia()
            senha_hash = cripto.criptografar(senha)
            cursor = connection.cursor()
            cursor.execute(sql_insert, (nome, sexo, telefone, cpf, cep, email, senha_hash, logradouro, bairro, localidade, uf))
            connection.commit()
            cursor.close()
            connection.close()


class Criptografia:
    def criptografar(self, texto):
        salt = bcrypt.gensalt()
        hash_valor = bcrypt.hashpw(texto.encode('utf-8'), salt)
        return hash_valor
    
    def verifica_criptografia(self, senha, senha_hash):
        return bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8'))
    
class Votos:
    def votar(candidato_id):
        connection = banco.connect(
            host="localhost", 
            user="root", 
            password="admin", 
            database="urna"
        )
        
        cursor = connection.cursor()
        try:
            cursor.execute('UPDATE candidatos SET votos = votos + 1 WHERE id = %s', (candidato_id,))
            connection.commit()
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()
