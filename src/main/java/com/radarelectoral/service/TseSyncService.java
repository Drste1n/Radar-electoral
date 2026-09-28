package com.radarelectoral.service;

import org.springframework.stereotype.Service;

@Service
public class TseSyncService {

    public void sincronizarPresidentes() {
        // Dejamos este método vacío intencionalmente.
        // La sincronización ahora se realiza a través de nuestro Data Lake en Python (alimentador_bd.py)
        // para poder saltarnos el firewall del TSE y procesar los archivos ZIP locales.
        System.out.println("Sincronización delegada al motor de datos de Python.");
    }
}