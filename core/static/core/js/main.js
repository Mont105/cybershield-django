document.addEventListener("DOMContentLoaded", () => {
  // 1. Resaltar enlace activo en la navegación
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll(".nav-link");

  navLinks.forEach((link) => {
    const href = link.getAttribute("href");
    const isActive = href === "/" ? currentPath === "/" : currentPath.startsWith(href);
    if (href && isActive) {
      link.classList.add("active");
    }
  });

  // 2. Filtro en vivo para servicios (catalog.html)
  const searchInput = document.getElementById("search-service");
  const serviceCards = document.querySelectorAll(".service-card");

  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      const term = e.target.value.toLowerCase().trim();

      serviceCards.forEach((card) => {
        const title = card.querySelector(".service-card-title")?.textContent.toLowerCase() || "";
        const desc = card.querySelector(".service-card-desc")?.textContent.toLowerCase() || "";
        const tag = card.querySelector(".service-card-tag")?.textContent.toLowerCase() || "";

        const matches = title.includes(term) || desc.includes(term) || tag.includes(term);
        card.style.display = matches ? "flex" : "none";
      });
    });
  }

  // 3. El formulario de contacto se valida en el servidor (contact/forms.py).
  //    Se limpia el error de un campo apenas el usuario lo modifica.
  document.querySelectorAll(".form-group.has-error").forEach((group) => {
    group.addEventListener("input", () => {
      group.classList.remove("has-error");
      group.querySelectorAll(".form-error").forEach((el) => el.remove());
    }, { once: true });
  });
});
