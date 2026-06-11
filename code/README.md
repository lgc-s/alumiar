# Estrutura do Projeto Alumiar

## 📁 Organização de Pastas

O projeto foi reorganizado em pastas e módulos para melhor manutenção e escalabilidade:

```
code/
├── main.py                     # Arquivo principal - ponto de entrada
├── dados/                      # Módulo de dados
│   ├── __init__.py
│   └── dados.py               # Variáveis globais, validações e persistência
├── fluxo_adm/                 # Fluxo do Administrador
│   ├── __init__.py
│   ├── usuarios.py            # CRUD de usuários
│   ├── cursos.py              # CRUD de cursos
│   ├── eventos.py             # CRUD de eventos
│   └── menu_adm.py            # Menu principal do administrador
├── fluxo_usuario/             # Fluxo do Usuário (Artesã)
│   ├── __init__.py
│   ├── perfil.py              # Gerenciamento de perfil
│   ├── artesas.py             # Visualização de artesãs
│   ├── eventos.py             # Inscrição em eventos
│   ├── cursos.py              # Inscrição em cursos
│   ├── calculadora.py         # Calculadora de preços
│   └── menu_user.py           # Menu principal do usuário
└── README.md                  # Este arquivo
```

## 🚀 Como Executar

Para executar o programa, use:

```bash
python main.py
```

## 📝 Descrição dos Módulos

### **dados/**
- **dados.py**: Contém todas as variáveis globais, funções de validação de dados (email, telefone, idade) e funções para carregar/salvar dados em JSON.

### **fluxo_adm/**
- **usuarios.py**: Gerencia CRUD de usuários (cadastrar, listar, editar, deletar)
- **cursos.py**: Gerencia CRUD de cursos
- **eventos.py**: Gerencia CRUD de eventos
- **menu_adm.py**: Menu principal do administrador que integra todos os submenu

### **fluxo_usuario/**
- **perfil.py**: Visualizar e atualizar perfil do usuário
- **artesas.py**: Listar e pesquisar outras artesãs cadastradas
- **eventos.py**: Listar, pesquisar e inscrever-se em eventos
- **cursos.py**: Listar, pesquisar e inscrever-se em cursos
- **calculadora.py**: Calculadora de preços baseada em materiais, horas e margem de lucro
- **menu_user.py**: Menu principal do usuário que integra todos os submenu

### **main.py**
- Arquivo principal que contém o menu inicial e a função de login
- Gerencia a navegação entre fluxo administrativo e fluxo de usuário

## 🔐 Credenciais de Teste

**Administrador:**
- Email: `ADM`
- Senha: `123`

## 📋 Funcionalidades

### Administrador pode:
- ✅ Cadastrar, editar, listar e deletar usuários
- ✅ Cadastrar, editar, listar e deletar eventos
- ✅ Cadastrar, editar, listar e deletar cursos

### Usuário (Artesã) pode:
- ✅ Visualizar e atualizar seu perfil
- ✅ Listar e pesquisar outras artesãs
- ✅ Listar, pesquisar e inscrever-se em eventos
- ✅ Listar, pesquisar e inscrever-se em cursos
- ✅ Usar a calculadora de preços

## 💾 Dados Persistentes

Os dados são salvos em arquivos JSON na raiz do projeto:
- `dados_usuarios.json` - Dados de usuários
- `dados_cursos.json` - Dados de cursos
- `dados_eventos.json` - Dados de eventos
