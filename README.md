# 💼 e-Custo$ — Sistema para Gerenciamento de Custos

Este é um sistema desenvolvido em Python utilizando o padrão **MVVM**, com **PySide6** para a interface gráfica e **SQLite** como banco de dados.  
O projeto foi desenvolvido como apoio para a disciplina de **Custos** do curso de **Engenharia de Produção** da **UFCG**.

## 🎯 Objetivo

Facilitar o acesso, controle e análise de informações no contexto da disciplina de Custos, incluindo relatórios detalhados e visualizações gráficas.

## 🔧 Tecnologias Utilizadas

- 🐍 **Python 3.11+**
- 🖼️ **PySide6** (interface gráfica)
- 💾 **SQLite** (banco de dados local)
- 🧠 **Padrão MVVM** (Model-View-ViewModel)
- 📈 **Matplotlib** (gráficos e geração de PDFs)
- 📁 Estrutura modular com `model`, `view`, e `controller`

## ✨ Funcionalidades

- Cadastro de usuários  
- Login com validação  
- Armazenamento seguro em banco SQLite  
- 📊 **Geração de relatórios em PDF** com informações detalhadas de custos  
- 📉 **Criação de gráficos de custo unitário** automáticos e dinâmicos  

## 🛠️ Instalação

```bash
git clone https://github.com/eduardonsm/e-custos.git
cd e-custos
pip install -r requirements.txt


## Como usar

```bash
python login_system.py
```
![GitHub license](https://img.shields.io/github/license/eduardonsm/e-custos)
![Python](https://img.shields.io/badge/python-3.12%2B-green)
