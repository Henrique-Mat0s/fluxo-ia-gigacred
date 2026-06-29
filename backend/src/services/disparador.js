// Disparador multi-instância: rotação round-robin entre os chips ativos.

import {
  getLeadsParaDisparar, updateLead, insertMensagem,
  contarDisparosHoje, contarBloqueadosHoje,
} from "../db/supabase.js";
import { listarInstanciasAtivas } from "../db/instancias.js";
import { enviarTexto, numeroExiste } from "../evolution/client.js";

const VARIANTES = [
  "Oi! Tudo bem? Aqui é a Giovanna da GIGACRED. Você sabia que dá pra antecipar até 7 anos do seu saque-aniversário do FGTS e receber tudo no PIX?",
  "Olá! Sou a Giovanna, consultora da GIGACRED. Posso te mandar uma simulação rápida de quanto dá pra antecipar do seu FGTS?",
  "Oi, tudo bem? Giovanna aqui da GIGACRED. Tem alguns minutos pra eu te explicar como antecipar o FGTS sem complicação?",
  "Olá! Aqui é a GIGACRED. Você sabia que pode receber o seu FGTS agora, sem esperar o aniversário? Quer simular sem compromisso?",
  "Oi! Sou a Giovanna. Trabalho com antecipação de FGTS — em 1-2 dias úteis o dinheiro cai no seu PIX. Te interessa saber quanto dá?",
];

const LIMITE_DIA_GLOBAL = parseInt(process.env.DISPARO_LIMITE_DIA || "150", 10);
const MIN_MS     = parseInt(process.env.DISPARO_MIN_INTERVALO_MS || "40000", 10);
const MAX_MS     = parseInt(process.env.DISPARO_MAX_INTERVALO_MS || "90000", 10);
const LIMITE_BLOQUEIO_PCT = parseFloat(process.env.DISPARO_LIMITE_BLOQUEIO_PCT || "5");

let disparoEmCurso = false;

const sleep = (ms) => new Promise(r => setTimeout(r, ms));
const aleatorio = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const variante = () => {
  const idx = Math.floor(Math.random() * VARIANTES.length);
  return { letra: "ABCDE"[idx], texto: VARIANTES[idx] };
};

/**
 * Inicia disparo. Carrega instâncias ativas e distribui o lote entre elas
 * em round-robin, respeitando o limite individual de cada chip.
 */
export async function iniciarDisparo() {
  if (disparoEmCurso) {
    return { ok: false, erro: "Já existe um disparo em andamento." };
  }

  // 1. Carrega instâncias ativas e conectadas
  const todasInstancias = await listarInstanciasAtivas();
  const instancias = todasInstancias.filter(i => i.estado === "open");
  if (instancias.length === 0) {
    return {
      ok: false,
      erro: "Nenhuma instância ativa e conectada. Vá em /instancias e conecte ao menos um chip.",
      instancias_disponiveis: todasInstancias.length,
    };
  }

  // 2. Calcula capacidade restante por instância (limite individual ou global)
  const capacidades = instancias.map(i => {
    const limite = i.limite_dia || LIMITE_DIA_GLOBAL;
    const restante = Math.max(0, limite - (i.mensagens_hoje || 0));
    return { ...i, restante };
  });
  const capacidadeTotal = capacidades.reduce((s, c) => s + c.restante, 0);

  if (capacidadeTotal === 0) {
    return { ok: false, erro: "Todas as instâncias atingiram o limite diário." };
  }

  // 3. Pega leads da base, no máximo igual à capacidade total
  const leads = await getLeadsParaDisparar(capacidadeTotal);
  if (leads.length === 0) {
    return { ok: false, erro: "Nenhum lead com status='base' pra disparar." };
  }

  disparoEmCurso = true;
  loopDisparo(leads, capacidades).finally(() => { disparoEmCurso = false; });

  return {
    ok: true,
    iniciado: true,
    total_planejado: leads.length,
    capacidade_total: capacidadeTotal,
    instancias_usadas: capacidades.map(c => ({
      nome: c.nome,
      numero: c.numero,
      restante: c.restante,
    })),
    intervalo_estimado_min: Math.round(leads.length * (MIN_MS + MAX_MS) / 2 / 60000 / capacidades.length),
  };
}

async function loopDisparo(leads, capacidadesInicial) {
  // Cópia local pra decrementar conforme avança
  const capacidades = capacidadesInicial.map(c => ({ ...c }));
  let rrIndex = 0;

  console.log(`[disparo] iniciando: ${leads.length} leads x ${capacidades.length} instância(s)`);

  for (const lead of leads) {
    // Escolhe próxima instância (round-robin) que ainda tem capacidade
    let inst = null;
    for (let tentativa = 0; tentativa < capacidades.length; tentativa++) {
      const candidata = capacidades[rrIndex % capacidades.length];
      rrIndex++;
      if (candidata.restante > 0) {
        inst = candidata;
        break;
      }
    }
    if (!inst) {
      console.log("[disparo] todas as instâncias esgotaram capacidade — parando");
      break;
    }

    // Circuit breaker global (mantido como segurança extra)
    const bloqueadosHoje = await contarBloqueadosHoje();
    const enviadosHoje = await contarDisparosHoje();
    const pctBloqueio = enviadosHoje > 0 ? (bloqueadosHoje / enviadosHoje) * 100 : 0;
    if (pctBloqueio >= LIMITE_BLOQUEIO_PCT && enviadosHoje >= 20) {
      console.warn(`[disparo] PARANDO — taxa de bloqueio ${pctBloqueio.toFixed(1)}%`);
      break;
    }

    // Verifica se o número existe no WhatsApp (consulta via a instância escolhida)
    try {
      const existe = await numeroExiste(lead.telefone, inst.nome);
      if (!existe) {
        await updateLead(lead.id, { status: "perdido", motivo: "numero_invalido" });
        console.log(`[disparo] ${lead.telefone}: número não tem WhatsApp`);
        continue;
      }
    } catch (e) {
      console.warn(`[disparo] ${lead.telefone}: falha checar número`, e.message);
    }

    // Envia
    const v = variante();
    try {
      await enviarTexto(lead.telefone, v.texto, { instance: inst.nome });
      await insertMensagem({
        lead_id: lead.id,
        autor: "ia",
        texto: v.texto,
        modelo: "isca_template",
        instancia_id: inst.id,
      });
      await updateLead(lead.id, {
        status: "disparado",
        variante_isca: v.letra,
        ultima_msg_em: new Date().toISOString(),
      });
      inst.restante--;
      console.log(`[disparo] ${lead.telefone} via ${inst.nome} (variante ${v.letra}) — ${inst.restante} restantes nesse chip`);
    } catch (e) {
      console.error(`[disparo] ${lead.telefone} via ${inst.nome}: ERRO`, e.message);
    }

    // Anti-ban: pausa entre mensagens
    await sleep(aleatorio(MIN_MS, MAX_MS));
  }

  console.log("[disparo] finalizado");
}

export function disparoStatus() {
  return { em_curso: disparoEmCurso };
}
