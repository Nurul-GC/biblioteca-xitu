from os import makedirs
from random import randint
from sys import argv
from time import sleep

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from gcrypter import decrypt, encrypt

from src.basedados import *
from src.funcoextra import *


def init():
    def iniciar():
        load = 0
        while load < 100:
            janela.showMessage(f"Processando Módulos: {load}%", align, Qt.GlobalColor.black)
            sleep(0.3)
            load += randint(2, 10)
        janela.close()
        executavel.inicio_sessao()

    img = QPixmap(os.path.abspath("favicon/favicon-400x400.png"))
    align = int(Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignAbsolute)
    janela = QSplashScreen(img)
    janela.setStyleSheet(tema)
    janela.show()
    iniciar()


class XITU:
    def __init__(self):
        self.app = QApplication(argv)
        QFontDatabase.addApplicationFont(os.path.abspath("font/copse.ttf"))

        # ******* global-vars *******
        self.db = BDB()
        self.utilizador = None
        self.ferramentas = QWidget()

        self.janelaprincipal = QMainWindow()
        self.janelaprincipal.setWindowIcon(QIcon("favicon/favicon-400x400.png"))
        self.janelaprincipal.setWindowTitle("Biblioteca - Xitu")
        self.janelaprincipal.setMinimumSize(500, 500)
        self.janelaprincipal.setStyleSheet(tema)

        # ******* background-image *******
        bg_image = QImage(f"favicon/bg.png")
        set_bg_image = bg_image.scaled(QSize(100, 100))  # resize Image to widget's size
        palette = QPalette()
        palette.setBrush(palette.ColorGroup.All, palette.ColorRole.Window, QBrush(set_bg_image))
        self.ferramentas.setPalette(palette)

        # ******* layout-janelas *******
        hbox = QHBoxLayout()
        self.layout = QVBoxLayout()

        # ******* menu-bar *******
        menu = QMenuBar()
        detalhes = menu.addMenu('&Ajuda')

        instr = detalhes.addAction('&Instruções')
        instr.triggered.connect(self._instr)
        detalhes.addSeparator()

        sair = detalhes.addAction('&Sair')
        sair.triggered.connect(self._sair)

        sobre = menu.addAction('&Sobre')
        sobre.triggered.connect(self._sobre)

        # ******* list-options *******
        self.listaJanelas = QListWidget(self.ferramentas)
        self.listaJanelas.setAlternatingRowColors(True)
        self.listaJanelas.setFixedSize(QSize(200, 100))
        self.listaJanelas.addItem("Registrar Materiais")
        self.listaJanelas.addItem("Alugar Materiais")
        self.listaJanelas.addItem("Devolver Materiais")
        hbox.addWidget(self.listaJanelas)

        # ******* init-windows *******
        self.janela1 = QWidget()
        self.registrar_materiais()

        self.janela2 = QWidget()
        self.alugar_materiais()

        self.janela3 = QWidget()
        self.devolver_materiais()

        # ******* stack *******
        self.stack = QStackedWidget(self.ferramentas)
        self.stack.addWidget(self.janela1)
        self.stack.addWidget(self.janela2)
        self.stack.addWidget(self.janela3)
        hbox.addWidget(self.stack)

        self.layout.addLayout(hbox)
        self.janelaprincipal.setMenuBar(menu)
        self.ferramentas.setLayout(self.layout)
        self.listaJanelas.currentRowChanged.connect(self.alterar_janela)
        self.janelaprincipal.setCentralWidget(self.ferramentas)

    def _instr(self):
        pass

    def _sobre(self):
        pass

    def _sair(self):
        pass

    # molduras-usuario
    def cadastro(self):
        def guardar():
            if utilizador_cd.text() == '' or codigo.text() == '':
                QMessageBox.warning(self.ferramentas, 'Cadastro',
                                    'Você Deve Preencher todos os Seus Dados Antes de Entrar..')
            else:
                if codigo.text() != codigo1.text():
                    QMessageBox.warning(
                        self.ferramentas,
                        'Cadastro',
                        f'Lamento {utilizador_cd.text()} os Códigos Não Correspondem, Tente Novamente..')
                else:
                    makedirs(f'{debugpath()}/{utilizador_cd.text()}', exist_ok=True)
                    with open(f'{debugpath()}/{utilizador_cd.text()}/utilizador.log', 'w+') as file_user:
                        texto = f"""TITULO: {tipoconta.currentText()}
NOME: {utilizador_cd.text()}
SENHA: {codigo.text()}
N-BI: {resposta.text()}"""
                        doc1, doc2 = encrypt(texto)
                        file_user.write(str(doc1) + '\n' + str(doc2))
                    janela_cadastro.destroy()
                    QMessageBox.information(self.ferramentas, 'Cadastro',
                                            f"Parabens {utilizador_cd.text()} o seu cadastro foi bem sucedido\n"
                                            f"agora inicie sessão para desfrutar do programa..")

        janela_cadastro = QDialog(self.janelaprincipal)
        janela_cadastro.setWhatsThis("Cadastro: permite ao usuario personalizar uma conta com nome e senha!")
        janela_cadastro.setWindowTitle("Cadastro")
        janela_cadastro.setFixedSize(350, 350)

        layout = QFormLayout()
        layout.setSpacing(20)

        layout.addRow(QLabel("<h3>Preencha os Seus Dados:</h3><hr>"))

        tipos = ['professor', 'estudante', 'visitante']
        tipoconta = QComboBox()
        tipoconta.addItems(tipos)
        layout.addRow('Selecione o tipo de conta:', tipoconta)

        utilizador_cd = QLineEdit()
        utilizador_cd.setToolTip('Obrigatório')
        utilizador_cd.setPlaceholderText('Digite o Seu Nome..')
        layout.addRow(utilizador_cd)

        resposta = QLineEdit()
        resposta.setToolTip('Obrigatório')
        resposta.setPlaceholderText('Digite o seu número do bilhete..')
        resposta.setMaxLength(14)  # aceita apenas a quantidade certa de digitos do BI
        resposta.setInputMask('999999999AA999')  # validacao do numero do BI
        layout.addRow(resposta)

        codigo = QLineEdit()
        codigo.setEchoMode(codigo.EchoMode.PasswordEchoOnEdit)
        codigo.setClearButtonEnabled(True)
        codigo.setToolTip('Obrigatório')
        codigo.setPlaceholderText('Digite a Sua Senha..')
        layout.addRow(codigo)

        codigo1 = QLineEdit()
        codigo1.setEchoMode(codigo1.EchoMode.PasswordEchoOnEdit)
        codigo1.setClearButtonEnabled(True)
        codigo1.setToolTip('Obrigatório')
        codigo1.setPlaceholderText('Redigite a Sua Senha..')
        codigo1.returnPressed.connect(guardar)
        layout.addRow(codigo1)

        guardar_botao = QPushButton('Entrar')
        guardar_botao.setDefault(True)
        guardar_botao.clicked.connect(guardar)
        layout.addRow(guardar_botao)

        janela_cadastro.setLayout(layout)
        janela_cadastro.show()

    def inicio_sessao(self):
        def iniciar():
            try:
                with open(f'{debugpath()}/{utilizador_is.text()}/utilizador.log', 'r+') as file_user:
                    filelines = file_user.readlines()
                    file = decrypt(
                        text_enc=(
                            int(filelines[0]),
                            int(filelines[1])
                        )
                    )
                    if utilizador_is.text() in file and codigo.text() in file and tipoconta.currentText() in file:
                        self.utilizador = utilizador_is.text()
                        janela_inicio_sessao.destroy()
                        self.janelaprincipal.show()
                    elif tipoconta.currentText() not in file:
                        QMessageBox.information(
                            self.ferramentas,
                            'Falha ao Iniciar Sessão',
                            f'Lamento {utilizador_is.text()} os seus dados não correspondem com os gravados..\n'
                            f'Tente novamente!'
                        )
                    else:
                        question = QMessageBox.question(
                            self.ferramentas,
                            'Falha ao Iniciar Sessão',
                            f'Lamento {utilizador_is.text()} Você Ainda Não Tem Uma Conta Criada..\n'
                            f'Registre-se Para Continuar Usando o Programa!')
                        if question == QMessageBox.StandardButton.Yes:
                            self.cadastro()
                        elif question == QMessageBox.StandardButton.No:
                            self.app.exit(0)
            except FileNotFoundError:
                question = QMessageBox.question(
                    self.ferramentas,
                    'Falha ao Iniciar Sessão',
                    f'Lamento {utilizador_is.text()} Você Ainda Não Tem Uma Conta Criada..\n'
                    f'Registre-se Para Continuar Usando o Programa!')
                if question == QMessageBox.StandardButton.Yes:
                    self.cadastro()
                elif question == QMessageBox.StandardButton.No:
                    self.app.exit(0)

        janela_inicio_sessao = QDialog(self.janelaprincipal)
        janela_inicio_sessao.setWindowTitle('Iniciar Sessão')
        janela_inicio_sessao.setFixedSize(500, 300)

        layout = QFormLayout()
        layout.setSpacing(10)

        layout.addRow(QLabel("<h2>Preencha os Seus Dados<br>Para Iniciar Sessão:</h2><hr>"))

        tipos = ['professor', 'estudante', 'visitante']
        tipoconta = QComboBox()
        tipoconta.addItems(tipos)
        layout.addRow('Selecione o tipo de conta:', tipoconta)

        utilizador_is = QLineEdit()
        utilizador_is.setToolTip('Obrigatório')
        utilizador_is.setPlaceholderText('Digite o Seu Nome..')
        layout.addRow(utilizador_is)

        codigo = QLineEdit()
        codigo.setEchoMode(codigo.EchoMode.PasswordEchoOnEdit)
        codigo.setClearButtonEnabled(True)
        codigo.setToolTip('Obrigatório')
        codigo.returnPressed.connect(iniciar)
        codigo.setPlaceholderText('Digite a Sua Senha..')
        layout.addRow(codigo)

        recuperar_senha = QLabel(
            '<a href="#" style="text-decoration:none; color:blue;">Esqueceu a sua senha?</a>')
        recuperar_senha.setToolTip(
            'Permite-lhe recuperar o seu login atravez da sua resposta especial fornecida no cadastro\n'
            'Caso ainda não tenha feito o cadastro, fá-lo já!')
        recuperar_senha.linkActivated.connect(self.recuperar_senha)
        recuperar_senha.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(recuperar_senha)

        layout_btns = QHBoxLayout()
        iniciar_botao = QPushButton('Entrar')
        iniciar_botao.clicked.connect(iniciar)
        iniciar_botao.setDefault(True)
        layout_btns.addWidget(iniciar_botao)

        cadastro_botao = QPushButton('Cadastrar')
        cadastro_botao.clicked.connect(self.cadastro)
        layout_btns.addWidget(cadastro_botao)
        layout.addRow(layout_btns)

        janela_inicio_sessao.setLayout(layout)
        janela_inicio_sessao.show()

    def recuperar_senha(self):
        def iniciar():
            try:
                with open(f'{debugpath()}/{nome.text()}/utilizador.log', 'r+') as file_user:
                    filelines = file_user.readlines()
                    file = decrypt(int(filelines[0]), int(filelines[1]))
                    if nome.text() in file and resposta.text() in file:
                        logged(_username=nome.text())
                        janela_recuperar_senha.destroy()
                        self.janelaprincipal.show()
                    else:
                        question = QMessageBox.question(
                            self.ferramentas,
                            'Falha ao Iniciar Sessão',
                            f"Lamento {nome.text()} a sua Resposta está Errada ou Você Ainda Não Tem Uma Conta Criada."
                            f"\nRegistre-se Para Continuar Usando o Programa!")
                        if question == QMessageBox.StandardButton.Yes:
                            janela_recuperar_senha.destroy()
                            self.cadastro()
                        elif question == QMessageBox.StandardButton.No:
                            return self.app.exit(0)
            except FileNotFoundError:
                question = QMessageBox.question(
                    self.ferramentas,
                    'Falha ao Iniciar Sessão',
                    f"Lamento {nome.text()} Você Ainda Não Tem Uma Conta Criada..\n"
                    f"Registre-se Para Continuar Usando o Programa!")
                if question == QMessageBox.StandardButton.Yes:
                    janela_recuperar_senha.destroy()
                    self.cadastro()
                elif question == QMessageBox.StandardButton.No:
                    return self.app.exit(0)

        janela_recuperar_senha = QDialog(self.janelaprincipal)
        janela_recuperar_senha.setWhatsThis("Sobre: Recuperação da sessão do úsuario!\n"
                                            "Poderá sempre iniciar sessão atravez desta opção caso esqueça "
                                            "permanentemente a sua senha..")
        janela_recuperar_senha.setWindowTitle('Recuperar Senha')
        janela_recuperar_senha.setFixedSize(300, 200)

        layout = QFormLayout()
        layout.setSpacing(10)

        layout.addRow(QLabel("<h3>Preencha os Seus Dados:</h3><hr>"))

        nome = QLineEdit()
        nome.setToolTip('Obrigatório')
        nome.setPlaceholderText('Digite o seu Nome de utilizador..')
        layout.addRow(nome)

        resposta = QLineEdit()
        resposta.setToolTip('Obrigatório')
        resposta.setPlaceholderText('Digite o seu número do bilhete..')
        resposta.setMaxLength(14)  # aceita apenas a quantidade certa de digitos do BI
        resposta.setInputMask('999999999AA999')  # validacao do numero do BI
        layout.addRow(resposta)

        confirmar = QPushButton('Confirmar')
        confirmar.setDefault(True)
        confirmar.clicked.connect(iniciar)
        layout.addRow(confirmar)

        janela_recuperar_senha.setLayout(layout)
        janela_recuperar_senha.show()

    # janela-biblioteca
    def registrar_materiais(self):
        def guardar():
            if nome.text().isspace() or nome.text() == "":
                QMessageBox.warning(
                    self.janelaprincipal,
                    "Atenção",
                    "<b>Não é possivel registrar sem o nome do material, Tente novamente!</b>"
                )
            else:
                if tipo.currentText() == 'livro':
                    self.db.criar_tabela_livros()
                    self.db.add_livro(
                        _nome=nome.text(),
                        _autor=autor.text(),
                        _anopublicado=anopublicado.text(),
                        _editora=editora.text(),
                        _estado=estado.currentText()
                    )
                elif tipo.currentText() == 'jornal':
                    self.db.criar_tabela_jornais()
                    self.db.add_jornal(
                        _nome=nome.text(),
                        _volume=volume.text(),
                        _mes=mes.text(),
                        _ano=ano.text(),
                        _estado=estado.currentText()
                    )

        def mudartipo():
            if tipo.currentText() == 'livro':
                hlayout.removeWidget(volume)
                hlayout.addWidget(autor, 0, 2)

                hlayout.removeWidget(mes)
                hlayout.addWidget(anopublicado, 1, 0)

                hlayout.removeWidget(ano)
                hlayout.addWidget(editora, 1, 1)
            else:
                hlayout.removeWidget(autor)
                hlayout.addWidget(volume, 0, 2)

                hlayout.removeWidget(anopublicado)
                hlayout.addWidget(mes, 1, 0)

                hlayout.removeWidget(editora)
                hlayout.addWidget(ano, 1, 1)

        hlayout = QGridLayout()
        vlayout = QVBoxLayout()

        infolabel = QLabel("<h1>Registro de Novos Materiais</h1><hr>")
        infolabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vlayout.addWidget(infolabel)

        tipos = ['livro', 'jornal']
        tipo = QComboBox()
        tipo.addItems(tipos)
        tipo.currentTextChanged.connect(mudartipo)
        hlayout.addWidget(tipo, 0, 0)

        nome = QLineEdit()
        nome.setPlaceholderText("Digite o nome do material..")
        hlayout.addWidget(nome, 0, 1)

        autor = QLineEdit()
        autor.setPlaceholderText("Digite o nome do autor do material..")
        volume = QLineEdit()
        volume.setPlaceholderText("Digite o volume de publicação do material..")
        hlayout.addWidget(autor, 0, 2)

        anopublicado = QLineEdit()
        anopublicado.setPlaceholderText("Digite o ano de publicação do material..")
        mes = QLineEdit()
        mes.setPlaceholderText("Digite o mes de publicação do material..")
        hlayout.addWidget(anopublicado, 1, 0)

        editora = QLineEdit()
        editora.setPlaceholderText("Digite o nome da editora do material..")
        ano = QLineEdit()
        ano.setPlaceholderText("Digite o ano de publicação do material..")
        ano.setMaxLength(4)
        hlayout.addWidget(editora, 1, 1)

        estados = ['disponivel']
        estado = QComboBox()
        estado.addItems(estados)
        hlayout.addWidget(estado, 1, 2)
        vlayout.addLayout(hlayout)

        guardarbtn = QPushButton("Registrar")
        guardarbtn.clicked.connect(guardar)
        vlayout.addWidget(guardarbtn)

        self.janela1.setLayout(vlayout)

    def alugar_materiais(self):
        def guardar():
            if nome.text().isspace() or nome.text() == "":
                QMessageBox.warning(
                    self.janelaprincipal,
                    "Atenção",
                    "<b>Não é possivel registrar sem o nome do material, Tente novamente!</b>"
                )
            else:
                self.db.atualizar_material(
                    _tipo=tipo.currentText(),
                    _nome=nome.text(),
                    _estado=estado.currentText()
                )

        hlayout = QGridLayout()
        vlayout = QVBoxLayout()

        infolabel = QLabel("<h1>Aluguer de Materiais</h1><hr>")
        infolabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vlayout.addWidget(infolabel)

        tabelaframe = QScrollArea()
        scrlbar = QScrollBar()
        scrlbar.setOrientation(Qt.Orientation.Vertical)
        tabelaframe.setVerticalScrollBar(scrlbar)
        layouttabela = QVBoxLayout()
        for livro in self.db.ver_livros():
            layouttabela.addWidget(
                self.livrosframe(
                    livro[0], livro[1], livro[2], livro[3], livro[4]
                )
            )
        tabelaframe.setLayout(layouttabela)
        vlayout.addWidget(tabelaframe)

        tipos = ['livro', 'jornal']
        tipo = QComboBox()
        tipo.addItems(tipos)

        hlayout.addWidget(tipo, 0, 0)

        nome = QLineEdit()
        nome.setPlaceholderText("Digite o nome do material..")
        hlayout.addWidget(nome, 0, 1)

        estados = ['alugado']
        estado = QComboBox()
        estado.addItems(estados)
        hlayout.addWidget(estado, 1, 0)

        guardarbtn = QPushButton("Registrar")
        guardarbtn.clicked.connect(guardar)
        hlayout.addWidget(guardarbtn, 1, 1)
        vlayout.addLayout(hlayout)

        self.janela2.setLayout(vlayout)

    def devolver_materiais(self):
        def guardar():
            if nome.text().isspace() or nome.text() == "":
                QMessageBox.warning(
                    self.janelaprincipal,
                    "Atenção",
                    "<b>Não é possivel registrar sem o nome do material, Tente novamente!</b>"
                )
            else:
                self.db.atualizar_material(
                    _tipo=tipo.currentText(),
                    _nome=nome.text(),
                    _estado=estado.currentText()
                )

        hlayout = QGridLayout()
        vlayout = QVBoxLayout()

        infolabel = QLabel("<h1>Devolução de Materiais</h1><hr>")
        infolabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vlayout.addWidget(infolabel)

        tabelaframe = QScrollArea()
        scrlbar = QScrollBar()
        tabelaframe.setVerticalScrollBar(scrlbar)
        layouttabela = QVBoxLayout()
        for livro in self.db.ver_livros():
            layouttabela.addWidget(
                self.livrosframe(
                    livro[0], livro[1], livro[2], livro[3], livro[4]
                )
            )
        tabelaframe.setLayout(layouttabela)
        vlayout.addWidget(tabelaframe)

        tipos = ['livro', 'jornal']
        tipo = QComboBox()
        tipo.addItems(tipos)

        hlayout.addWidget(tipo, 0, 0)

        nome = QLineEdit()
        nome.setPlaceholderText("Digite o nome do material..")
        hlayout.addWidget(nome, 0, 1)

        estados = ['disponivel']
        estado = QComboBox()
        estado.addItems(estados)
        hlayout.addWidget(estado, 1, 0)

        guardarbtn = QPushButton("Registrar")
        guardarbtn.clicked.connect(guardar)
        hlayout.addWidget(guardarbtn, 1, 1)
        vlayout.addLayout(hlayout)

        self.janela3.setLayout(vlayout)

    @staticmethod
    def livrosframe(_nome, _autor, _anopublicado, _editora, _estado):
        frame = QWidget()
        frame.setFixedHeight(200)
        frame.setStyleSheet("border-radius:5px;"
                            "border-width:2px;"
                            "border-style:solid;"
                            "border-color:black;"
                            "background-color:white;")
        layout = QFormLayout()
        layout.addRow("Nome:", QLabel(_nome))
        layout.addRow("Autor:", QLabel(_autor))
        layout.addRow("Editora:", QLabel(_editora))
        layout.addRow("Ano Publicação", QLabel(_anopublicado))
        layout.addRow("Estado:", QLabel(_estado))
        selectbtn = QPushButton("Selecionar")
        layout.addRow(selectbtn)
        frame.setLayout(layout)
        return frame

    def alterar_janela(self, index):
        self.stack.setCurrentIndex(index)


if __name__ == '__main__':
    tema = open("theme/xitu.qss").read().strip()
    executavel = XITU()
    init()
    executavel.db.criar_tabela_livros()
    executavel.db.criar_tabela_jornais()
    executavel.app.exec()
