document.addEventListener('DOMContentLoaded', function() {
document.querySelector('form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío del formulario

    // Obtén los valores del formulario
    var correo = document.getElementById('exampleFormControlInput1').value;
    var mensaje = document.getElementById('exampleFormControlTextarea1').value;

    // Realiza la solicitud Ajax a Django
    $.ajax({
        url: enviarMensajeUrl,
        method: "POST",
        data: {
            correo: correo,
            mensaje: mensaje
        },
        success: function(response) {
            // Muestra la ventana de confirmación o realiza otras acciones después de recibir una respuesta exitosa
            alert('Mensaje enviado correctamente');

            // Restablece los valores del formulario si es necesario
            document.querySelector('form').reset();
        },
        error: function(error) {
            // Muestra un mensaje de error o realiza otras acciones en caso de error
            alert('Ocurrió un error al enviar el mensaje');
        }
    });
});
});

function redirectToLinkedin() {
    window.open('https://www.linkedin.com/in/brayan-giovani-rico-riveros-196994232/', '_blank');
  }