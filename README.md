# Portfólio de Automações e Integrações (n8n)

Este repositório contém as exportações JSON dos meus principais workflows construídos no **n8n**.

Cada arquivo `.json` presente aqui pode ser importado diretamente para qualquer instância do n8n para visualização do fluxo. Abaixo, detalho a arquitetura e o propósito de cada um deles.

---

## 1. Suporte Automatizado ao Cliente
![Workflow Interview Case](./assets/interview-case.png)
**Arquivo:** `Interview_Case.json`

Um case técnico focado em otimização de atendimento ao cliente via e-mail, utilizando inteligência artificial para ler, classificar e redigir respostas baseadas em dados de plataformas externas (Mocks de Shopify e CRM).

**Arquitetura do Fluxo:**
1. **Trigger:** Monitora a caixa de entrada do Gmail buscando por e-mails com a tag "Pendente".
2. **Registro:** Faz o backup do e-mail recebido em uma planilha do Google Sheets.
3. **Roteamento:** Um nó `Switch` atua como roteador principal, analisando o conteúdo/assunto para direcionar o fluxo para a esteira correta de atendimento (Cancelamento, Andamento, Parado ou Fallback).
4. **Respostas Templates:** Para cenários conhecidos, injeta respostas padronizadas em templates, mantendo o tom de voz da marca.
5. **Enriquecimento de Dados:** Faz consultas a APIs simuladas (Shopify para status de pedidos e CRM para histórico do cliente).
6. **IA Generativa:** Emprega o Google Gemini para analisar os dados enriquecidos e gerar uma resposta humanizada e contextualizada.
7. **Ação Final:** Cria um rascunho (draft) da resposta no Gmail, pronto para ser revisado ou disparado por um atendente humano.

**Destaques de Engenharia:**
- Uso de nós condicionais e lógicos (`Switch`, `If`) para garantir que apenas os fluxos necessários sejam executados, economizando recursos.
- Tratamento de Mocks de API para simular um ambiente de produção real.
- Delegação de tarefas cognitivas (entendimento de contexto) para LLMs (Large Language Models).

---

## 2. Backend MVP (OrçaAqui)
![Workflow Backend MVP](./assets/orcaaqui.png)
**Arquivo:** `Backend_OrcaAqui_MVP.json`

Desenvolvido para atuar como o backend completo de uma aplicação SaaS (Single Page Application hospedada na Vercel). O n8n expõe Webhooks que o Front-End consome via fetch nativo, eliminando a necessidade de um servidor Node.js intermediário.

**Arquitetura do Fluxo:**
1. **Webhooks GET/POST:** Atuam como endpoints de uma API RESTful.
   - `/webhook/orcaaqui-get-pedidos`: Retorna a lista de pedidos.
   - `/webhook/orcaaqui-post-proposta`: Recebe novas propostas e salva no banco de dados.
   - `/webhook/orcaaqui-analise-ia`: Endpoint avançado para análise inteligente.
2. **Banco de Dados (Google Sheets):** Leitura e escrita otimizada na planilha que atua como o banco relacional do MVP.
3. **IA Analítica (Gemini):**
   - Recebe um `id_pedido`.
   - Busca no banco todas as propostas relacionadas a esse ID.
   - Envia o contexto em lote para o Google Gemini via requisição HTTP (API REST nativa).
   - A IA atua como um "consultor financeiro", comparando as propostas, apontando o melhor custo-benefício e formatando a saída de volta para o frontend.
4. **Tratamento de Rate Limit:** O frontend consome este fluxo já esperando possíveis respostas HTTP `429 Too Many Requests`, lidando de forma graciosa com os limites da IA.

**Destaques de Engenharia:**
- Construção de "API-less Backend": O n8n assume total responsabilidade pelas regras de negócios e rotas.
- Otimização de prompts para que a IA processe matrizes de dados complexos (múltiplas propostas e valores) e retorne insights diretos.

---

## 3. Integração Simples de Dados (Case de Faculdade)
![Workflow Case Faculdade](./assets/facul-case.png)
**Arquivo:** `case_projeto_facul.json`

Um projeto acadêmico demonstrando os fundamentos de extração e disponibilização de dados utilizando Webhooks como micro-serviços.

**Arquitetura do Fluxo:**
1. **Endpoint 1 (`/livros`):** Acionado via GET, busca dados em uma tabela "Livros_Destaque" e retorna o payload limpo para o front-end consumir.
2. **Endpoint 2 (`/avisos`):** Acionado via GET, busca dados em uma tabela "Avisos" e retorna a lista de recados.

**Destaques de Engenharia:**
- Demonstra entendimento da estrutura `Request -> Process -> Response`.
- Uso eficiente de Webhooks para servir conteúdo dinâmico (Headless CMS com Google Sheets).
