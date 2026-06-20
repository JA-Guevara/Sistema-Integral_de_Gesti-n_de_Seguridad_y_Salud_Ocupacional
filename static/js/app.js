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
})();
