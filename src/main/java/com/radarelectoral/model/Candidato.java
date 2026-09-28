package com.radarelectoral.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "candidatos")
public class Candidato {

    @Id
    @Column(name = "sq_candidato")
    private String sqCandidato;

    @Column(name = "nome")
    private String nombre;

    @Column(name = "nome_urna")
    private String nombreUrna;

    @Column(name = "numero")
    private Integer numero;

    @Column(name = "cargo")
    private String cargo;

    @Column(name = "situacao")
    private String situacionLegal;

    @Column(name = "profesion")
    private String profesion;

    @Column(name = "patrimonio")
    private String patrimonio;

    @Column(name = "vicepresidente")
    private String vicepresidente;

    @Column(name = "sq_candidato_vice")
    private String sqCandidatoVice;

    // NUEVOS CAMPOS JURÍDICOS
    @Column(name = "numero_processo")
    private String numeroProcesso;

    @Column(name = "motivo_situacao", columnDefinition = "TEXT")
    private String motivoSituacao;

    @Column(name = "foto_url")
    private String fotoUrl;

    @Column(name = "pdf_plan_gobierno_url", columnDefinition = "TEXT")
    private String pdfPlanGobiernoUrl;

    @Column(name = "resumen_propuestas", columnDefinition = "TEXT")
    private String resumenPropuestas;

    @Column(name = "propuestas_detalles", columnDefinition = "TEXT")
    private String propuestasDetalles;

    @Column(name = "partido_sigla")
    private String partidoSigla;

    @Column(name = "bienes_detalles", columnDefinition = "TEXT")
    private String bienesDetalles;

    @Column(name = "redes_sociales", columnDefinition = "TEXT")
    private String redesSociales;

    @Column(name = "grau_instrucao")
    private String grauInstrucao;

    @Column(name = "estado_civil")
    private String estadoCivil;

    @Column(name = "ocupacao")
    private String ocupacao;

    @Column(name = "cor_raca")
    private String corRaca;

    @Column(name = "despesa_maxima")
    private Double despesaMaxima;

    @Column(name = "top_despesas", columnDefinition = "TEXT")
    private String topDespesas;

    @Column(name = "top_doadores", columnDefinition = "TEXT")
    private String topDoadores;

    @Column(name = "top_fornecedores", columnDefinition = "TEXT")
    private String topFornecedores;

    @Column(name = "total_receitas")
    private Double totalReceitas;

    @Column(name = "total_despesas")
    private Double totalDespesas;

    @Column(name = "pdf_certidoes_url", columnDefinition = "TEXT")
    private String pdfCertidoesUrl;

    @Column(name = "atualizado_em")
    private java.time.LocalDateTime atualizadoEm;

    public Candidato() {}

    // ==========================================
    // GETTERS Y SETTERS
    // ==========================================

    public String getSqCandidato() { return sqCandidato; }
    public void setSqCandidato(String sqCandidato) { this.sqCandidato = sqCandidato; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public String getNombreUrna() { return nombreUrna; }
    public void setNombreUrna(String nombreUrna) { this.nombreUrna = nombreUrna; }

    public Integer getNumero() { return numero; }
    public void setNumero(Integer numero) { this.numero = numero; }

    public String getCargo() { return cargo; }
    public void setCargo(String cargo) { this.cargo = cargo; }

    public String getSituacionLegal() { return situacionLegal; }
    public void setSituacionLegal(String situacionLegal) { this.situacionLegal = situacionLegal; }

    public String getProfesion() { return profesion; }
    public void setProfesion(String profesion) { this.profesion = profesion; }

    public String getPatrimonio() { return patrimonio; }
    public void setPatrimonio(String patrimonio) { this.patrimonio = patrimonio; }

    public String getVicepresidente() { return vicepresidente; }
    public void setVicepresidente(String vicepresidente) { this.vicepresidente = vicepresidente; }

    public String getSqCandidatoVice() { return sqCandidatoVice; }
    public void setSqCandidatoVice(String sqCandidatoVice) { this.sqCandidatoVice = sqCandidatoVice; }

    // GETTERS Y SETTERS DE LOS NUEVOS CAMPOS JURÍDICOS
    public String getNumeroProcesso() { return numeroProcesso; }
    public void setNumeroProcesso(String numeroProcesso) { this.numeroProcesso = numeroProcesso; }

    public String getMotivoSituacao() { return motivoSituacao; }
    public void setMotivoSituacao(String motivoSituacao) { this.motivoSituacao = motivoSituacao; }

    public String getFotoUrl() { return fotoUrl; }
    public void setFotoUrl(String fotoUrl) { this.fotoUrl = fotoUrl; }

    public String getPdfPlanGobiernoUrl() { return pdfPlanGobiernoUrl; }
    public void setPdfPlanGobiernoUrl(String pdfPlanGobiernoUrl) { this.pdfPlanGobiernoUrl = pdfPlanGobiernoUrl; }

    public String getResumenPropuestas() { return resumenPropuestas; }
    public void setResumenPropuestas(String resumenPropuestas) { this.resumenPropuestas = resumenPropuestas; }

    public String getPropuestasDetalles() { return propuestasDetalles; }
    public void setPropuestasDetalles(String propuestasDetalles) { this.propuestasDetalles = propuestasDetalles; }

    public String getPartidoSigla() { return partidoSigla; }
    public void setPartidoSigla(String partidoSigla) { this.partidoSigla = partidoSigla; }

    public String getBienesDetalles() { return bienesDetalles; }
    public void setBienesDetalles(String bienesDetalles) { this.bienesDetalles = bienesDetalles; }

    public String getRedesSociales() { return redesSociales; }
    public void setRedesSociales(String redesSociales) { this.redesSociales = redesSociales; }

    public String getGrauInstrucao() { return grauInstrucao; }
    public void setGrauInstrucao(String grauInstrucao) { this.grauInstrucao = grauInstrucao; }

    public String getEstadoCivil() { return estadoCivil; }
    public void setEstadoCivil(String estadoCivil) { this.estadoCivil = estadoCivil; }

    public String getOcupacao() { return ocupacao; }
    public void setOcupacao(String ocupacao) { this.ocupacao = ocupacao; }

    public String getCorRaca() { return corRaca; }
    public void setCorRaca(String corRaca) { this.corRaca = corRaca; }

    public Double getDespesaMaxima() { return despesaMaxima; }
    public void setDespesaMaxima(Double despesaMaxima) { this.despesaMaxima = despesaMaxima; }

    public String getTopDespesas() { return topDespesas; }
    public void setTopDespesas(String topDespesas) { this.topDespesas = topDespesas; }

    public String getTopDoadores() { return topDoadores; }
    public void setTopDoadores(String topDoadores) { this.topDoadores = topDoadores; }

    public String getTopFornecedores() { return topFornecedores; }
    public void setTopFornecedores(String topFornecedores) { this.topFornecedores = topFornecedores; }

    public Double getTotalReceitas() { return totalReceitas; }
    public void setTotalReceitas(Double totalReceitas) { this.totalReceitas = totalReceitas; }

    public Double getTotalDespesas() { return totalDespesas; }
    public void setTotalDespesas(Double totalDespesas) { this.totalDespesas = totalDespesas; }

    public String getPdfCertidoesUrl() { return pdfCertidoesUrl; }
    public void setPdfCertidoesUrl(String pdfCertidoesUrl) { this.pdfCertidoesUrl = pdfCertidoesUrl; }

    public java.time.LocalDateTime getAtualizadoEm() { return atualizadoEm; }
    public void setAtualizadoEm(java.time.LocalDateTime atualizadoEm) { this.atualizadoEm = atualizadoEm; }
}