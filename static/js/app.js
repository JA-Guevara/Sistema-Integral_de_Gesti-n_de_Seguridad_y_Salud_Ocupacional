(function () {
  const body = document.body;

  window.addEventListener("load", function () {
    body.classList.add("is-loaded");
  });

  const storedSidebar = localStorage.getItem("syso-sidebar-collapsed");
  if (storedSidebar === "true") {
    body.classList.add("sidebar-collapsed");
  }

  document.querySelectorAll("[data-sidebar-toggle]").forEach(function (button) {
    button.addEventListener("click", function () {
      body.classList.toggle("sidebar-collapsed");
      localStorage.setItem(
        "syso-sidebar-collapsed",
        body.classList.contains("sidebar-collapsed")
      );
    });
  });

  document.querySelectorAll("[data-auto-dismiss]").forEach(function (alert) {
    window.setTimeout(function () {
      if (!window.bootstrap || !alert.isConnected) return;
      const instance = window.bootstrap.Alert.getOrCreateInstance(alert);
      instance.close();
    }, 5200);
  });

  document.querySelectorAll(".mobile-sidebar .sidebar-link:not(.disabled)").forEach(function (link) {
    link.addEventListener("click", function () {
      const panel = document.getElementById("mobileSidebar");
      if (!panel || !window.bootstrap) return;
      const instance = window.bootstrap.Offcanvas.getInstance(panel);
      if (instance) instance.hide();
    });
  });

  // --- Animación "count-up" de las tarjetas KPI (.stat-value) ---
  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  document.querySelectorAll(".stat-value").forEach(function (el) {
    const target = parseInt((el.textContent || "").replace(/\D/g, ""), 10);
    if (isNaN(target) || target <= 0 || prefersReduced) return;
    const duration = 700;
    let startTs = null;
    function tick(ts) {
      if (!startTs) startTs = ts;
      const progress = Math.min((ts - startTs) / duration, 1);
      el.textContent = Math.floor(progress * target).toLocaleString("es-BO");
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });

  // --- Buscador de tablas: <input data-table-filter="#idTabla"> ---
  document.querySelectorAll("[data-table-filter]").forEach(function (input) {
    const table = document.querySelector(input.getAttribute("data-table-filter"));
    if (!table) return;
    const emptyRow = table.querySelector("[data-filter-empty]");
    input.addEventListener("input", function () {
      const q = input.value.trim().toLowerCase();
      let visibles = 0;
      table.querySelectorAll("tbody tr[data-row]").forEach(function (row) {
        const match = row.textContent.toLowerCase().indexOf(q) !== -1;
        row.classList.toggle("filtro-oculto", !match);
        if (match) visibles += 1;
      });
      if (emptyRow) emptyRow.classList.toggle("is-visible", visibles === 0);
    });
  });
})();
