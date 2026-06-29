// Lê um CSV (nome;telefone;origem) e insere na tabela leads com status='base'.
// Uso: node scripts/importar-base.js caminho/pra/base.csv

import "dotenv/config";
import fs from "node:fs";
import { findLeadByTelefone, createLead } from "../src/db/supabase.js";

const csvPath = process.argv[2];
if (!csvPath) {
  console.error("Uso: node scripts/importar-base.js caminho/pra/base.csv");
  process.exit(1);
}

const linhas = fs.readFileSync(csvPath, "utf8").split(/\r?\n/).filter(Boolean);
const header = linhas[0].toLowerCase().split(/[;,]/).map(s => s.trim());

const idxNome  = header.indexOf("nome");
const idxFone  = header.indexOf("telefone");
const idxOrigem = header.indexOf("origem");

if (idxFone === -1) {
  console.error('CSV deve ter coluna "telefone". Header detectado:', header);
  process.exit(1);
}

let inseridos = 0, jaExistia = 0, invalidos = 0;

for (const linha of linhas.slice(1)) {
  const cols = linha.split(/[;,]/).map(c => c.trim());
  const telefoneRaw = cols[idxFone] || "";
  const telefone = telefoneRaw.replace(/\D/g, "");

  if (telefone.length < 10) { invalidos++; continue; }

  // Garante formato E.164 BR (5511...)
  const fone = telefone.startsWith("55") ? telefone : `55${telefone}`;

  const existe = await findLeadByTelefone(fone);
  if (existe) {
    jaExistia++;
    continue;
  }

  await createLead({
    nome: idxNome >= 0 ? (cols[idxNome] || null) : null,
    telefone: fone,
    origem: idxOrigem >= 0 ? (cols[idxOrigem] || "csv_import") : "csv_import",
    status: "base",
  });
  inseridos++;
  if (inseridos % 50 === 0) console.log(`... ${inseridos} importados`);
}

console.log(`\n=== Importação concluída ===`);
console.log(`Inseridos:    ${inseridos}`);
console.log(`Já existiam:  ${jaExistia}`);
console.log(`Inválidos:    ${invalidos}`);
console.log(`Total CSV:    ${linhas.length - 1}`);
console.log(`\nPróximo passo: POST /api/disparo/iniciar pra começar`);
