# FURIA Hours Tracker - Backend Django

Backend em Django + Django REST Framework para o projeto **FURIA Hours Tracker**, preparado para rodar localmente com **Docker Compose + MySQL**.

## O que foi modelado

Este backend foi construído a partir de:

- o frontend React enviado
- o diagrama do banco enviado
- as decisões de arquitetura discutidas antes da implementação

## Assunções adotadas

Para conseguir iniciar o projeto sem bloquear a implementação, assumi o seguinte:

- **Projects** representam as modalidades do frontend (`LoL`, `Valorant`, `CS2`, etc.)
- **Categories** representam categorias acadêmicas/administrativas de horas
- **Time entries** são os lançamentos de horas
- **Approvals** controlam o fluxo de aprovação
- **File attachments** armazenam comprovantes
- **Tokens** são usados para autenticação por token própria

Além das tabelas do diagrama, foram adicionadas duas extensões para cobrir recursos que já existem no frontend:

- `TimeEntryParticipant`: participantes do registro de atividade
- `CalendarEvent`: agenda da aba calendário

## Estrutura

```bash
.
├── docker-compose.yml
├── .env
├── .env.example
├── Dockerfile
├── entrypoint.sh
├── manage.py
├── requirements.txt
├── asgi.py
├── settings.py
├── urls.py
├── wsgi.py
├── pagination.py
├── apps/
├── .venv/
└── README.md
```

## Como rodar

1. Copie o arquivo de ambiente:

```bash
cp .env.example .env
```

2. Suba os containers:

```bash
docker compose up --build
```

3. Em outro terminal, rode as migrations:

```bash
docker compose exec backend python manage.py makemigrations
docker compose exec backend python manage.py migrate
```

4. Crie um superusuário:

```bash
docker compose exec backend python manage.py createsuperuser
```

5. Opcional: popular dados iniciais:

```bash
docker compose exec backend python manage.py seed_initial_data
```

6. As modalidades usadas pelo front são criadas automaticamente pela migration de dados `apps.hours.0003_seed_projects`, então um `migrate` limpo já deixa `GET /api/projects/` com as oito opções esperadas.

## Documentação do backend

### Visao geral

Base URL: `http://localhost:8000/api/`

O backend foi organizado em 5 blocos principais:

- `auth`: login, logout e usuário autenticado
- `users` e `access`: usuários, perfis, permissões, roles e tokens
- `hours`: projetos, categorias, lançamentos de horas, participantes, aprovações, anexos e eventos de calendário
- `audit`: trilha de auditoria

### Autenticacao

O projeto usa autenticação por token próprio.

- Faça login em `POST /api/auth/login/`
- Envie o token no header:

```http
Authorization: Token <token>
```

O token:

- é emitido para o usuário autenticado
- expira conforme `TOKEN_EXPIRATION_HOURS`
- pode ser revogado em `POST /api/auth/logout/`

O endpoint `GET /api/auth/me/` retorna o usuário logado.

### Permissoes

O controle de acesso é feito por permissão atribuída ao role do usuário.

Permissões usadas no projeto:

- `manage_users`
- `manage_roles`
- `manage_permissions`
- `manage_tokens`
- `approve_time_entries`
- `manage_calendar_events`
- `view_audit_logs`

Regras importantes:

- superuser tem acesso total
- usuário sem role não passa nas permissões específicas
- rotas sem permissão extra continuam exigindo autenticação

### Paginação, busca e ordenacao

O backend usa a configuração padrão do DRF:

- `page` controla a página
- `page_size` controla o tamanho da página
- tamanho padrão: `20`
- tamanho máximo: `100`

Também há suporte a:

- `search`
- `ordering`

Exemplo:

```http
GET /api/time-entries/?search=cs2&ordering=-work_date&page=1&page_size=20
```

### Referencia das rotas

#### Auth

- `POST /api/auth/login/`
  - Entrada: `email`, `password`
  - Saída: `token`, `expires_at`, `user`
- `POST /api/auth/logout/`
  - Revoga o token atual
- `GET /api/auth/me/`
  - Retorna o usuário autenticado

#### Usuarios, roles e permissoes

- `GET/POST/PATCH/DELETE /api/users/`
  - Permissão: `manage_users`
- `GET/POST/PATCH/DELETE /api/roles/`
  - Permissão: `manage_roles`
- `GET/POST/PATCH/DELETE /api/permissions/`
  - Permissão: `manage_permissions`
- `GET/POST/PATCH/DELETE /api/role-permissions/`
  - Permissão: `manage_permissions`
- `GET /api/tokens/`
  - Permissão: `manage_tokens`

#### Horas

- `GET/POST/PATCH/DELETE /api/projects/`
  - Lista e mantém as modalidades usadas pelo frontend
  - `POST` e `PATCH` usam `name`, `description` e `active`
- `GET/POST/PATCH/DELETE /api/categories/`
  - Categorias acadêmicas ou administrativas
- `GET/POST/PATCH/DELETE /api/time-entries/`
  - Lançamentos de horas
  - `POST` e `PATCH` usam `project`, `category`, `work_date`, `start_time`, `end_time`, `hours_worked`, `description`
  - O `user` é preenchido automaticamente com o usuário logado
- `GET/POST/PATCH/DELETE /api/participants/`
  - Participantes vinculados a um lançamento
- `GET/POST/PATCH/DELETE /api/approvals/`
  - Fluxo de aprovação dos lançamentos
  - Permissão: `approve_time_entries`
  - `approver` é preenchido automaticamente
  - o campo `approved` em `time_entries` é sincronizado com `approvals.status`
- `GET/POST/PATCH/DELETE /api/file-attachments/`
  - Anexos e comprovantes vinculados ao lançamento
  - os campos `file_name`, `file_path`, `file_type` e `uploaded_at` são gerados pelo backend
- `GET/POST/PATCH/DELETE /api/calendar-events/`
  - Eventos da agenda/calendário
  - Permissão para escrita: `manage_calendar_events`
  - `created_by` é preenchido automaticamente

#### Auditoria

- `GET /api/audit-logs/`
  - Permissão: `view_audit_logs`
  - Registro de operações relevantes da API

### Fluxo sugerido de integração com o frontend

1. autenticar via `POST /api/auth/login/`
2. salvar o token e usar `Authorization: Token <token>`
3. listar modalidades via `GET /api/projects/`
4. listar categorias via `GET /api/categories/`
5. cadastrar atividade via `POST /api/time-entries/`
6. vincular participantes via `POST /api/participants/`
7. subir comprovantes via `POST /api/file-attachments/`
8. aprovar ou rejeitar via `POST /api/approvals/`
9. alimentar o calendário via `POST /api/calendar-events/`
10. consultar auditoria em `GET /api/audit-logs/`

### Regras de negocio relevantes

- `TimeEntry.clean()` valida que o horário final seja maior que o inicial
- `hours_worked` precisa ser maior que zero
- `hours_worked` não pode ultrapassar `category.max_hours`
- `Approval.save()` atualiza automaticamente o campo `approved` do `TimeEntry`
- `FileAttachment.save()` normaliza nome, caminho e tipo do arquivo
- `CalendarEvent` depende de um `project` existente

