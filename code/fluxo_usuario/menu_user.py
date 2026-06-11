# ============================================================
# MENU USUÁRIO
# ============================================================

from fluxo_usuario.perfil import menu_perfil
from fluxo_usuario.artesas import menu_artesas
from fluxo_usuario.eventos import menu_eventos
from fluxo_usuario.cursos import menu_cursos
from fluxo_usuario.calculadora import calculadora_precos


def menu_user():
    """Menu principal do usuário logado."""
    while True:
        opcao = input("""\n============================================================

                ALUMIAR APP (Menu Usuário)

============================================================

1 - Perfil
2 - Artesãs
3 - Eventos
4 - Cursos
5 - Calculadora de Preços
0 - Sair

Escolha: """).strip()

        if opcao == "1":
            menu_perfil()
        elif opcao == "2":
            menu_artesas()
        elif opcao == "3":
            menu_eventos()
        elif opcao == "4":
            menu_cursos()
        elif opcao == "5":
            calculadora_precos()
        elif opcao == "0":
            break
        else:
            print("Comando inválido, tente novamente...")
