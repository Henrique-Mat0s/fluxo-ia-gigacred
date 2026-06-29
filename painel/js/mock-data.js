// Dados mock — usado quando o painel roda sem Supabase configurado.
// Quando você plugar o Supabase, troca tudo isso por queries reais.

const MOCK_DATA = {
  // Status da instância Evolution
  instancia: {
    nome: "gigacred-bot-01",
    estado: "open",          // 'open' | 'connecting' | 'close'
    numero: "+55 31 99988-7766",
    ultimo_qr_em: "2026-06-28T08:14:00Z",
    mensagens_hoje: 127,
    limite_dia: 150,
    bloqueios_hoje: 3,
    taxa_bloqueio: 2.4,
  },

  // Config da IA
  config_ia: {
    ativa: true,
    modelo: "gemini-1.5-flash",
    api_key_configurada: true,
    requisicoes_hoje: 412,
    limite_dia: 1500,
    system_prompt: `Você é a Giovanna, consultora virtual da GIGACRED Correspondente.
Sua função é qualificar leads que querem antecipar FGTS, INSS ou consignado privado.

REGRAS:
- Tom caloroso, direto, brasileiro. Sem formalidades excessivas.
- NUNCA mais de 2 frases por mensagem.
- UMA pergunta por mensagem.
- Se o lead não fez adesão ao Saque-Aniversário, EXPLIQUE como fazer no app FGTS.
- NUNCA dê taxa específica ou prometa aprovação — isso é função do closer.

O QUE DESCOBRIR (BANT adaptado):
1. Saldo FGTS estimado
2. Adesão ao Saque-Aniversário (CRITÉRIO ELIMINATÓRIO)
3. Motivo do dinheiro
4. Urgência
5. Vínculo de trabalho`,
  },

  // Conversas ATIVAS (IA está trabalhando agora)
  conversas_ativas: [
    {
      id: "c1",
      nome: "José Oliveira",
      telefone: "+55 31 98765-4321",
      iniciais: "JO",
      ultima_msg_lead: "Acho que uns 8 mil",
      ultima_msg_ia: "Com R$ 8 mil dá pra antecipar até R$ 5.200 no PIX em 1-2 dias. Posso te chamar pra fechar?",
      ia_digitando: false,
      mensagens_trocadas: 7,
      iniciou_em: "14:20",
      score_atual: 88,
      proxima_acao: "aguardando_resposta",
    },
    {
      id: "c2",
      nome: "Maria Santos",
      telefone: "+55 21 99876-5432",
      iniciais: "MS",
      ultima_msg_lead: "Eu acho que tinha uns 10 mil mas faz tempo",
      ultima_msg_ia: "Beleza! E você já fez a adesão ao Saque-Aniversário no app da Caixa?",
      ia_digitando: false,
      mensagens_trocadas: 5,
      iniciou_em: "14:31",
      score_atual: 62,
      proxima_acao: "qualificando",
    },
    {
      id: "c3",
      nome: "Pedro Lima",
      telefone: "+55 11 97654-3210",
      iniciais: "PL",
      ultima_msg_lead: "Sou aposentado pelo INSS",
      ultima_msg_ia: "",
      ia_digitando: true,    // IA está formulando resposta
      mensagens_trocadas: 3,
      iniciou_em: "14:38",
      score_atual: 45,
      proxima_acao: "ia_digitando",
    },
    {
      id: "c4",
      nome: "Ana Souza",
      telefone: "+55 47 96543-2109",
      iniciais: "AS",
      ultima_msg_lead: "para de me mandar mensagem",
      ultima_msg_ia: "Tudo bem, peço desculpas pelo incômodo. Tenha um bom dia!",
      ia_digitando: false,
      mensagens_trocadas: 2,
      iniciou_em: "14:40",
      score_atual: 0,
      proxima_acao: "removido",
    },
    {
      id: "c5",
      nome: "Carlos Mendes",
      telefone: "+55 85 95432-1098",
      iniciais: "CM",
      ultima_msg_lead: "to interessado sim",
      ultima_msg_ia: "Show! Pra eu te ajudar melhor, qual seu vínculo de trabalho hoje?",
      ia_digitando: false,
      mensagens_trocadas: 4,
      iniciou_em: "14:42",
      score_atual: 58,
      proxima_acao: "qualificando",
    },
  ],

  // Leads QUALIFICADOS (passaram do score 80 — closer precisa ligar)
  pra_ligar: [
    {
      id: "l1",
      nome: "José Oliveira",
      telefone: "+55 31 98765-4321",
      iniciais: "JO",
      produto: "FGTS",
      valor_estimado: 5200,
      score: 88,
      resumo: "Saldo ~R$ 8k, adesão feita. Quitar dívida — urgente. Receber via PIX em 1-2 dias.",
      qualificado_ha: "agora",
      qualificado_em: new Date(Date.now() - 1 * 60 * 1000).toISOString(),
    },
    {
      id: "l2",
      nome: "Helena Carvalho",
      telefone: "+55 21 98123-4567",
      iniciais: "HC",
      produto: "FGTS",
      valor_estimado: 6800,
      score: 92,
      resumo: "Saldo ~R$ 12k, adesão feita há 2 anos. Reforma de casa, sem urgência extrema.",
      qualificado_ha: "há 6 min",
      qualificado_em: new Date(Date.now() - 6 * 60 * 1000).toISOString(),
    },
    {
      id: "l3",
      nome: "Roberto Alves",
      telefone: "+55 11 91234-5678",
      iniciais: "RA",
      produto: "Cons. INSS",
      valor_estimado: 4500,
      score: 85,
      resumo: "Aposentado INSS, sem restrição. Quer trocar dívida cara por consignado.",
      qualificado_ha: "há 14 min",
      qualificado_em: new Date(Date.now() - 14 * 60 * 1000).toISOString(),
    },
    {
      id: "l4",
      nome: "Sandra Costa",
      telefone: "+55 21 92345-6789",
      iniciais: "SC",
      produto: "FGTS",
      valor_estimado: 3900,
      score: 81,
      resumo: "Saldo ~R$ 6k, adesão feita. Pra viagem em julho. Prefere C6.",
      qualificado_ha: "há 22 min",
      qualificado_em: new Date(Date.now() - 22 * 60 * 1000).toISOString(),
    },
    {
      id: "l5",
      nome: "Felipe Santos",
      telefone: "+55 62 95678-9012",
      iniciais: "FS",
      produto: "Cons. Privado",
      valor_estimado: 7200,
      score: 83,
      resumo: "CLT estável, 3 anos de empresa, quer quitar dívidas. Sem restrição no SPC.",
      qualificado_ha: "há 38 min",
      qualificado_em: new Date(Date.now() - 38 * 60 * 1000).toISOString(),
    },
  ],
};

window.MOCK_DATA = MOCK_DATA;
