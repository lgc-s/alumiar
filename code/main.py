# ============================================================
# MAIN - Sistema de Apoio às Artesãs
# Ponto de entrada da aplicação
# ============================================================

import dados.dados as dados_module
from fluxo_usuario.menu_user import menu_user
from fluxo_adm.menu_adm import menu_adm
from fluxo_adm.usuarios import cadastrar
from dados.dados import carregar_dados, salvar_dados

def login():
    """Realiza o login do usuário (artesã ou administrador)."""
    while True:

        print("\n==== Login ====\n")
        email = input("- Email: ").strip()
        senha = input("- Senha: ").strip()

        # Login do administrador
        if email == "ADM" and senha == "123":
            menu_adm()
            return

        # Login de usuário (artesã)
        else:
            for id, usuario in dados_module.usuarios.items():
                if usuario["email"] == email and usuario["senha"] == senha:
                    dados_module.id_logado = id
                    menu_user()
                    return

        print("Email ou Senha inválidos, tente novamente...")

        continuar = input("Tentar novamente? [S/N]: \n").strip().upper()
        while continuar not in ("S", "N"):
            continuar = input(
                "Resposta Inválida, tente novamente...\n- Tentar novamente? [S/N]): ").strip().upper()

        if continuar == "N":
            break


def menu_inicial():
    """
    Exibe o menu principal em loop e direciona para as funcionalidades do sistema.

    Opções disponíveis:
        1 - Cadastrar novo usuário
        2 - Login
        0 - Encerrar o programa
    """
    carregar_dados()
    while True:

        opcao = input("""\n============================================================

                ALUMIAR APP (Menu Inicial)

============================================================

1 - Cadastro
2 - Login
0 - Sair
            
Escolha: """).strip()

        if opcao == "1":
            cadastrar()
        elif opcao == "2":
            login()
        elif opcao == "0":
            salvar_dados()
            break  # Encerra o loop e finaliza o programa
        else:
            print("Comando inválido, tente novamente...")


# ============================================================
# PONTO DE ENTRADA DA APLICAÇÃO
# ============================================================

if __name__ == "__main__":
    menu_inicial()
