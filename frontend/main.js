const apiBase = "http://127.0.0.1:8000";

const form = document.getElementById("contestacao-form");
const resultado = document.getElementById("resultado");
const submitBtn = document.getElementById("submit-btn");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const payload = {
    tipo_acao: document.getElementById("tipo_acao").value,
    nome_parte_autora: document.getElementById("nome_parte_autora").value,
    nome_parte_re: document.getElementById("nome_parte_re").value,
    fatos: document.getElementById("fatos").value,
    pedidos_autor: document.getElementById("pedidos_autor").value,
  };

  resultado.textContent = "Gerando contestação...";
  submitBtn.disabled = true;

  try {
    const response = await fetch(`${apiBase}/gerar-contestacao`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!response.ok) {
      const erro = await response.json();
      throw new Error(erro.detail || "Erro ao gerar contestação");
    }

    const data = await response.json();
    resultado.textContent = data.contestacao;
  } catch (error) {
    resultado.textContent = `Falha: ${error.message}`;
  } finally {
    submitBtn.disabled = false;
  }
});
