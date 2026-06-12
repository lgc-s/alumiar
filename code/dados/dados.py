# ============================================================
# MÓDULO DE DADOS - Alumiar
# Gerencia todas as variáveis globais, validações e persistência de dados
# ============================================================

from re import fullmatch
import json
import os
from datetime import datetime, date

# ============================================================
# CONFIGURAÇÃO DE CAMINHOS
# ============================================================

# Define o diretório onde os arquivos JSON serão salvos
# Sempre na raiz do projeto (diretório pai de 'code')
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
DADOS_DIR = BASE_DIR

# Caminhos completos dos arquivos JSON
ARQUIVO_USUARIOS = os.path.join(DADOS_DIR, 'dados_usuarios.json')
ARQUIVO_CURSOS = os.path.join(DADOS_DIR, 'dados_cursos.json')
ARQUIVO_EVENTOS = os.path.join(DADOS_DIR, 'dados_eventos.json')

# ============================================================
# VARIÁVEIS GLOBAIS
# ============================================================

# Dicionário principal que armazena todos os usuários cadastrados.
# Chave: ID inteiro | Valor: dicionário com os dados do usuário
usuarios = {}
cursos = []
eventos = []

# Contador global de ID, incrementado a cada novo cadastro
id = 1

# Variável global que armazena o ID registrado após login
id_logado = None


# ============================================================
# FUNÇÕES DE PERSISTÊNCIA DE DADOS
# ============================================================

def salvar_dados():
    """Salva os dados de usuários, cursos e eventos em arquivos JSON."""
    with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
        json.dump({"id": id, "usuarios": usuarios},
                  f, ensure_ascii=False, indent=2)

    with open(ARQUIVO_CURSOS, 'w', encoding='utf-8') as f:
        json.dump(cursos, f, ensure_ascii=False, indent=2)

    with open(ARQUIVO_EVENTOS, 'w', encoding='utf-8') as f:
        json.dump(eventos, f, ensure_ascii=False, indent=2)

    print("\nDados salvos com sucesso!")


def carregar_dados():
    """Carrega os dados de usuários, cursos e eventos dos arquivos JSON."""
    global id, usuarios, cursos, eventos

    if os.path.exists(ARQUIVO_USUARIOS):
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            id = dados["id"]
            usuarios = {int(k): v for k, v in dados["usuarios"].items()}

    if os.path.exists(ARQUIVO_CURSOS):
        with open(ARQUIVO_CURSOS, 'r', encoding='utf-8') as f:
            cursos = json.load(f)

    if os.path.exists(ARQUIVO_EVENTOS):
        with open(ARQUIVO_EVENTOS, 'r', encoding='utf-8') as f:
            eventos = json.load(f)


# ============================================================
# FUNÇÕES DE VALIDAÇÃO
# ============================================================

def validar_telefone(telefone):
    """
    Valida se o telefone informado é um celular brasileiro válido.

    Formato esperado: DDD (2 dígitos) + 9 + 8 dígitos = 11 dígitos no total.
    Exemplo válido: 81999999999

    Args:
        telefone (str): Número de telefone contendo apenas dígitos.

    Returns:
        bool: True se válido, False caso contrário.
    """
    regex = r'^\d{2}9\d{8}$'
    if fullmatch(regex, telefone):
        return True
    else:
        return False


def validar_e_calcular_idade(data_str):
    """
    Valida a data de nascimento (DD/MM/AAAA) e calcula a idade.
    Retorna a idade (int) se for válida (entre 1 e 120 anos), ou False caso contrário.
    """
    try:
        # Tenta converter a string no formato de data brasileira
        data_nascimento = datetime.strptime(data_str, "%d/%m/%Y").date()
        hoje = date.today()  # Pega a data exata de hoje no calendário do PC

        # Cálculo exato da idade considerando o mês e o dia atual
        idade = hoje.year - data_nascimento.year - ((hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day))

        # Mantém a idade entre 1 e 120 anos
        if 1 <= idade <= 120:
            return idade
        else:
            return False
    except ValueError:
        # Se o usuário digitar letras ou uma data inválida (ex: 30/02/2000)
        return False


def validar_email(email):
    """
    Valida se o e-mail informado possui um formato válido.

    Formato esperado: usuario@dominio.extensao
    A extensão pode ter entre 2 e 7 caracteres (ex: .com, .com.br).

    Args:
        email (str): Endereço de e-mail a ser validado.

    Returns:
        bool: True se válido, False caso contrário.
    """
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,7}$'
    if fullmatch(regex, email):
        return True
    else:
        return False


def verificar_email_existente(email):
    """
    Verifica se um e-mail já está vinculado a algum usuário cadastrado.

    Percorre todos os usuários no dicionário e compara os e-mails,
    impedindo duplicatas no sistema.

    Args:
        email (str): E-mail a ser verificado.

    Returns:
        bool: True se o e-mail já existe, False caso contrário.
    """
    for usuario in usuarios.values():
        if usuario["email"] == email:
            return True
    return False
