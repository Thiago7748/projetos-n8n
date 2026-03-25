# WFM Data Processor (ETL em Python) 🐍

Este sub-projeto demonstra como reescrever arquiteturas pesadas e lógicas complexas de negócios (geralmente presas em planilhas e fórmulas como SOMASES/PROCX) para a linguagem **Python** utilizando a biblioteca `pandas`.

A conversão de regras de *Workforce Management* (WFM) para código garante:
- **Escalabilidade:** Capaz de processar centenas de milhares de linhas de logs da telefonia instantaneamente.
- **Automação:** Pode ser integrado a rotinas de banco de dados (Cron Jobs, Airflow) sem necessidade de intervenção humana em planilhas.

## 🚀 Como funciona

O script `wfm_calculator.py` realiza:
1. **Leitura (Extract):** Ingere as bases de logs de telefonia (`base_twilio_mock.csv`) e chamadas atendidas (`base_atendidas_mock.csv`).
2. **Tratamento (Transform):** 
   - Converte os dados temporais para formatos adequados (Timedelta).
   - Agrupa os logs individuais pelo nome do agente.
   - Calcula o Log In inicial e o Log Out final considerando a duração das atividades sistêmicas.
   - Aplica a lógica condicional de SLAs (turnos de 08:20:00) para calcular banco de horas.
3. **Cruzamento (Load):** Consolida todos os indicadores na tabela final.

### Como testar localmente:
```bash
pip install pandas
python wfm_calculator.py
```
*(As bases CSVs locais contêm dados fictícios estruturados (mocks) para demonstração).*
