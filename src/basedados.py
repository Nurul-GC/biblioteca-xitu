import sqlite3
from src.funcoextra import debugpath


class BDB:
    @staticmethod
    def connect_db():
        """criando conexão com a db sqlite

        :return: resultado da conexao
        """
        try:
            return sqlite3.connect(f"{debugpath()}/xitu.db")
        except sqlite3.Error as erro:
            raise erro

    # biblioteca main base dados
    def criar_tabela_livros(self):
        query = "CREATE TABLE IF NOT EXISTS livro" \
                "(id integer primary key autoincrement," \
                " nome varchar(50) not null," \
                " autor varchar(50) not null," \
                " anopublicado varchar(10) not null," \
                " editora varchar(50) not null," \
                " estado varchar(10) not null);" \

        return self.criar_tabela(_query=query)

    def criar_tabela_jornais(self):
        query = "CREATE TABLE IF NOT EXISTS jornal" \
                "(id integer primary key autoincrement," \
                " nome varchar(50) not null," \
                " volume varchar(50) not null," \
                " mes varchar(10) not null," \
                " ano varchar(10) not null," \
                " estado varchar(10) not null);"

        return self.criar_tabela(_query=query)

    def criar_tabela(self, _query):
        """criando tabela dos jogadores

        :return: resultado da conexao
        """
        db = self.connect_db()
        try:
            sql = db.cursor()
            result = sql.execute(_query)
            db.commit()
            return result
        except sqlite3.Error as erro:
            db.rollback()
            raise erro
        finally:
            db.close()

    def add_livro(self, _nome, _autor, _anopublicado, _editora, _estado):
        """adicionando livros novos a BD

        :param _nome: nome do livro
        :param _autor: nome autor
        :param _anopublicado: ano publicacao
        :param _editora: nome editora
        :param _estado: estado do livro (alugado ou disponivel)
        :return: resultado da conexao
        """
        db = self.connect_db()
        query = 'INSERT INTO livro' \
                '(nome,autor,anopublicado,editora,estado)' \
                f'VALUES("{_nome}","{_autor}","{_anopublicado}","{_editora}", "{_estado}");'

        try:
            sql = db.cursor()
            result = sql.execute(query)
            db.commit()
            return result
        except sqlite3.Error as erro:
            db.rollback()
            raise erro
        finally:
            db.close()

    def add_jornal(self, _nome, _volume, _mes, _ano, _estado):
        """adicionando jornais novos a BD

        :param _nome: nome do jornal
        :param _volume: volume do jornal
        :param _mes: mes publicacao
        :param _ano: ano publicacao
        :param _estado: estado do jornal (alugado ou disponivel)
        :return: resultado da conexao
        """
        db = self.connect_db()
        query = 'INSERT INTO jornal' \
                '(nome,volume,mes,ano,estado)' \
                f'VALUES("{_nome}","{_volume}","{_mes}","{_ano}", "{_estado}");'

        try:
            sql = db.cursor()
            result = sql.execute(query)
            db.commit()
            return result
        except sqlite3.Error as erro:
            db.rollback()
            raise erro
        finally:
            db.close()

    def ver_livros(self):
        """selecionar os livros guardados na db

        :return: os dados em uma lista
        """
        db = self.connect_db()
        query = "SELECT nome,autor,anopublicado,editora,estado FROM livro;"
        try:
            sql = db.cursor()
            sql.execute(query)
            result = sql.fetchall()
            db.commit()
            return result
        except sqlite3.Error as erro:
            db.rollback()
            raise erro
        finally:
            db.close()

    def ver_jornais(self):
        """selecionar os jornais guardados na db

        :return: os dados em uma lista
        """
        db = self.connect_db()
        query = "SELECT nome,volume,mes,ano,estado FROM jornal;"
        try:
            sql = db.cursor()
            sql.execute(query)
            result = sql.fetchall()
            db.commit()
            return result
        except sqlite3.Error as erro:
            db.rollback()
            raise erro
        finally:
            db.close()

    def apagar_materiais(self, _tipo):
        """apagar todos os materiais ja guardados

        :param _tipo: livro ou jornal
        :return: resultado da conexao
        """
        db = self.connect_db()
        query = f"DELETE FROM {_tipo};"
        try:
            sql = db.cursor()
            result = sql.execute(query)
            db.commit()
            return result
        except sqlite3.Error as erro:
            db.rollback()
            raise erro
        finally:
            db.close()

    def atualizar_material(self, _tipo, _nome, _estado):
        db = self.connect_db()
        try:
            executor = db.cursor()
            resultado = executor.execute(f"UPDATE {_tipo} SET estado=?"
                                         "WHERE nome=?;", (_estado, _nome))
            if resultado:
                db.commit()
                db.close()
                return True
        except Exception as erro:
            print(erro)
            return False
        if not db:
            raise ConnectionError(f"Erro ao conectar a db!\nconnection_result:{db}")
