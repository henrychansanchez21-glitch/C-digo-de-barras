function onScanSuccess(decodedText) {
    // 1. Pausar el escáner
    html5QrcodeScanner.pause(true);

    // 2. Obtener el inventario actual
    let inventario = JSON.parse(localStorage.getItem("inventario_web") || "[]");

    // 3. Buscar si el código ya está registrado
    let productoExistente = inventario.find(p => p.id === decodedText);

    if (productoExistente) {
        // SI EXISTE: Mostrar información y no pedir registro
        alert("Producto ya registrado:\n\nNombre: " + productoExistente.nombre + "\nCódigo: " + decodedText);
    } else {
        // NO EXISTE: Pedir nombre para registrarlo
        let nombre = prompt("NUEVO PRODUCTO DETECTADO\nCódigo: " + decodedText + "\n\nIngrese el nombre:");

        if (nombre) {
            inventario.push({
                id: decodedText,
                nombre: nombre,
                fecha: new Date().toLocaleString()
            });
            localStorage.setItem("inventario_web", JSON.stringify(inventario));
            alert("¡Guardado con éxito!");
            actualizarInterfaz();
        }
    }

    // 4. Reanudar el escáner después de 2 segundos
    setTimeout(() => { 
        html5QrcodeScanner.resume(); 
    }, 2000);
}
