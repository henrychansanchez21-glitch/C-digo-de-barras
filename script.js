function onScanSuccess(decodedText, decodedResult) {
    // Se ejecuta cuando se detecta un código
    document.getElementById('result').innerText = `Código detectado: ${decodedText}`;
    
    // Opcional: Detener el escaneo tras el éxito
    html5QrcodeScanner.clear();
}

function onScanFailure(error) {
    // Errores de lectura (sucede continuamente mientras busca, mejor no mostrar nada)
}

// Configuración del escáner
let html5QrcodeScanner = new Html5QrcodeScanner(
    "reader", 
    { 
        fps: 10, // Cuadros por segundo
        qrbox: { width: 250, height: 150 }, // Área de escaneo
        rememberLastUsedCamera: true
    },
    /* verbose= */ false
);

html5QrcodeScanner.render(onScanSuccess, onScanFailure);
