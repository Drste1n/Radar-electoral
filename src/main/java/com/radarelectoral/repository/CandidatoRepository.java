package com.radarelectoral.repository;

import com.radarelectoral.model.Candidato;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CandidatoRepository extends JpaRepository<Candidato, String> {
    // Aquí puedes agregar métodos personalizados después si los necesitas
}