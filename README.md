# MDSIS - Sistema de Gestão de Metas e Indicadores

Este é um sistema de gestão de metas e indicadores desenvolvido em Django, projetado para permitir que utilizadores acompanhem o seu progresso e administradores façam a gestão global da plataforma.

## Funcionalidades

### Para Utilizadores
* **Gestão de Metas**: Criação, visualização, edição e exclusão de metas pessoais.
* **Monitorização de Progresso**: Acompanhamento visual da quantidade atual vs. quantidade total.
* **Indicadores**: Visualização de métricas de desempenho.

### Para Administradores (Staff)
* **Dashboard Administrativo**: Visão geral do sistema com total de metas e utilizadores ativos.
* **Gestão Global**: Capacidade de listar, editar e eliminar metas de qualquer utilizador.
* **Gestão de Perfis**: Controlo sobre contas de utilizadores, permitindo ativar/desativar perfis.

## Tecnologias Utilizadas

* **Framework**: [Django 5.0+](https://www.djangoproject.com/)
* **Linguagem**: Python 3.12+
* **Base de Dados**: SQLite (Desenvolvimento)
* **Frontend**: HTML5, CSS3, Bootstrap 5 (UI Responsiva)

## Estrutura do Projeto (Apps)

* `goals/`: Gere a lógica central das metas e indicadores.
* `users/`: Responsável pela autenticação e perfis de utilizador.
* `analytics/`: Contém as views e lógicas do painel administrativo.

## Configuração e Instalação

1.  **Clonar o repositório**:
    ```bash
    git clone https://github.com/masteguim/mdsis
    cd mdsis
    ```

2.  **Criar e ativar o ambiente virtual**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instalar as dependências**:
    ```bash
    pip install django
    ```

4.  **Executar migrações**:
    ```bash
    python3 manage.py makemigrations
    python3 manage.py migrate
    ```

5.  **Criar um Superusuário (Admin)**:
    ```bash
    python manage.py createsuperuser
    ```

6.  **Iniciar o servidor**:
    ```bash
    python manage.py runserver
    ```

## Acesso ao Painel
* **Utilizador Comum**: `/dashboard/`
* **Painel Administrativo**: `/painel/` (Apenas acessível por utilizadores com `is_staff=True`)

---
Desenvolvido como parte do projeto de Modelagem de Sistemas.


Por JooJdeSaaS e masteguim
