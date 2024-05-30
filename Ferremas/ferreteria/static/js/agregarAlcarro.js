document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('button[data-url]').forEach(button => {
        button.addEventListener('click', function () {
            const url = this.getAttribute('data-url');
            console.log("URL para redirección:", url);  // Esto debería mostrar la URL correcta en la consola
            window.location.href = url;
        });
    });
});
