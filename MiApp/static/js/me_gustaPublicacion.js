document.addEventListener('DOMContentLoaded', function () {
    const botonesMeGusta = document.querySelectorAll('.btn-me-gusta');

    botonesMeGusta.forEach((boton) => {
        boton.addEventListener('click', function () {
            const publicacionId = this.getAttribute('data-id');

            // Simulación de llamada al servidor para actualizar "Me gusta"
            fetch(`/me_gusta/${publicacionId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value || '',
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.estado === 'added') {
                        this.textContent = `❤️ ${data.total_me_gusta} Te gusta`;
                        lanzarCorazones(this);
                    } else {
                        this.textContent = `❤️ ${data.total_me_gusta} Me gusta`;
                    }
                })
                .catch((error) => console.error('Error:', error));
        });
    });

    function lanzarCorazones(boton) {
        const rect = boton.getBoundingClientRect(); // Obtener posición absoluta del botón
        const centroX = rect.left + rect.width / 2;
        const centroY = rect.top;

        for (let i = 0; i < 15; i++) { // Generar 15 corazones
            const corazon = document.createElement('div');
            corazon.className = 'corazon';
            corazon.style.left = `${centroX + (Math.random() * 50 - 25)}px`; // Dispersión horizontal
            corazon.style.top = `${centroY}px`; // Punto inicial en la posición del botón
            corazon.style.animationDelay = `${Math.random() * 0.5}s`; // Retraso aleatorio
            corazon.style.transform = `scale(${Math.random() * 0.6 + 0.7})`; // Tamaño aleatorio
            document.body.appendChild(corazon);

            // Eliminar corazón después de la animación
            setTimeout(() => {
                corazon.remove();
            }, 3000);
        }
    }
});