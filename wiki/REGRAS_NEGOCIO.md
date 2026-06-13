# 📋 REGRAS DE NEGÓCIO

## Índice Rápido

1. [Regras de Agendamento](#1-regras-de-agendamento)
2. [Regras de Cancelamento](#2-regras-de-cancelamento)
3. [Regras de Desconto](#3-regras-de-desconto)
4. [Regras de Disponibilidade](#4-regras-de-disponibilidade)
5. [Regras de Validação](#5-regras-de-validação)
6. [Regras de Cobrança](#6-regras-de-cobrança)
7. [Regras de Segurança](#7-regras-de-segurança)
8. [Regras por Especialidade](#8-regras-por-especialidade)

---

## 1. Regras de Agendamento

### 1.1 Elegibilidade Geral

| Regra | Descrição | Validação |
|-------|-----------|-----------|
| **Paciente Ativo** | Apenas pacientes com status "ativo" podem agendar | `paciente.status == 'ativo'` |
| **Serviço Ativo** | Apenas serviços marcados como "ativo" estão disponíveis | `servico.ativo == true` |
| **Não em Banimento** | Paciente não pode estar em banimento temporário | `paciente.banido_ate < now()` |
| **Dados Completos** | CPF e e-mail obrigatórios | `paciente.cpf NOT NULL AND paciente.email NOT NULL` |

### 1.2 Limites de Agendamento

```json
{
  "limites_simultaneos": {
    "agendamentos_por_dia": 2,
    "agendamentos_simultaneos": 1,
    "agendamentos_em_24h": 3
  },
  "validacoes": {
    "agendamentos_sem_confirmacao": {
      "maximo": 3,
      "desc": "Máximo 3 agendamentos pendentes por paciente"
    },
    "intervalo_minimo_entre_agendamentos": {
      "minutos": 0,
      "desc": "Paciente pode agendar agora e ir amanhã"
    }
  }
}
```

### 1.3 Antecedência Mínima/Máxima

```json
{
  "antecedencia_minima": {
    "minutos": 0,
    "desc": "Pode agendar para agora mesmo (com slots disponíveis)"
  },
  "antecedencia_maxima": {
    "dias": 90,
    "desc": "Não pode agendar com mais de 90 dias de antecedência"
  },
  "excecoes": {
    "pacientes_vip": {
      "dias": 180,
      "desc": "VIPs podem agendar com até 6 meses"
    },
    "saude_mental": {
      "dias": 30,
      "desc": "Psicologia/psiquiatria: limite reduzido para 30 dias"
    }
  }
}
```

### 1.4 Ocupação Máxima

```json
{
  "ocupacao_maxima_por_profissional": {
    "percentual": 85,
    "desc": "Nunca mais de 85% da agenda de um profissional"
  },
  "slots_obrigatorios_livres": {
    "quantidade_por_dia": 2,
    "desc": "Sempre manter 2 slots livres por dia para urgências"
  }
}
```

---

## 2. Regras de Cancelamento

### 2.1 Prazos de Antecedência

```json
{
  "cancelamento": {
    "sem_taxa": {
      "minimo_horas_antecedencia": 24,
      "desc": "Cancelamento com 24h+ de antecedência é sem taxa",
      "reembolso": "100%"
    },
    "com_taxa_50": {
      "minimo_horas_antecedencia": 12,
      "descricao": "Cancelamento com 12-24h de antecedência",
      "reembolso": "50%"
    },
    "nao_permitido": {
      "minimo_horas_antecedencia": 0,
      "descricao": "Cancelamento com menos de 12h",
      "reembolso": "0% (perda total)",
      "observacao": "Paciente pode ser compensado em crédito"
    }
  },
  "excecoes": {
    "saude_mental": {
      "desc": "Saúde mental NUNCA cobra taxa",
      "motivo": "Questões de privacidade e bem-estar"
    },
    "primeira_consulta": {
      "desc": "Primeira consulta sempre sem taxa",
      "motivo": "Incentivo ao agendamento"
    }
  }
}
```

### 2.2 Impacto no Perfil

```json
{
  "penalidades": {
    "cancelo_sem_taxa": {
      "limite_mensal": 2,
      "acima_disso": "Cobra taxa no próximo"
    },
    "no_show": {
      "desc": "Não comparecimento sem aviso prévio",
      "penalidade": "Banimento por 7 dias",
      "apos_3_no_shows": "Banimento permanente"
    }
  }
}
```

---

## 3. Regras de Desconto

### 3.1 Promoções Automáticas

```json
{
  "promocoes": {
    "primeira_visita": {
      "id": "promo-001",
      "nome": "Primeira Visita",
      "condicoes": {
        "total_agendamentos_realizados": 0,
        "especialidades": ["estética", "salão", "beleza"],
        "excluir": ["psicologia", "psiquiatria"]
      },
      "desconto_percentual": 15,
      "desconto_fixo": null,
      "validade_dias": 30,
      "usos_por_paciente": 1,
      "requer_agendamento_imediato": true,
      "valid_from": "2026-01-01",
      "valid_to": "2026-12-31"
    },
    "lealdade_3_servicos": {
      "id": "promo-002",
      "nome": "Lealdade (3+ Serviços)",
      "condicoes": {
        "total_agendamentos_realizados": { "gte": 3 },
        "dias_desde_ultimo": { "gte": 30 }
      },
      "desconto_percentual": 10,
      "usos_por_paciente": null,
      "requer_agendamento_imediato": false
    },
    "horario_baixa_demanda": {
      "id": "promo-003",
      "nome": "Happy Hour - Horário de Baixa Demanda",
      "condicoes": {
        "hora_inicio": { "gte": "10:00", "lte": "12:00" },
        "dia_semana": ["terça", "quarta"],
        "ocupacao_agenda_profissional": { "lte": 30 }
      },
      "desconto_percentual": 5,
      "validade_minutos": 10,
      "desc": "Válido apenas no momento da oferta"
    },
    "combo_servicos": {
      "id": "promo-004",
      "nome": "Desconto Combo (2+ serviços)",
      "condicoes": {
        "total_servicos_no_mesmo_dia": { "gte": 2 }
      },
      "desconto_percentual": 20,
      "aplicar_ao": "segundo_servico",
      "desc": "20% off no segundo serviço quando agendar 2+ no mesmo dia"
    }
  }
}
```

### 3.2 Políticas de Desconto

```json
{
  "politicas": {
    "desconto_maximo_acumulado": {
      "percentual": 30,
      "desc": "Nunca mais de 30% de desconto na mesma transação"
    },
    "limite_descontos_mes": {
      "quantidade": 5,
      "desc": "Máximo 5 descontos por mês por paciente"
    },
    "desconto_nunca_leva_negativo": {
      "desc": "Preço final nunca é negativo/zero",
      "valor_minimo": 1.00
    },
    "autorizacao_manual": {
      "desc": "Descontos > 25% requerem aprovação manual",
      "requer": "admin ou gerente"
    }
  }
}
```

### 3.3 Desconto por Profissional

```json
{
  "desconto_por_profissional": {
    "limite": 15,
    "desc": "Cada profissional pode oferecer até 15% adicional"
  }
}
```

---

## 4. Regras de Disponibilidade

### 4.1 Horário de Funcionamento

```json
{
  "horario_funcionamento": {
    "segunda_a_sexta": {
      "abertura": "09:00",
      "fechamento": "19:00"
    },
    "sabado": {
      "abertura": "09:00",
      "fechamento": "14:00"
    },
    "domingo": "fechado",
    "feriados": {
      "politica": "fechado",
      "excecoes": [
        "Operação de emergência em saúde mental"
      ]
    }
  }
}
```

### 4.2 Bloqueios de Agenda

```json
{
  "bloqueios": {
    "limpeza_agenda": {
      "segunda": "07:00-09:00",
      "desc": "Espaço para limpeza da clínica"
    },
    "intervalo_almoco": {
      "horario": "12:00-13:00",
      "desc": "Intervalo obrigatório para profissional"
    },
    "treinamento": {
      "quarta": "14:00-16:00",
      "desc": "Bloqueio periódico para capacitação"
    }
  }
}
```

### 4.3 Duração Mínima de Slot

```json
{
  "duracao_slot": {
    "minimo_minutos": 15,
    "desc": "Slot mínimo é 15 minutos",
    "padrao_minutos": 60,
    "desc_padrao": "Maioria dos serviços: 1 hora"
  }
}
```

---

## 5. Regras de Validação

### 5.1 Dados Obrigatórios

```json
{
  "dados_obrigatorios": {
    "no_agendamento": {
      "cpf": {
        "obrigatorio": true,
        "validacao": "formato CPF válido",
        "criptografia": true
      },
      "email": {
        "obrigatorio": true,
        "validacao": "email válido (regex)",
        "privacidade": "confidencial"
      },
      "telefone": {
        "obrigatorio": true,
        "validacao": "formato brasileiro"
      }
    },
    "dados_complementares": {
      "alergias": {
        "obrigatorio": false,
        "relevancia": "alta para saude_mental"
      },
      "medicamentos": {
        "obrigatorio": false,
        "relevancia": "alta para saude_mental"
      },
      "historico_saude": {
        "obrigatorio": false,
        "relevancia": "alta para saude_mental"
      }
    }
  }
}
```

### 5.2 Validações por Especialidade

```json
{
  "validacoes_especializadas": {
    "saude_mental": {
      "primeira_consulta_requer_questoes": [
        "Você está em crise agora?",
        "Tem pensamentos suicidas?",
        "Está sob tratamento psicológico?"
      ],
      "encaminhamento_protocolo": {
        "se_critico": "Interromper e escalacionar para emergência"
      }
    },
    "estética": {
      "validacoes": [
        "Tipo de pele",
        "Alergias a produtos",
        "Procedimentos anteriores"
      ]
    }
  }
}
```

---

## 6. Regras de Cobrança

### 6.1 Valores e Reembolsos

```json
{
  "pagamento": {
    "tipos_aceitos": [
      "pix",
      "cartao_credito",
      "cartao_debito",
      "boleto"
    ],
    "prazo_reembolso": {
      "dias_uteis": 2,
      "desc": "Reembolso processado em até 2 dias úteis"
    },
    "taxa_processamento": {
      "pix": 0,
      "cartao": "3.5%",
      "boleto": "2%"
    }
  }
}
```

### 6.2 Sinal vs. Integral

```json
{
  "sinal": {
    "percentual": 50,
    "desc": "Sinal de 50% do valor total",
    "liberacao_slot": true,
    "desc_liberacao": "Slot é bloqueado apenas com sinal"
  },
  "pagamento_integral": {
    "quando": "No dia do procedimento",
    "opcoes": [
      "Pagar integral na recepção",
      "Pagar no débito automático"
    ]
  }
}
```

---

## 7. Regras de Segurança

### 7.1 Proteção de Dados

```json
{
  "privacidade": {
    "saude_mental": {
      "nivel": "MÁXIMO",
      "criptografia": "AES-256",
      "acesso_restrito_a": ["paciente", "seu_terapeuta", "admin_legítimo"],
      "log_acesso": true,
      "notificar_paciente_on_access": "opcional"
    },
    "dados_pessoais": {
      "cpf_criptografado": true,
      "email_criptografado": false,
      "historico_agendamentos": "visível apenas ao paciente"
    }
  }
}
```

### 7.2 Rate Limiting

```json
{
  "rate_limits": {
    "por_paciente": {
      "requisicoes_por_minuto": 10,
      "agendamentos_por_hora": 2,
      "cancelamentos_por_dia": 5
    },
    "por_ip": {
      "requisicoes_por_minuto": 60,
      "desc": "Prevenir DDoS"
    }
  }
}
```

### 7.3 Detecção de Anomalias

```json
{
  "deteccao_fraude": {
    "multiplos_agendamentos_rapido": {
      "desc": "3+ agendamentos em 5 minutos = suspeita",
      "acao": "Bloquear por 1 hora"
    },
    "mudancas_rapidas_dados": {
      "desc": "Email/CPF alterados múltiplas vezes em 1 dia",
      "acao": "Requerer verificação adicional"
    },
    "ip_suspeita": {
      "desc": "Múltiplos pacientes do mesmo IP",
      "acao": "Monitor + possível bloqueio"
    }
  }
}
```

---

## 8. Regras por Especialidade

### 8.1 Saúde Mental (Psicologia/Psiquiatria)

```json
{
  "saude_mental": {
    "protocolos_especiais": {
      "avaliacao_risco": {
        "freq": "toda_primeira_consulta",
        "items": [
          "Ideação suicida?",
          "Auto-agressão?",
          "Uso de substâncias?"
        ]
      }
    },
    "desconto_especial": {
      "nunca_cobra_cancelamento": true,
      "motivo": "Privacidade e bem-estar do paciente"
    },
    "privacidade_maxima": {
      "sem_historico_visivel": "Histórico não aparece em dashboards públicos",
      "sem_notificacoes_intrusivas": "Nunca enviar lembrete se paciente não desejar"
    },
    "encaminhamento": {
      "se_internacao_necessaria": "Protocolo automático",
      "se_medicacao": "Coordenação com psiquiatra"
    }
  }
}
```

### 8.2 Estética

```json
{
  "estetica": {
    "protocolos_especiais": {
      "validacao_antes": {
        "tipo_pele": true,
        "alergias_conhecidas": true,
        "procedimentos_recentes": true
      }
    },
    "promocoes_agressivas": {
      "primeira_visita": 15,
      "combo_servicos": 20,
      "recomendacao": true
    },
    "cross_selling": {
      "frequencia_recomendacao": "alta",
      "exemplo": "Após hidratação → Peeling"
    }
  }
}
```

### 8.3 Salão de Beleza

```json
{
  "salao_beleza": {
    "especialidades": [
      "cabelo",
      "unhas",
      "barba",
      "sobrancelha"
    ],
    "desconto_frequente": {
      "pacote_6_visitas": 30,
      "desc": "30% off ao comprar pacote de 6"
    }
  }
}
```

---

## 9. Regras de Priorização

### 9.1 Fila de Espera (Waitlist)

```json
{
  "waitlist": {
    "prioridade_ordem": "FIFO",
    "validez_dias": 30,
    "auto_remove": "após 30 dias sem ação",
    "notificacao": {
      "automatica": true,
      "tentativas": 3,
      "intervalo_horas": 2
    }
  }
}
```

### 9.2 Agendamentos VIP

```json
{
  "vip": {
    "critério_automatico": {
      "total_gasto": 1000,
      "desc": "Pacientes que gastaram R$ 1k+ viram VIP"
    },
    "beneficios": {
      "antecedencia_maxima_dias": 180,
      "desconto_permanente": 10,
      "prioridade_waitlist": true,
      "atendimento_priority": true
    }
  }
}
```

---

## 10. Tabela de Referência Rápida

| Aspecto | Padrão | Exceção |
|---------|--------|---------|
| **Cancelamento sem taxa** | 24h antes | 0h (saúde mental) |
| **Desconto primeira visita** | 15% | Não aplica (saúde mental) |
| **Antecedência máxima** | 90 dias | 180 dias (VIP) |
| **Limite agendamentos/dia** | 2 | 3 (VIP) |
| **Ocupação máxima agenda** | 85% | N/A |
| **Sinal obrigatório** | 50% | Pode ser 0% (VIP) |
| **Taxa no card** | 3.5% | 0% (PIX) |

---

## 11. Configuração de Ambiente

### 11.1 Arquivo .env (Exemplo)

```env
# Regras globais
MAX_DISCOUNT_PERCENTAGE=30
MAX_ADVANCE_DAYS=90
MIN_CANCELLATION_HOURS=24

# Saúde mental
SAUDE_MENTAL_SPECIAL_HANDLING=true
SAUDE_MENTAL_CRISIS_HOTLINE=188

# Segurança
ENCRYPTION_KEY=your-key-here
LOG_SENSITIVE_DATA=false
RATE_LIMIT_REQUESTS_PER_MIN=10

# Pagamento
PAYMENT_GATEWAY=stripe
PAYMENT_MIN_AMOUNT=1.00
REFUND_DAYS=2
```

---

**Próximo**: Consulte [COMPONENTES.md](./COMPONENTES.md) para estrutura de dados e APIs.
