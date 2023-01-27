from src.basedados import BDB


db = BDB()

db.criar_tabela_livros()

db.add_livro(
    _nome="minha vidinha",
    _autor="nurul-gc",
    _editora="artesgc inc",
    _anopublicado="1999",
    _estado="disponivel"
)
db.add_livro(
    _nome="meu renascimento",
    _autor="nurul-gc",
    _editora="artesgc inc",
    _anopublicado="2018",
    _estado="disponivel"
)

print(db.ver_livros())
