from datetime import datetime
import os
from subprocess import getoutput


def debugpath() -> str:
    if os.name == 'posix':
        home = getoutput('echo $HOME')
        return os.path.join(home, '.xitu-debug')
    return '.xitu-debug'


def perfilnome(_folder: str) -> str or None:
    nome = compile("[aA-zZ]+")
    if nome.match(_folder):
        return _folder.split("-")[-1]
    return None


def created(_username: str):
    from src.basedados import BDB
    db = BDB()
    date_created = datetime.today()
    return db.insert_user(_nome=_username, _created=date_created)


def logged(_username: str):
    from src.basedados import BDB
    db = BDB()
    date_last_login = datetime.today()
    return db.update_lastlogin(_nome=_username, _last_login=date_last_login)


def localpath() -> str:
    return os.path.abspath(os.path.curdir)


def after(_sec: int, _do):
    while _sec > 0:
        _sec -= 1
    return _do
