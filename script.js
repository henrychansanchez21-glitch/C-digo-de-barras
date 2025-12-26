function onScanSuccess(decodedText) {
    // 1. Limpiar el código (quitar espacios invisibles que arruinan la comparación)
    const codigoLimpio = decodedText.trim();
    
    // 2. Pausar el escáner inmediatamente
    html5QrcodeScanner.pause(true);

    // 3. Obtener inventario y verificar si existe
    let inventario = JSON.parse(localStorage.getItem("inventario_web") || "[]");
    
    // Buscamos si ya existe el código
    let productoExistente = inventario.find(p => p.id.trim() === codigoLimpio);

    if (productoExistente) {
        // SI YA EXISTE: Mostramos datos y SALIMOS de la función con 'return'
        alert("📋 PRODUCTO ENCONTRADO\n" +
              "------------------------------\n" +
              "Nombre: " + productoExistente.nombre + "\n" +
              "Código: " + productoExistente.id + "\n" +
              "Registrado el: " + productoExistente.fecha);
        
        // Reanudamos y cortamos la ejecución aquí
        setTimeout(() => { html5QrcodeScanner.resume(); }, 2000);
        return; 
    }

    // 4. SI NO EXISTE: Entonces sí pedimos el nombre
    let nombre = prompt("NUEVO CÓDIGO: " + codigoLimpio + "\nEl producto no existe. Ingrese nombre para registrar:");

    if (nombre && nombre.trim() !== "") {
        inventario.push({
            id: codigoLimpio,
            nombre: nombre.trim(),
            fecha: new Date().toLocaleString()
        });
        localStorage.setItem("inventario_web", JSON.stringify(inventario));
        actualizarInterfaz();
        alert("✅ Guardado exitosamente");
    } else {
        alert("❌ Registro cancelado");
    }

    // 5. Reanudar el escáner
    setTimeout(() => { html5QrcodeScanner.resume(); }, 1500);
}
