# ControleCombustivel

Sistema Desktop para controle de abastecimento de frotas, desenvolvido e entregue a um cliente real - e em uso continuo há meses sem relatos de falha.

## Sobre o Projeto

Desenvolvido sob demanda para um cliente que precisava registrar e acompanhar o consumo e combustivel de sua frota de veículos. O sistema substitui planilhas manuais e oferece relatórios analíticos com exportação para Excel, tudo em um executavel standalone que não exige instalação de python nem de nenhum banco de dados na maquina do usuario

---

## Funcionalidades 

- lançamento de abastecimentos por veículo e data
- Relatório anual com análise vertical (A/V%) e horizontal (A/H%)
- Total anual por veículo
- Exportação para Excel formatado
- impressão via excel
- Gestão de veículos com ativação/inativação
- Backup automatico incremental

---

## Stack

- Python 3.14
- CustomTkinter
- SQLite
- pywin32
- PyInstaller

---

## Como rodar o sistema

Basta apertar no botao releases do github, escolhe a versão mais atual e baixa o ControleCombustivel.rar

## Como gerar o executável
 
```bash
pyinstaller --onefile --windowed main.py
```

O `.exe` gerado estará na pasta `dist/` e pode ser distribuído sem necessidade de Python instalado na máquina de destino.


---


## Status

Em produção - sistema entregue e em uso ativo pelo cliente
