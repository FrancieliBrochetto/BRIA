// app.js — Lê JSONs estáticos do GitHub Pages (sem API Flask)

let dadosAtuais = null;
let temaAtivo   = "IA & Tech";
let dataAtiva   = null;

async function init() {
  configurarAbas();
  await Promise.all([
    carregarBriefingInicial(),
    carregarHistorico(),
  ]);
}

async function carregarBriefingInicial() {
  // Tenta o briefing de hoje; se não existir, pega o mais recente do índice
  const hoje = new Date().toISOString().split("T")[0];
  try {
    await carregarBriefing(hoje);
  } catch {
    try {
      const resp  = await fetch("briefings/index.json");
      const index = await resp.json();
      if (index.datas.length > 0) {
        await carregarBriefing(index.datas[0]);
      } else {
        mostrarErro("Nenhum briefing encontrado ainda.");
      }
    } catch {
      mostrarErro("Não foi possível carregar o briefing.");
    }
  }
}

async function carregarBriefing(data) {
  mostrarLoading();
  try {
    const resp = await fetch(`briefings/${data}.json`);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    dadosAtuais = await resp.json();
    dataAtiva   = data;
    atualizarHeader();
    atualizarBotoesHistorico();
    renderizarCards();
  } catch (err) {
    mostrarErro("Briefing não encontrado para esta data.");
    throw err;
  }
}

async function carregarHistorico() {
  try {
    const resp  = await fetch("briefings/index.json");
    const index = await resp.json();
    renderizarHistorico(index.datas);
  } catch {
    // silêncio — histórico é secundário
  }
}

function atualizarHeader() {
  if (!dadosAtuais?.data) return;
  const [ano, mes, dia] = dadosAtuais.data.split("-");
  const meses = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];
  document.getElementById("headerDate").textContent =
    `${dia} ${meses[parseInt(mes) - 1]}. ${ano}`;
}

function renderizarCards() {
  const cards = document.getElementById("cards");
  const vazio = document.getElementById("vazio");

  document.getElementById("loading").classList.add("hidden");
  document.getElementById("erro").classList.add("hidden");

  const noticias  = dadosAtuais?.noticias ?? [];
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

function renderizarHistorico(datas) {
  const container = document.getElementById("histbarDias");
  const meses     = ["jan","fev","mar","abr","mai","jun","jul","ago","set","out","nov","dez"];

  container.innerHTML = datas.map(data => {
    const [, mes, dia] = data.split("-");
    const label = `${dia}/${meses[parseInt(mes) - 1]}`;
    return `<button class="hist-btn" data-data="${data}"
      onclick="carregarBriefing('${data}')">
      ${label}
    </button>`;
  }).join("");
}

function atualizarBotoesHistorico() {
  document.querySelectorAll(".hist-btn").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.data === dataAtiva);
  });
}

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

function normalizar(str = "") {
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase().trim();
}

function escHTML(str = "") {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

init();