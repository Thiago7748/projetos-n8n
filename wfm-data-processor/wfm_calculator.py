import pandas as pd
import datetime


def sec_to_timedelta(seconds):
    return pd.to_timedelta(seconds, unit="s")


def calculate_wfm_metrics():
    print("--- 📊 WFM Data Processor (ETL) ---")
    print("Lendo bases mockadas do Twilio e CSAT/Zendesk...\n")

    # 1. Carregar Dados
    df_twilio = pd.read_csv("base_twilio_mock.csv")
    df_atendidas = pd.read_csv("base_atendidas_mock.csv")

    # 2. Conversão de Tipos
    # Transforma segundos do Twilio em timedelta para facilitar cálculos matemáticos com horas
    df_twilio["Duration"] = sec_to_timedelta(df_twilio["Activity Time (s)"])
    df_twilio["Datetime"] = pd.to_datetime(
        df_twilio["Date"] + " " + df_twilio["Time"], format="%m/%d/%Y %H:%M:%S"
    )

    # 3. Categorização de Atividades (Lógica de Negócios / Agrupamentos)
    almoco_categories = ["Pré-Almoço", "Almoço"]
    improdutivo_hc_categories = [
        "Desconectado",
        "Particular",
        "Pausa BH",
        "Tok - Pausa 15",
    ]
    operacional_categories = [
        "Treinamento",
        "Reunião",
        "Preleção",
        "Pré-FeedBack",
        "Feedback",
        "Tratativa e-mail",
        "Task",
    ]
    sistema_categories = ["Sistema"]

    # 4. Agregação por Agente
    results = []

    agrupado = df_twilio.groupby("Agent")
    for agente, df_agente in agrupado:
        # Ordena cronologicamente os eventos do agente no dia
        df_agente = df_agente.sort_values("Datetime")

        # Log In (Primeiro evento do dia) e Log Out (Último evento do dia)
        log_in = df_agente.iloc[0]["Datetime"].time()

        ultima_linha = df_agente.iloc[-1]
        # Se a última atividade não for Desconectado, soma a duração da última atividade
        if ultima_linha["Activity"] == "Desconectado":
            log_out_dt = ultima_linha["Datetime"]
        else:
            log_out_dt = ultima_linha["Datetime"] + ultima_linha["Duration"]
        log_out = log_out_dt.time()

        # Tempo total logado (Trabalhado bruto)
        horas_trabalhadas = log_out_dt - df_agente.iloc[0]["Datetime"]

        # Cálculo de Banco de Horas (Comparação com SLA Contratual de 08:20:00)
        sla_turno = pd.Timedelta(hours=8, minutes=20)
        if horas_trabalhadas > sla_turno:
            bh_realizado = horas_trabalhadas - sla_turno
        else:
            bh_realizado = pd.Timedelta(seconds=0)

        # Agrupamento de Pausas
        tempo_almoco = df_agente[df_agente["Activity"].isin(almoco_categories)][
            "Duration"
        ].sum()
        tempo_improdutivo_hc = df_agente[
            df_agente["Activity"].isin(improdutivo_hc_categories)
        ]["Duration"].sum()
        tempo_operacional = df_agente[
            df_agente["Activity"].isin(operacional_categories)
        ]["Duration"].sum()
        tempo_sistema = df_agente[df_agente["Activity"].isin(sistema_categories)][
            "Duration"
        ].sum()

        # Buscar quantidade de Atendidas (Merge/PROCX com a base de CSAT)
        try:
            atendidas = df_atendidas.loc[
                df_atendidas["agent"] == agente, "Atendidas"
            ].values[0]
        except IndexError:
            atendidas = 0

        # Formata o output visualmente
        def fmt(td):
            if pd.isna(td) or td.total_seconds() == 0:
                return "00:00:00"
            total_sec = int(td.total_seconds())
            h = total_sec // 3600
            m = (total_sec % 3600) // 60
            s = total_sec % 60
            return f"{h:02d}:{m:02d}:{s:02d}"

        results.append(
            {
                "Agente": agente,
                "Log In": log_in.strftime("%H:%M:%S"),
                "Log Out": log_out.strftime("%H:%M:%S"),
                "Horas Trabalhadas": fmt(horas_trabalhadas),
                "BH Realizado": fmt(bh_realizado)
                if bh_realizado.total_seconds() > 0
                else "Sem BH",
                "Almoço": fmt(tempo_almoco),
                "Improdutivo HC": fmt(tempo_improdutivo_hc),
                "Improdutivo Sist.": fmt(tempo_sistema),
                "Atividades Op.": fmt(tempo_operacional),
                "Atendidas": atendidas,
            }
        )

    # 5. Criar Dataframe Final e exibir
    df_resultado = pd.DataFrame(results)

    print(df_resultado.to_string(index=False))
    print("\n✅ Processamento concluído com sucesso!")

    # Opcional: exportar para Excel/CSV
    # df_resultado.to_csv('resultado_wfm.csv', index=False)


if __name__ == "__main__":
    calculate_wfm_metrics()
