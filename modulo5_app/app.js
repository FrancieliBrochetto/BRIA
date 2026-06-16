// app.js — Lógica do frontend BRIA

// ── Configuração ─────────────────────────────────────
// Em desenvolvimento: API local. Ao subir pro Railway, troca a URL aqui.
const API = "http://127.0.0.1:5000";

// ── Estado da aplicação ──────────────────────────────
let dadosAtuais = null;   // { data, noticias[] }
let temaAtivo   = "IA & Tech";
let dataAtiva   = null;

// ── Inicialização ────────────────────────────────────
async function init() {
  configurarAbas();
  await Promise.all([
    carregarBriefing(),
    carregarHistorico(),
  ]);
}

// ── API calls ────────────────────────────────────────
async function carregarBriefing(data = null) {
  mostrarLoading();
  try {
    const endpoint = data
      ? `${API}/api/briefing/${data}`
      : `${API}/api/briefing/hoje`;

    const resp = await fetch(endpoint);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);

    dadosAtuais = await resp.json();
    dataAtiva   = dadosAtuais.data;

    atualizarHeader();
    atualizarBotoesHistorico();
    renderizarCards();
  } catch (err) {
    mostrarErro("Não foi possível conectar à API. Verifique se o servidor está rodando.");
    console.error("Erro ao carregar briefing:", err);
  }
}

async function carregarHistorico() {
  try {
    const resp = await fetch(`${API}/api/historico`);
    const dias  = await resp.json();
    renderizarHistorico(dias);
  } catch {
    // falha silenciosa — histórico é secundário
  }
}

// ── Renderização ─────────────────────────────────────
function atualizarHeader() {
  if (!dadosAtuais?.data) return;
  const [ano, mes, dia] = dadosAtuais.data.split("-");
  const meses = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];
  document.getElementById("headerDate").textContent =
    `${dia} ${meses[parseInt(mes) - 1]}. ${ano}`;
}

function renderizarCards() {
  const cards  = document.getElementById("cards");
  const vazio  = document.getElementById("vazio");

  // Esconde loading e erro
  document.getElementById("loading").classList.add("hidden");
  document.getElementById("erro").classList.add("hidden");

  const noticias = dadosAtuais?.noticias ?? [];

  // Filtra pelo tema da aba ativa (ignora acentuação)
  const filtradas = noticias.filter(n => normalizar(n.tema) === normalizar(temaAtivo));

  if (filtradas.length === 0) {
    cards.innerHTML = "";
    vazio.classList.remove("hidden");
    return;
  }

  vazio.classList.add("hidden");

  cards.innerHTML = filtradas.map(n => `
    <article class="card">
      <div class="card-meta">
        <span class="card-subtema">${escHTML(n.subtema || n.tema)}</span>
        <span class="card-fonte">${escHTML(n.fonte)}</span>
      </div>
      <h2 class="card-titulo">${escHTML(n.titulo)}</h2>
      <p class="card-resumo">${escHTML(n.resumo)}</p>
      <a class="card-link" href="${escHTML(n.url_original)}" target="_blank" rel="noopener noreferrer">
        Ver original →
      </a>
    </article>
  `).join("");
}

function renderizarHistorico(dias) {
  const container = document.getElementById("histbarDias");
  const meses     = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];

  container.innerHTML = dias.map(d => {
    const [, mes, dia] = d.data_coleta.split("-");
    const label = `${dia}/${meses[parseInt(mes) - 1]}`;
    return `<button class="hist-btn" data-data="${d.data_coleta}"
      title="${d.total_salvo} notícias salvas"
      onclick="carregarBriefing('${d.data_coleta}')">
      ${label}
    </button>`;
  }).join("");
}

function atualizarBotoesHistorico() {
  document.querySelectorAll(".hist-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.data === dataAtiva);
  });
}

// ── Abas ─────────────────────────────────────────────
function configurarAbas() {
  document.querySelectorAll(".tab").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
      btn.classList.add("active");
      temaAtivo = btn.dataset.tema;
      if (dadosAtuais) renderizarCards();
    });
  });
}

// ── Estados de UI ────────────────────────────────────
function mostrarLoading() {
  document.getElementById("loading").classList.remove("hidden");
  document.getElementById("erro").classList.add("hidden");
  document.getElementById("vazio").classList.add("hidden");
  document.getElementById("cards").innerHTML = "";
}

function mostrarErro(msg) {
  document.getElementById("loading").classList.add("hidden");
  document.getElementById("erroMsg").textContent = msg;
  document.getElementById("erro").classList.remove("hidden");
}

// ── Utilitários ───────────────────────────────────────
// Remove acentos antes de comparar temas (BRIA pode retornar "Legislação" ou "Legislacao")
function normalizar(str = "") {
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
}

// Escapa HTML para evitar injeção de conteúdo malicioso
function escHTML(str = "") {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ── Start ─────────────────────────────────────────────
init();