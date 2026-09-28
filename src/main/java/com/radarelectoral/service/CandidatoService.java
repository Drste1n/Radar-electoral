package com.radarelectoral.service;

import com.radarelectoral.model.Candidato;
import com.radarelectoral.repository.CandidatoRepository;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class CandidatoService {

    private final CandidatoRepository repository;

    public CandidatoService(CandidatoRepository repository) {
        this.repository = repository;
    }

    public List<Candidato> obtenerTodos() {
        return repository.findAll();
    }

    public Optional<Candidato> obtenerPorId(String id) { // <-- Aquí está la clave: String
        return repository.findById(id);
    }
}