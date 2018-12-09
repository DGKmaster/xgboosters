# Команда xgboosters

Хакатон **Nexign Hack 2018**. Тема QA.

[![Build Status](https://travis-ci.org/DGKmaster/xgboosters.svg?branch=master)](https://travis-ci.org/DGKmaster/xgboosters)

---

## Структура проекта

* **code**
  * Исходный код проекта.
  * В отдельной папке находится каждая из версий проекта.
  * Есть отдельный README для описания функциональности.
* **run**
  * Скрипты запуска программы.
* **tests**
  * Unit тесты для проверки программы.
  * Для
* **docker**
  * Папка с Dockerfile для автоматического создания контейнера.
  * В контейнере будет установлено само приложение и его рабочее окружением.
* **.travis.yml**
  * Файл конфигурации для запуска Travis CI.

---

## Создание пакета

1. Создаем пакет
```bash
~$ python3 setup.py sdist
```
2. Устанавливаем пакет в ```lib/python3.7/site-packages```
```bash
~$ pip3 install smarthouse-1.0.0.tar.gz
```

---

## Получение начального docker контейнера для ОС Linux

Необходимо выполнить следующие команды в терминале
```bash
~$ sudo apt install docker-ce
~$ sudo usermod -aG docker $(whoami)
~$ sudo docker pull ubuntu
```

---