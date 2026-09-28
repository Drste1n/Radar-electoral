package com.radarelectoral.controller;

import com.radarelectoral.model.Candidato;
import com.radarelectoral.service.CandidatoService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/candidatos")
public class CandidatoRestController {

    private final CandidatoService service;

    public CandidatoRestController(CandidatoService service) {
        this.service = service;
    }

    // Devuelve todos los candidatos en JSON
    @GetMapping
    public List<Candidato> listarCandidatosJson() {
        return service.obtenerTodos();
    }

    // Devuelve un candidato específico en JSON
    @GetMapping("/{id}")
    public ResponseEntity<Candidato> obtenerCandidatoJson(@PathVariable String id) {
        return service.obtenerPorId(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }
}