package com.radarelectoral;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class RadarElectoralApplication {
    public static void main(String[] args) {
        SpringApplication.run(RadarElectoralApplication.class, args);
    }
}