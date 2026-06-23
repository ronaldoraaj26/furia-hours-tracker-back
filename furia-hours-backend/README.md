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
furia-hours-backend/
├── docker-compose.yml
├── .env.example
├── backend/
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── manage.py
│   ├── requirements.txt
│   ├── furia_backend/
│   └── apps/
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

## Endpoints principais

Base URL: `http://localhost:8000/api/`

- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/auth/me/`
- `GET /api/users/`
- `GET /api/projects/`
- `GET /api/categories/`
- `GET /api/time-entries/`
- `GET /api/approvals/`
- `GET /api/file-attachments/`
- `GET /api/calendar-events/`
- `GET /api/audit-logs/`

## Fluxo sugerido de integração com o frontend

1. login real via `/api/auth/login/`
2. listar modalidades via `/api/projects/`
3. cadastrar atividade via `/api/time-entries/`
4. subir comprovantes via `/api/file-attachments/`
5. listar histórico via `/api/time-entries/?mine=1`
6. alimentar calendário via `/api/calendar-events/`

## Observações importantes

- O projeto usa autenticação por token próprio, alinhada ao diagrama recebido.
- O campo `approved` em `time_entries` é mantido sincronizado com `approvals.status`.
- O middleware de auditoria registra operações de escrita na API.
- O backend foi preparado para **desenvolvimento local**, não para produção final.
