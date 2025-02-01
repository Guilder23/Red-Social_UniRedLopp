// Función para filtrar publicaciones por el nombre de usuario dentro de <strong>
function buscarPublicacion() {
    const query = document.getElementById('buscador').value.toLowerCase();
    const publicaciones = document.querySelectorAll('.publicacion');
    const resultadosDiv = document.getElementById('resultadosBusqueda');

    let encontrado = false; // Para verificar si se encontró alguna coincidencia

    publicaciones.forEach(publicacion => {
        // Buscar el texto del usuario dentro de <strong>
        const username = publicacion.querySelector('strong').textContent.toLowerCase();

        if (username.includes(query)) {
            // Mostrar publicación si el nombre de usuario coincide con la búsqueda
            publicacion.style.display = 'block';
            encontrado = true;
        } else {
            // Ocultar publicación si el nombre de usuario no coincide
            publicacion.style.display = 'none';
        }
    });

    // Mostrar un mensaje si no se encontraron resultados
    if (!encontrado && query.trim() !== "") {
        resultadosDiv.innerHTML = "<p>No se encontraron publicaciones con ese nombre de usuario.</p>";
        resultadosDiv.style.display = 'block';
    } else {
        resultadosDiv.style.display = 'none'; // Ocultar el mensaje de 'sin resultados' si se encuentran publicaciones
    }
}



//BUSCADOR DE USUARIOS EN LA PAGINA DE USUARIOS
// Función para filtrar usuarios por el nombre de usuario
function buscarUsuarios() {
    // Obtener el valor de la búsqueda
    const query = document.getElementById('buscadorUsuarios').value.toLowerCase();
    
    // Obtener todas las listas de usuarios
    const usuarios = document.querySelectorAll('.user-item');
    
    // Recorrer cada usuario en la lista
    usuarios.forEach(usuario => {
      // Obtener el texto del nombre de usuario dentro del <span class="username">
      const username = usuario.querySelector('.username').textContent.toLowerCase();
      
      // Mostrar o ocultar el usuario según si el nombre contiene la búsqueda
      if (username.includes(query)) {
        usuario.style.display = 'block';  // Mostrar si coincide
      } else {
        usuario.style.display = 'none';   // Ocultar si no coincide
      }
    });
  }
  