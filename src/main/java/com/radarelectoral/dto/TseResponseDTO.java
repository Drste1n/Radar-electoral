package com.radarelectoral.dto;

import java.util.List;

public class TseResponseDTO {
    private List<TseCandidatoDTO> candidatos;

    public List<TseCandidatoDTO> getCandidatos() { return candidatos; }
    public void setCandidatos(List<TseCandidatoDTO> candidatos) { this.candidatos = candidatos; }
}