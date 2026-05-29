# Baseline Deployment Quick Guide

## English

### 1. Purpose

This guide helps a new online Ubuntu / WSL Ubuntu machine install and check baseline adapter prerequisites from the GitHub checkout. An adapter is not the same as runtime: adapter code lives in this repo, while some real runtimes are external and optional.

### 2. Prerequisites

- Ubuntu / WSL Ubuntu.
- `Rewritebench_v0` cloned from GitHub.
- Base developer environment already installed, or run:

```bash
bash scripts/setup_dev_env_ubuntu.sh
```

- Internet access is available on the new machine.

### 3. Quick Start

```bash
bash scripts/setup_baseline_adapters.sh --profile core
bash scripts/check_baseline_adapters.sh --profile all-safe
```

### 4. Profiles

- `core`: installs/checks the editable project, `sqlglot`, `pytest`, SQLGlot adapter, Direct LLM adapters, and CLI help.
- `calcite`: checks Java 17 and the Calcite HEP adapter; optionally checks or unpacks a project-owner-prepared Calcite runtime archive.
- `prior-adapted`: checks R-Bot, LLM-R2, and LearnedRewrite adapted wrappers and prints only redacted environment-variable status.
- `all-safe`: runs safe checks for all profiles. No API call is made.

### 5. Baseline Status

- SQLGlot: Python package + adapter, ready after `sqlglot` install.
- Calcite HEP: adapter in repo, runtime optional/external. Use the maintained Calcite runtime archive prepared by the project owner, or build Calcite separately following Apache Calcite official documentation.
- Direct LLM: adapter in repo; live API requires local environment setup and explicit authorization.
- R-Bot / LLM-R2 / LearnedRewrite: adapted wrappers in repo; official upstream runtimes are not bundled and not automatically installed.

### 6. What Is Not Done

- No API call is made.
- No baseline run is performed.
- No Track A 120 run is performed.
- No DB/checker/timing run is performed.
- No paper metric is promoted.
- No reports/results update is made.

### 7. Output Policy

`check_baseline_adapters.sh` writes local reports only under:

```text
output/reports/baseline_env_check_<timestamp>/baseline_report.txt
```

Do not commit output/.

### 8. Troubleshooting

- `sqlglot` missing: run `bash scripts/setup_baseline_adapters.sh --profile core`.
- Java missing: install OpenJDK 17 with the base dev setup or your system package manager.
- Calcite runtime missing: provide `--calcite-runtime-root <path>` or `--calcite-runtime-archive <tar.gz>`; do not vendor Calcite into this repo.
- API env not configured: set local `SQLRB_LLM_*` or compatible provider variables outside Git. The scripts never print key values.
- Prior-method official runtime missing: use adapted wrappers or perform a separate reviewed upstream-runtime setup.

## Русский

### 1. Назначение

Это краткое руководство помогает быстро установить и проверить предпосылки для baseline adapters на новой online машине с Ubuntu / WSL Ubuntu. Адаптер не является средой выполнения: код адаптера находится в этом репозитории, а некоторые реальные runtime-среды являются внешними и необязательными. Иными словами, адаптер не является средой выполнения.

### 2. Предварительные требования

- Ubuntu / WSL Ubuntu.
- `Rewritebench_v0` склонирован из GitHub.
- Базовая среда разработки уже установлена, либо выполните:

```bash
bash scripts/setup_dev_env_ubuntu.sh
```

- На новой машине есть доступ к интернету.

### 3. Быстрый старт

```bash
bash scripts/setup_baseline_adapters.sh --profile core
bash scripts/check_baseline_adapters.sh --profile all-safe
```

### 4. Профили

- `core`: устанавливает/проверяет editable project, `sqlglot`, `pytest`, SQLGlot adapter, Direct LLM adapters и CLI help.
- `calcite`: проверяет Java 17 и Calcite HEP adapter; опционально проверяет или распаковывает архив Calcite runtime, подготовленный владельцем проекта.
- `prior-adapted`: проверяет адаптированные wrappers для R-Bot, LLM-R2 и LearnedRewrite и показывает только redacted статус переменных окружения.
- `all-safe`: выполняет безопасные проверки для всех профилей. API-вызовы не выполняются.

### 5. Статус baseline

- SQLGlot: Python package + adapter, готов после установки `sqlglot`.
- Calcite HEP: adapter есть в репозитории, runtime внешний и необязательный. Используйте поддерживаемый архив Calcite runtime от владельца проекта или соберите Calcite отдельно по официальной документации Apache Calcite.
- Direct LLM: adapter есть в репозитории; live API требует локальной настройки окружения и отдельного разрешения.
- R-Bot / LLM-R2 / LearnedRewrite: adapted wrappers есть в репозитории; official upstream runtimes не включены и автоматически не устанавливаются.

### 6. Что не выполняется

- API-вызовы не выполняются.
- Baseline run не выполняется.
- Track A 120 не запускается.
- DB/checker/timing не запускаются.
- Paper metric не продвигается.
- Обновление reports/results не выполняется.

### 7. Политика output

`check_baseline_adapters.sh` пишет только локальный отчет:

```text
output/reports/baseline_env_check_<timestamp>/baseline_report.txt
```

Не добавляйте output/ в коммит; для автоматической проверки формулировки: не добавляйте output/ в коммит.

### 8. Устранение проблем

- Нет `sqlglot`: выполните `bash scripts/setup_baseline_adapters.sh --profile core`.
- Нет Java: установите OpenJDK 17 через базовый dev setup или системный пакетный менеджер.
- Нет Calcite runtime: используйте `--calcite-runtime-root <path>` или `--calcite-runtime-archive <tar.gz>`; не добавляйте Calcite runtime в этот репозиторий.
- API env не настроен: задайте локальные `SQLRB_LLM_*` или совместимые provider variables вне Git. Скрипты никогда не печатают значения ключей.
- Нет official runtime для prior methods: используйте adapted wrappers или выполните отдельную проверенную настройку upstream runtime.
