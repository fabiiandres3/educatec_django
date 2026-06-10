const urls = document.getElementById('urls');

const crearUrl = urls.dataset.crearUrl;

fetch(crearUrl)
    .then(response => response.text())
    .then(html => {
        document.getElementById('contenido').innerHTML = html;
    })
    .catch(error => {
        console.error(error);
    });