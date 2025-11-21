function mostrarCampos() {
  const tipo = document.querySelector('input[name="tipo_entrega"]:checked').value;
  const datosDomicilio = document.getElementById("datos-domicilio");

  if (tipo === "domicilio") {
    datosDomicilio.style.display = "block";
    document.getElementById("direccion").setAttribute("required", true);
    document.getElementById("telefono_envio").setAttribute("required", true);
  } else {
    datosDomicilio.style.display = "none";
    document.getElementById("direccion").value = "";
    document.getElementById("telefono_envio").value = "";
    document.getElementById("direccion").removeAttribute("required");
    document.getElementById("telefono_envio").removeAttribute("required");
  }
}


const totalEl = document.getElementById("total");
const acompDiv = document.getElementById("acompaniamientos");
const tituloAcomp = document.getElementById("titulo-acomp");
const form = document.querySelector("form");


//  Ocultar bloque de acompañamientos

const carritoTDs = document.querySelectorAll("tbody tr td:first-child");
const hayPlatos = carritoTDs.length > 0;

if (!hayPlatos) {
  acompDiv.style.display = "none";
} else {
  acompDiv.style.display = "block";
  tituloAcomp.textContent = "🍽️ Selecciona 2 acompañamientos obligatorios";
}


// Cada porción con 2 acompañamientos

document.addEventListener("DOMContentLoaded", function () {

  const bloques = document.querySelectorAll('.bloque-acomp[data-requiere="1"]');

  bloques.forEach(bloque => {

    const checks = bloque.querySelectorAll(".acomp-check");

    checks.forEach(check => {

      check.addEventListener("change", () => {

        const seleccionados = bloque.querySelectorAll(".acomp-check:checked").length;

        if (seleccionados >= 2) {
          checks.forEach(c => {
            if (!c.checked) {
              c.disabled = true;
              c.parentElement.style.opacity = "0.4";
              c.parentElement.style.textDecoration = "line-through";
            }
          });
        } else {
          checks.forEach(c => {
            c.disabled = false;
            c.parentElement.style.opacity = "1";
            c.parentElement.style.textDecoration = "none";
          });
        }

      });

    });

  });

});


//  Validar antes de enviar

form.addEventListener("submit", function (e) {
  e.preventDefault();

  const bloques = document.querySelectorAll('.bloque-acomp[data-requiere="1"]');

  for (let bloque of bloques) {
    const seleccionados = bloque.querySelectorAll(".acomp-check:checked").length;

    if (seleccionados !== 2) {

      const modal = new bootstrap.Modal(document.getElementById('modalAcompError'));
      modal.show();

      return; 
    }
  }

  Swal.fire({
    title: "¿Confirmar pedido?",
    html: `Tu pedido será enviado.<br>${totalEl ? totalEl.innerText : ""}`,
    icon: "question",
    showCancelButton: true,
    confirmButtonText: "✅ Finalizar",
    cancelButtonText: "❌ Cancelar",
    background: "#2f2f2f",
    color: "#fff",
    confirmButtonColor: "#ffd700",
    cancelButtonColor: "#ff4444"
  }).then(result => {
    if (result.isConfirmed) form.submit();
  });
});