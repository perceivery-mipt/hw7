# HW7. CI/CD для ML-сервиса и безопасное развертывание модели

## Описание проекта

Проект выполнен в рамках модуля 7 «Автоматизированное развертывание с помощью CI/CD».

Цель работы — собрать воспроизводимый CI/CD-пайплайн для ML-проекта, реализовать безопасную стратегию развертывания модели и проверить работу сервиса локально и в CI-среде.

В проекте используется учебная ML-задача классификации датасета Iris. Базовый пайплайн `ml_pipeline.py` обучает модель `RandomForestClassifier`, считает метрику accuracy и используется для проверки воспроизводимости в CI/CD.

Для демонстрации развертывания реализован минимальный FastAPI ML-сервис `app.py`, построенный на той же логике: модель обучается на Iris, сервис возвращает статус, метрики и предсказание класса Iris по четырем признакам.

## Репозитории

GitLab:

```text
https://gitlab.com/perceivery-mipt/hw7
```

GitHub:

```text
https://github.com/perceivery-mipt/hw7
```

## Структура проекта

Проект организован так, чтобы отдельно хранить код ML-пайплайна, код сервиса, конфигурации CI/CD, файлы развертывания, ADR-документы и скриншоты проверок.

```text
.
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── doc/
│   └── architecture/
│       └── decisions/
│           ├── 0001-record-architecture-decisions.md
│           └── 0002-use-canary-deployment-for-ml-service.md
├── docs/
│   └── screenshots/
├── nginx/
│   ├── nginx.active.conf
│   ├── nginx-canary-90-10.conf
│   ├── nginx-canary-50-50.conf
│   ├── nginx-canary-100.conf
│   └── nginx-rollback.conf
├── notebooks/
│   └── HW7_CICD_Freydina_Alena_2.ipynb
├── scripts/
│   ├── check_service.sh
│   ├── rollback_to_stable.sh
│   ├── switch_to_50_50.sh
│   └── switch_to_100_canary.sh
├── .adr-dir
├── .gitignore
├── .gitlab-ci.yml
├── app.py
├── docker-compose.canary.yml
├── Dockerfile
├── ml_pipeline.py
├── README.md
└── requirements.txt
```

### Описание файлов и директорий

| Файл / директория | Назначение |
|---|---|
| `.github/workflows/ci.yml` | GitHub Actions workflow для проверки воспроизводимости offline ML-пайплайна. Устанавливает Python, ставит зависимости из `requirements.txt`, запускает `ml_pipeline.py`, сохраняет логи, метрики и артефакты выполнения. |
| `.github/workflows/deploy.yml` | GitHub Actions workflow для deployment-проверки ML-сервиса. Собирает Docker-образ из `Dockerfile`, запускает контейнер внутри GitHub Actions, проверяет endpoint’ы `/health`, `/metrics` и `/predict`, логинится в GitHub Container Registry и публикует образ. Шаг `Deploy via API` оставлен как безопасная заглушка, так как реальный cloud provider endpoint в проекте не используется. |
| `.gitlab-ci.yml` | GitLab CI/CD pipeline. Проверяет воспроизводимость проекта, устанавливает зависимости, запускает `ml_pipeline.py`, сохраняет отчеты, логи и метрики как artifacts. |
| `ml_pipeline.py` | Offline ML-пайплайн. Загружает датасет Iris, обучает `RandomForestClassifier`, считает accuracy и выводит результат. Используется в GitLab CI/CD и GitHub Actions для проверки воспроизводимого запуска модели. |
| `app.py` | FastAPI ML-сервис, построенный на той же логике, что и `ml_pipeline.py`. Поддерживает endpoint’ы `/health`, `/metrics` и `/predict`. Используется для демонстрации деплоя двух версий модели. |
| `requirements.txt` | Минимальный список зависимостей проекта. Включает библиотеки для ML-пайплайна и FastAPI-сервиса: `numpy`, `pandas`, `scikit-learn`, `fastapi`, `uvicorn`, `pydantic`. |
| `Dockerfile` | Инструкция для сборки Docker-образа ML-сервиса. Использует минимальный образ `python:3.11-slim`, устанавливает зависимости и запускает FastAPI через `uvicorn`. |
| `docker-compose.canary.yml` | Docker Compose-конфигурация для Canary Deployment. Поднимает три контейнера: `stable` с версией `v1.0.0`, `canary` с версией `v1.1.0` и `nginx` как балансировщик трафика. |
| `nginx/nginx.active.conf` | Активная конфигурация Nginx, которая монтируется внутрь контейнера балансировщика. Именно этот файл определяет текущее распределение трафика. |
| `nginx/nginx-canary-90-10.conf` | Начальная Canary-конфигурация: примерно 90% запросов направляются на стабильную версию `v1.0.0`, а 10% — на новую версию `v1.1.0`. |
| `nginx/nginx-canary-50-50.conf` | Промежуточная Canary-конфигурация: трафик распределяется между стабильной и новой версией примерно поровну. |
| `nginx/nginx-canary-100.conf` | Конфигурация полного переключения: весь трафик направляется на новую версию `v1.1.0`. |
| `nginx/nginx-rollback.conf` | Конфигурация отката: весь трафик возвращается на стабильную версию `v1.0.0`. |
| `scripts/check_service.sh` | Скрипт проверки сервиса. Выполняет запросы к `/health`, `/metrics` и `/predict`, чтобы убедиться, что ML-сервис работает корректно. |
| `scripts/switch_to_50_50.sh` | Скрипт переключения Nginx на режим Canary `50/50`. Копирует нужную конфигурацию в `nginx.active.conf` и перезапускает контейнер Nginx. |
| `scripts/switch_to_100_canary.sh` | Скрипт полного переключения на canary-версию `v1.1.0`. |
| `scripts/rollback_to_stable.sh` | Скрипт rollback. Возвращает весь трафик на стабильную версию `v1.0.0`. |
| `doc/architecture/decisions/` | Директория с ADR-документами. Используется для фиксации архитектурных решений проекта. |
| `doc/architecture/decisions/0001-record-architecture-decisions.md` | Первый ADR, созданный при инициализации `adr-tools`. Фиксирует решение использовать Architecture Decision Records. |
| `doc/architecture/decisions/0002-use-canary-deployment-for-ml-service.md` | Основной ADR проекта. В нем сравниваются Blue-Green и Canary Deployment, обосновывается выбор Canary Deployment и описываются риски выбранной стратегии. |
| `.adr-dir` | Служебный файл `adr-tools`, в котором хранится путь к директории ADR-документов. |
| `docs/screenshots/` | Директория со скриншотами проверок: успешный GitLab pipeline, запуск Docker Compose, работа endpoint’ов, Canary 90/10, 50/50, 100%, rollback и успешный GitHub Actions workflow. |
| `notebooks/HW7_CICD_Freydina_Alena_2.ipynb` | Итоговый ноутбук с выполнением домашнего задания, выводами, скриншотами и результатами проверок. |
| `.gitignore` | Исключает из Git служебные файлы Colab, Python-кэш, временные файлы, локальные директории и скачанный инструмент `adr-tools`. |
| `README.md` | Основная документация проекта: описание пайплайна, стратегии деплоя, запуска сервиса, A/B-теста, ADR и CI/CD. |
