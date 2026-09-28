package com.radarelectoral.dto;

public class TseCandidatoDTO {
    private Long id;
    private String nomeUrna;
    private TsePartidoDTO partido;
    private String propuestas;
    
    // NUEVOS CAMPOS DTO
    private String resumenPropuestas;
    private String pdfPlanGobiernoUrl;
    
    private String fotoUrl;
    
    private String numeroUrna;
    private String profesion;
    private String patrimonio;
    private String situacionLegal;
    private String vicepresidente;

    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getNomeUrna() { return nomeUrna; }
    public void setNomeUrna(String nomeUrna) { this.nomeUrna = nomeUrna; }
    public TsePartidoDTO getPartido() { return partido; }
    public void setPartido(TsePartidoDTO partido) { this.partido = partido; }
    public String getPropuestas() { return propuestas; }
    public void setPropuestas(String propuestas) { this.propuestas = propuestas; }
    
    // Getters y Setters de los nuevos campos
    public String getResumenPropuestas() { return resumenPropuestas; }
    public void setResumenPropuestas(String resumenPropuestas) { this.resumenPropuestas = resumenPropuestas; }
    public String getPdfPlanGobiernoUrl() { return pdfPlanGobiernoUrl; }
    public void setPdfPlanGobiernoUrl(String pdfPlanGobiernoUrl) { this.pdfPlanGobiernoUrl = pdfPlanGobiernoUrl; }

    public String getFotoUrl() { return fotoUrl; }
    public void setFotoUrl(String fotoUrl) { this.fotoUrl = fotoUrl; }

    public String getNumeroUrna() { return numeroUrna; }
    public void setNumeroUrna(String numeroUrna) { this.numeroUrna = numeroUrna; }
    public String getProfesion() { return profesion; }
    public void setProfesion(String profesion) { this.profesion = profesion; }
    public String getPatrimonio() { return patrimonio; }
    public void setPatrimonio(String patrimonio) { this.patrimonio = patrimonio; }
    public String getSituacionLegal() { return situacionLegal; }
    public void setSituacionLegal(String situacionLegal) { this.situacionLegal = situacionLegal; }
    public String getVicepresidente() { return vicepresidente; }
    public void setVicepresidente(String vicepresidente) { this.vicepresidente = vicepresidente; }
}