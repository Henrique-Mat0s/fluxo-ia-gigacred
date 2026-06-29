// Disparador: pega leads com status='base', envia mensagem-isca com cadência
// anti-ban, marca cada disparo. Roda em background até bater o limite diário
// ou taxa de bloqueio crítica.

import {
  getLeadsParaDisparar, updateLead, insertMensagem,
  contarDisparosHoje, contarBloqueadosHoje,
} from "../db/supabase.js";
import { enviarTexto, numeroExiste } from "../evolution/client.js";

const VARIANTES = [
  "Oi! Tudo bem? Aqui é a Giovanna da GIGACRED. Você sabia que dá pra antecipar até 7 anos do seu saque-aniversário do FGTS e receber tudo no PIX?",
  "Olá! Sou a Giovanna, consultora da GIGACRED. Posso te mandar uma simulação rápida de quanto dá pra antecipar do seu FGTS?",
  "Oi, tudo bem? Giovanna aqui da GIGACRED. Tem alguns minutos pra eu te explicar como antecipar o FGTS sem complicação?",
  "Olá! Aqui é a GIGACRED. Você sabia que pode receber o seu FGTS agora, sem esperar o aniversário? Quer simular sem compromisso?",
  "Oi! Sou a Giovanna. Trabalho com antecipação de FGTS — em 1-2 dias úteis o dinheiro cai no seu PIX. Te interessa saber quanto dá?",
];

const LIMITE_DIA = parseInt(process.env.DISPARO_LIMITE_DIA || "150", 10);
const MIN_MS     = parseInt(process.env.DISPARO_MIN_INTERVALO_MS || "40000", 10);
const MAX_MS     = parseInt(process.env.DISPARO_MAX_INTERVALO_MS || "90000", 10);
const LIMITE_BLOQUEIO_PCT = parseFloat(process.env.DISPARO_LIMITE_BLOQUEIO_PCT || "5");

// Estado em memória do disparo em curso (idempotente: 1 disparo por processo)
let disparoEmCurso = false;

const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const aleatorio = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const variante = () => {
  const idx = Math.floor(Math.random() * VARIANTES.length);
  return { letra: "ABCDE"[idx], texto: VARIANTES[idx] };
};

/**
 * Inicia um disparo (não-bloqueante).
 * Roda em background até bater limite ou estourar taxa de bloqueio.
 * @returns {object} status inicial
 */
export async function iniciarDisparo() {
  if (disparoEmCurso) {
    return { ok: false, erro: "Já existe um disparo em andamento." };
  }

  // Quantos ainda dá pra disparar hoje?
  const enviadosHoje = await contarDisparosHoje();
  const restante = LIMITE_DIA - enviadosHoje;
  if (restante <= 0) {
    return { ok: false, erro: `Limite diário (${LIMITE_DIA}) já atingido.` };
  }

  // Pega leads da base
  const leads = await getLeadsParaDisparar(restante);
  if (leads.length === 0) {
    return { ok: false, erro: "Nenhum lead na base com status='base' pra disparar." };
  }

  disparoEmCurso = true;
  // Roda em background — não aguarda
  loopDisparo(leads).finally(() => { disparoEmCurso = false; });

  return {
    ok: true,
    iniciado: true,
    total_planejado: leads.length,
    restante_dia: restante,
    intervalo_estimado_min: Math.round(leads.length * (MIN_MS + MAX_MS) / 2 / 60000),
  };
}

async function loopDisparo(leads) {
  console.log(`[disparo] iniciando disparo de ${leads.length} leads`);

  for (const lead of leads) {
    // 1. Checa taxa de bloqueio (circuit breaker)
    const enviadosHoje = await contarDisparosHoje();
    const bloqueadosHoje = await contarBloqueadosHoje();
    const pctBloqueio = enviadosHoje > 0 ? (bloqueadosHoje / enviadosHoje) * 100 : 0;
    if (pctBloqueio >= LIMITE_BLOQUEIO_PCT && enviadosHoje >= 20) {
      console.warn(`[disparo] PARANDO — taxa de bloqueio ${pctBloqueio.toFixed(1)}% acima do limite ${LIMITE_BLOQUEIO_PCT}%`);
      break;
    }

    // 2. Verifica se o número existe no WhatsApp
    try {
      const existe = await numeroExiste(lead.telefone);
      if (!existe) {
        await updateLead(lead.id, { status: "perdido", motivo: "numero_invalido" });
        console.log(`[disparo] ${lead.telefone}: número não tem WhatsApp, pulando`);
        continue;
      }
    } catch (e) {
      console.warn(`[disparo] ${lead.telefone}: falha ao verificar número (continua mesmo assim)`, e.message);
    }

    // 3. Envia
    const v = variante();
    try {
      await enviarTexto(lead.telefone, v.texto);
      await insertMensagem({
        lead_id: lead.id,
        autor: "ia",
        texto: v.texto,
        modelo: "isca_template",
      });
      await updateLead(lead.id, {
        status: "disparado",
        variante_isca: v.letra,
        ultima_msg_em: new Date().toISOString(),
      });
      console.log(`[disparo] ${lead.telefone}: enviado (variante ${v.letra})`);
    } catch (e) {
      console.error(`[disparo] ${lead.telefone}: ERRO`, e.message);
      // Não atualiza status — pode ser retentado depois
    }

    // 4. Espera intervalo aleatório (anti-ban)
    const espera = aleatorio(MIN_MS, MAX_MS);
    await sleep(espera);
  }

  console.log("[disparo] finalizado");
}

export function disparoStatus() {
  return { em_curso: disparoEmCurso };
}
