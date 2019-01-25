# Team xgboosters

Hackathon **Nexign Hack 2018**. QA case.

[![Build Status](https://travis-ci.org/DGKmaster/xgboosters.svg?branch=master)](https://travis-ci.org/DGKmaster/xgboosters)

---

## Project structure

* **code**
  * Project source code.
  * Each project version is placed in a separate folder.
  * Have separate readme for functionality description.
* **docs**
  * Output information about project testing.
  * This page is also available on [Github page](https://dgkmaster.github.io/xgboosters/)
* **run**
  * Scripts for program start.
* **tests**
  * Unit tests for program check.
* **docker**
  * Folder with Dockerfile for automatic container creation.
  * In container the app and its dependencies are installed.
* **.travis.yml**
  * Configuration file for Travis CI run.

---

## pip package creation

**1.** Create a packet

```bash
~$ python3 setup.py sdist
```

**2.** Install packet in ```lib/python3.7/site-packages```

```bash
~$ pip3 install smarthouse-1.0.0.tar.gz
```

---

## Get initial Docker container for Linux OS

Need to run next commands in terminal:

```bash
~$ sudo apt install docker-ce
~$ sudo usermod -aG docker $(whoami)
~$ sudo docker pull ubuntu

~$ docker build -t <repository name> <Dockerfile directory>

~$ sudo docker run -it <image name> /bin/bash
```

---
