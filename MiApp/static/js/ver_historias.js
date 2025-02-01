document.addEventListener('DOMContentLoaded', () => {
    const carrusel = document.querySelector('.historias-carrusel');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const historias = document.querySelectorAll('.historia');
    const wrapper = document.querySelector('.historias-carrusel-wrapper');
    const totalHistorias = historias.length;
    const visibleWidth = wrapper.offsetWidth;

    let currentIndex = 0;

    function updateButtons() {
        prevBtn.classList.toggle('hidden', currentIndex === 0);
        nextBtn.classList.toggle('hidden', currentIndex >= totalHistorias - 1);
    }

    function scrollToIndex(index) {
        const offset = visibleWidth * index;
        carrusel.style.transform = `translateX(-${offset}px)`;
    }

    prevBtn.addEventListener('click', () => {
        if (currentIndex > 0) {
            currentIndex--;
            scrollToIndex(currentIndex);
        }
        updateButtons();
    });

    nextBtn.addEventListener('click', () => {
        if (currentIndex < totalHistorias - 1) {
            currentIndex++;
            scrollToIndex(currentIndex);
        }
        updateButtons();
    });

    // Inicializar botones
    updateButtons();
});

async function react(historiaId, tipoReaccion) {
    try {
        const response = await fetch(`/reaccionar/${historiaId}/${tipoReaccion}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
        });

        if (response.ok) {
            const data = await response.json();
            document.getElementById(`like-count-${historiaId}`).textContent = data.likes;
            document.getElementById(`dislike-count-${historiaId}`).textContent = data.dislikes;

            // Crear el efecto de los corazones
            createHeartsEffect();
        } else {
            console.error('Error al reaccionar');
        }
    } catch (error) {
        console.error('Error en la solicitud:', error);
    }
}

// Función para crear el efecto de los corazones
function createHeartsEffect() {
    const container = document.getElementById('hearts-container');
    const heartCount = 100; // Número de corazones que se generarán

    for (let i = 0; i < heartCount; i++) {
        const heart = document.createElement('div');
        heart.classList.add('heart');
        heart.innerHTML = '❤️💕💖'; // Corazón como contenido

        // Posición aleatoria en el contenedor
        const leftPosition = Math.random() * 100;
        const animationDelay = Math.random() * 1.9; // Retardo aleatorio para que no todos se muevan al mismo tiempo

        heart.style.left = `${leftPosition}%`;
        heart.style.animationDelay = `${animationDelay}s`;

        container.appendChild(heart);

        // Eliminar el corazón después de que termine la animación
        setTimeout(() => {
            heart.remove();
        }, 5500); // Tiempo de la animación
    }
}
