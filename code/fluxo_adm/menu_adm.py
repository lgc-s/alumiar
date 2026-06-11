# ============================================================
# MENU ADMINISTRADOR
# ============================================================

from fluxo_adm.usuarios import menu_usuarios_adm
from fluxo_adm.eventos import menu_eventos_adm
from fluxo_adm.cursos import menu_cursos_adm


def menu_adm():
    """Menu principal do administrador."""
    while True:
        opcao = input("""\n============================================================

                ALUMIAR APP (Menu Administrador)

============================================================
                  
1 - Usuários
2 - Eventos
3 - Cursos
0 - Sair

Escolha: """).strip()

        if opcao == "1":
            menu_usuarios_adm()
        elif opcao == "2":
            menu_eventos_adm()
        elif opcao == "3":
            menu_cursos_adm()
        elif opcao == "0":
            break
        else:
            print("Comando inválido, tente novamente...")
