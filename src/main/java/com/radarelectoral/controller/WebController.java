package com.radarelectoral.controller;

import com.radarelectoral.model.Candidato;
import com.radarelectoral.service.CandidatoService;
import com.radarelectoral.service.TseSyncService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

import java.util.Optional;
import java.util.stream.Collectors;

@Controller
public class WebController {

    private final CandidatoService service;
    private final TseSyncService tseSyncService;

    public WebController(CandidatoService service, TseSyncService tseSyncService) {
        this.service = service;
        this.tseSyncService = tseSyncService;
    }

    // Muestra la página principal con la lista de candidatos
    @GetMapping("/")
    public String mostrarInicio(Model model) {
        // Filtramos para que en el index solo aparezcan los candidatos a Presidente 
        // (evitamos que los vices salgan mezclados como tarjetas principales)
        var presidentes = service.obtenerTodos().stream()
                .filter(c -> "PRESIDENTE".equalsIgnoreCase(c.getCargo()))
                .collect(Collectors.toList());
        
        model.addAttribute("candidatos", presidentes);
        return "index";
    }

    @GetMapping("/sincronizar-tse")
    public String sincronizarTse() {
        tseSyncService.sincronizarPresidentes();
        return "redirect:/";
    }

    // Perfil Principal del Candidato
    @GetMapping("/candidatos/{id}")
    public String mostrarDetalle(@PathVariable String id, Model model) {
        Optional<Candidato> candidato = service.obtenerPorId(id);
        if (candidato.isPresent()) {
            model.addAttribute("candidato", candidato.get());
            return "detalle";
        }
        return "redirect:/";
    }

    // --- NUEVAS RUTAS PARA EL DRILL-DOWN (SUB-PÁGINAS) ---

    // Ruta para la página de desglose de Patrimonio
    @GetMapping("/candidatos/{id}/patrimonio")
    public String mostrarPatrimonio(@PathVariable String id, Model model) {
        return service.obtenerPorId(id).map(candidato -> {
            model.addAttribute("candidato", candidato);
            return "patrimonio"; 
        }).orElse("redirect:/");
    }

    // Ruta para la página de Transparencia Financiera
    @GetMapping("/candidatos/{id}/financas")
    public String verFinanzas(@PathVariable String id, Model model) {
        return service.obtenerPorId(id).map(candidato -> {
            model.addAttribute("candidato", candidato);
            return "financas"; 
        }).orElse("redirect:/");
    }

    // Ruta para la página de Situación Legal
    @GetMapping("/candidatos/{id}/situacao")
    public String mostrarSituacao(@PathVariable String id, Model model) {
        return service.obtenerPorId(id).map(candidato -> {
            model.addAttribute("candidato", candidato);
            return "situacao"; 
        }).orElse("redirect:/");
    }

    // Ruta para la página del Vicepresidente
    @GetMapping("/candidatos/{id}/vice")
    public String mostrarVice(@PathVariable String id, Model model) {
        Optional<Candidato> presidenteOpt = service.obtenerPorId(id);
        
        if (presidenteOpt.isPresent()) {
            Candidato presidente = presidenteOpt.get();
            // Mantenemos el objeto "candidato" (presidente) para el botón de "Voltar" y el título
            model.addAttribute("candidato", presidente); 
            
            // Si el presidente tiene enlazado un Vice, buscamos su registro real
            if (presidente.getSqCandidatoVice() != null && !presidente.getSqCandidatoVice().isEmpty()) {
                Optional<Candidato> viceOpt = service.obtenerPorId(presidente.getSqCandidatoVice());
                // Pasamos el objeto "vice" completo a la vista para extraer su patrimonio y certidumbres
                viceOpt.ifPresent(vice -> model.addAttribute("vice", vice)); 
            }
            
            return "vice"; 
        }
        return "redirect:/";
    }
}