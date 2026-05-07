# Banco de Questões

Aplicação web desenvolvida em Django para estudo com questões de múltipla escolha.

---

## Requisitos

- Python 3.10+
- Pip

---

## Instalação

```bash
# 1. Clone o repositório e entre na pasta
cd bancoquestoes

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\Activate.ps1  # Windows PowerShell

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Aplique as migrations
python manage.py migrate

# 5. Crie um superusuário para acessar o admin
python manage.py createsuperuser

# 6. Rode o servidor
python manage.py runserver
```

Acesse em: http://127.0.0.1:8000

---

## Telas

| Tela | URL | Descrição |
|---|---|---|
| Home | `/` | Página inicial. Sem login: apresentação do site. Com login: saudação, total de questões resolvidas, acertos, erros e gráfico anual. |
| Login | `/login` | Autenticação do usuário. |
| Cadastro | `/cadastro/` | Criação de nova conta. |
| Questões | `/questoes/` | Lista de questões com filtros por matéria e nível. Navegação uma por vez com Anterior/Próxima. Ao final exibe o resultado. Requer login. |
| Minha Conta | `/minha-conta/` | Permite alterar e-mail, senha e foto de perfil. Requer login. |
| Admin | `/admin/` | Painel administrativo do Django. Requer superusuário. |

---

## Admin

Acesse `/admin/` com o superusuário criado. No painel você pode:

**Questões**
- Adicionar, editar e excluir questões
- Cada questão deve ter exatamente 5 alternativas, sendo exatamente 1 correta
- Campos: título, enunciado, ano, nível (Fácil/Médio/Difícil) e matéria

**Estudantes**
- Criados automaticamente quando um novo usuário se cadastra
- Contém a foto de perfil vinculada ao usuário

**Questões Feitas**
- Registro de todas as respostas dos usuários
- Exibe: usuário, questão (com link direto), alternativa escolhida, se acertou e data

---

## Tabelas do banco

| Tabela | Descrição |
|---|---|
| `auth_user` | Usuários do Django (nativo) |
| `nossoapp_estudantes` | Perfil estendido do usuário com foto |
| `nossoapp_questoes` | Questões com enunciado, ano, nível e matéria |
| `nossoapp_alternativa` | Alternativas (A-E) vinculadas a cada questão |
| `nossoapp_questaofeita` | Respostas dos usuários com data e resultado |

---

## Matérias disponíveis

- Matemática
- Linguagens
- Ciências Humanas
- Ciências da Natureza

## Níveis disponíveis

- Fácil
- Médio
- Difícil
