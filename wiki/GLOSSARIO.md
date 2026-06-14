# 📖 GLOSSÁRIO

## Termos de Negócio

### Agendamento
Reserva de horário na agenda de um profissional para realização de um serviço. Pode estar nos estados: pendente, confirmado, realizado ou cancelado.

### Sinal (Pré-pagamento)
Pagamento parcial (geralmente 50%) realizado no momento da confirmação do agendamento, garantindo a reserva do horário.

### Waitlist / Fila de Espera
Lista de pacientes interessados em um horário indisponível. Quando alguém cancela, o primeiro da fila é notificado automaticamente.

### Cross-Selling
Prática de oferecer serviços complementares ou adicionais ao confirmar um agendamento (ex: Limpeza + Hidratação).

### Combo de Serviços
Promoção onde o paciente agenda múltiplos serviços no mesmo dia e recebe desconto no segundo ou posteriores.

### No-Show
Quando o paciente falta ao agendamento sem cancelar previamente. Penalidades podem incluir taxa ou banimento.

### Deflexão Suave
Tentativa empática do agente de resolver o problema do paciente antes de transferir para um atendente humano.

### Handoff / Transferência
Passagem do atendimento de um agente autônomo para um atendente humano.

### VIP (Very Important Person)
Classificação de pacientes de alto valor (geralmente com alto gasto total) que recebem benefícios especiais.

### Periodicidade Técnica
Intervalo recomendado entre procedimentos de um mesmo tipo (ex: limpeza de pele a cada 30 dias).

---

## Termos Técnicos

### LLM (Large Language Model)
Modelo de linguagem de grande escala usado para gerar respostas conversacionais. Neste projeto, o único modelo suportado é o Google Composer 2.5.

### RAG (Retrieval Augmented Generation)
Técnica que combina busca em base de dados com geração de respostas, mitigando alucinações do LLM.

### Tool Calling / Function Calling
Capacidade de um LLM invocar funções estruturadas (APIs) para executar ações específicas.

### Prompt Engineering
Arte de estruturar instruções para um LLM de forma a obter respostas melhores e mais previsíveis.

### System Prompt
Instrução inicial injetada no LLM que define seu comportamento, persona e restrições.

### Injeção de Contexto
Prática de adicionar dados dinâmicos ao system prompt (histórico do paciente, dados de agendamento, etc).

### Lock Temporário
Bloqueio no banco de dados que reserva um slot de agenda por um tempo limitado (5 minutos padrão).

### Double-Booking
Problema de agendar o mesmo horário para dois pacientes diferentes. Evitado com locks e controle transacional.

### Transação ACID
Propriedades de banco de dados: Atomicidade, Consistência, Isolamento, Durabilidade. Essencial para agendamentos.

### Webhook
URL que recebe notificações automáticas de eventos externos (ex: confirmação de pagamento).

### Event Emitter / Publisher-Subscriber
Padrão onde mudanças de estado geram eventos que múltiplos serviços podem "escutar" e reagir.

### Rate Limiting
Técnica de limitar requisições por IP/usuário para prevenir abuso e DDoS.

### Rate Limiting
Técnica de limitar requisições por IP/usuário para prevenir abuso e DDoS.

### Middleware
Camada intermediária que processa requisições antes de chegar ao endpoint final.

### REST API / RESTful
Padrão de arquitetura para APIs baseado em HTTP com métodos GET, POST, PUT, DELETE.

### Criptografia de Dados em Repouso
Dados sensíveis (CPF, dados de saúde) são criptografados quando armazenados no banco de dados.

### Criptografia em Trânsito
Dados são criptografados quando transmitidos pela internet (HTTPS/TLS).

### UUID (Universally Unique Identifier)
Identificador único de 36 caracteres usado para IDs de registros no banco de dados.

### ISO 8601
Padrão internacional para representação de datas e horas (ex: 2026-06-16T14:00:00Z).

### CQRS (Command Query Responsibility Segregation)
Padrão de separar operações de escrita (commands) de leitura (queries) para melhor performance.

### Idempotência
Propriedade onde executar a mesma operação múltiplas vezes tem o mesmo resultado que executá-la uma vez.

---

## Termos de Domínio (Saúde)

### Anamnese
Histórico de saúde coletado durante primeira consulta (alergias, medicamentos, condições pré-existentes).

### Contraindicação
Situação ou condição que torna um procedimento inapropriado ou perigoso para um paciente.

### Periódico
Relativo a um período; procedimentos periódicos devem ser repetidos em intervalos regulares.

### Crise / Situação de Crise
Estado agudo de angústia ou emergência médica que requer intervenção imediata.

### Ideação Suicida
Pensamentos ou desejos de cometer suicídio. Indicador crítico de risco.

### Automutilação
Ato de se ferir intencionalmente como mecanismo de coping. Indicador crítico de risco.

### Protocolo de Emergência
Procedimentos estruturados para lidar com situações críticas (ex: alertar equipe, fornecer contatos de ajuda).

### Triage (Triagem)
Processo de avaliar e classificar a urgência de uma situação (do mais ao menos urgente).

### Anestesia
Medicação que remove a sensação de dor durante procedimentos.

---

## Abreviações

| Abreviação | Significado |
|------------|------------|
| API | Application Programming Interface |
| ACID | Atomicity, Consistency, Isolation, Durability |
| BD / DB | Banco de Dados |
| CEO | Chief Executive Officer |
| CPF | Cadastro de Pessoa Física |
| CRM | Customer Relationship Management |
| CVSS | Common Vulnerability Scoring System |
| CVV | Centro de Valorização da Vida (Brasil) |
| DTO | Data Transfer Object |
| HTTP | HyperText Transfer Protocol |
| HTTPS | HTTP Secure |
| ID | Identifier |
| IP | Internet Protocol |
| JSON | JavaScript Object Notation |
| JWT | JSON Web Token |
| LLM | Large Language Model |
| NPS | Net Promoter Score |
| OAuth | Open Authorization |
| RBAC | Role-Based Access Control |
| RAG | Retrieval Augmented Generation |
| REST | Representational State Transfer |
| SAMU | Serviço de Atendimento Móvel de Urgência |
| SMS | Short Message Service |
| SQL | Structured Query Language |
| TLS | Transport Layer Security |
| TTL | Time To Live |
| UUID | Universally Unique Identifier |
| VIP | Very Important Person |

---

## Termos de Interface de Usuário

### CTA (Call to Action)
Elemento que convida o usuário a tomar uma ação específica (ex: "Agendar agora", "Confirmar").

### UI / UX
User Interface (interface visual) e User Experience (experiência do usuário).

### Dashboard
Painel visual que mostra informações resumidas e métricas importantes.

### Modal / Dialog
Janela popup que aparece sobre o conteúdo principal da página.

### Placeholder
Texto de exemplo em um campo de entrada.

### Toast / Notificação
Mensagem breve que aparece e desaparece automaticamente.

### Responsive Design
Design que se adapta a diferentes tamanhos de tela (mobile, tablet, desktop).

---

## Termos de Segurança

### Autenticação
Processo de verificar a identidade de um usuário (login com senha, biometria, etc).

### Autorização
Processo de verificar se um usuário autenticado tem permissão para executar uma ação.

### Brute Force
Ataque que tenta múltiplas combinações de senha até encontrar a correta.

### Criptografia
Processo de converter dados legíveis em código ilegível para protegê-los.

### DDoS (Distributed Denial of Service)
Ataque que sobrecarrega um servidor com múltiplas requisições simultâneas.

### Firewall
Sistema que controla tráfego de rede permitindo ou bloqueando conexões.

### Hashing
Função que converte uma entrada em uma saída de tamanho fixo não-reversível (ex: SHA-256).

### Phishing
Tentativa enganosa de obter dados sensíveis fingindo ser uma entidade confiável.

### SQL Injection
Ataque que injeta comandos SQL maliciosos em formulários de entrada.

### Token
Chave temporária que autoriza acesso a recursos protegidos.

### XSS (Cross-Site Scripting)
Ataque que injeta código malicioso em páginas web.

---

## Termos de Projeto

### Backlog
Lista de funcionalidades e melhorias planejadas para desenvolvimento futuro.

### Sprint
Período curto (2-4 semanas) onde o time trabalha em tarefas específicas.

### MVP (Minimum Viable Product)
Versão mínima do produto com features essenciais para validar a ideia.

### Stakeholder
Pessoa interessada no projeto (cliente, usuário, gerente, etc).

### Roadmap
Plano de alto nível mostrando direção do projeto e marcos principais.

### Bug / Defeito
Comportamento indesejado ou erro no software.

### Feature / Funcionalidade
Nova capacidade ou melhoria adicionada ao produto.

### Hotfix
Correção urgente de bug crítico lançada fora do ciclo normal.

---

## Referências Rápidas por Contexto

### Se você é um **Paciente**:
- Agendamento, Serviço, Protocolo, Lembrete, Cancelamento, Desconto

### Se você é um **Recepcionista/Atendente**:
- Handoff, Dossiê, Dashboard, Paciente Ativo, No-Show, Fila de Espera

### Se você é um **Desenvolvedor Backend**:
- API, Transação ACID, Lock Temporário, Event Emitter, Webhook, Rate Limiting

### Se você é um **Desenvolvedor Frontend**:
- UI/UX, Responsive Design, Modal, CTA, Toast, Placeholder

### Se você é um **Gestor/Stakeholder**:
- VIP, Cross-Selling, NPS, Ticket Médio, Periodicidade, Roadmap

### Se você é um **Especialista em IA**:
- LLM, RAG, Tool Calling, Prompt Engineering, System Prompt, Injeção de Contexto

### Se você é um **Especialista em Segurança**:
- Autenticação, Autorização, Criptografia, Hashing, Rate Limiting, Auditoria

---

## Tabela de Símbolos Usados na Documentação

| Símbolo | Significado |
|---------|------------|
| 🎯 | Objetivo |
| 📝 | Requisito Funcional |
| 🔄 | Sequência / Fluxo |
| ✅ | Validação / Sucesso |
| ❌ | Erro / Falha |
| ⚠️ | Atenção / Aviso |
| 🔴 | Crítico |
| 🟠 | Alto |
| 🟡 | Médio |
| 🟢 | Baixo |
| 💾 | Banco de Dados |
| 🔐 | Segurança |
| 📞 | Contato / Comunicação |
| 📱 | Mobile / Aplicativo |
| 💰 | Financeiro / Pagamento |
| 👤 | Usuário / Paciente |
| 👨‍⚕️ | Profissional / Médico |
| 🚨 | Emergência / Alerta |
| 📊 | Dados / Métrica |
| 🔗 | Link / Referência |
| 📄 | Documento |

---

## Dúvidas Frequentes

### O que é a diferença entre "Sinal" e "Pagamento Integral"?
- **Sinal**: Pagamento parcial (50%) que bloqueia o slot de agenda
- **Pagamento Integral**: Pagamento do valor total, geralmente feito no dia do atendimento

### Por que "Saúde Mental" tem regras diferentes?
Por razões de privacidade, bem-estar do paciente e protocolo ético. Pacientes de saúde mental:
- Nunca pagam taxa de cancelamento
- Têm máxima privacidade nos dados
- Passam por triagem de risco diferente
- Recebem tratamento mais empático

### O que fazer se o paciente estiver em crise?
1. Ativar protocolo de emergência imediatamente
2. Fornecer contatos: CVV (188), SAMU (192), Pronto-socorro
3. Notificar a equipe clínica
4. Não deixar o paciente sozinho na conversa

### Como funciona a detecção automática de crise?
O sistema analisa:
- Palavras-chave (suicídio, automutilação, etc)
- Sentimento da mensagem (score 0-1)
- Contexto (especialidade, histórico)
- Resultado: score de risco (0-1)

Se score > threshold (ex: 0.8), ativar protocolo.

### Por que existe Lock Temporário?
Evitar que dois pacientes reservem o mesmo horário simultâneamente. O lock dura 5 minutos:
- Paciente vê horário
- Lock criado
- Paciente pensa e confirma (< 5 min)
- Agendamento confirmado
- Lock removido

Se passar de 5 min, slot fica livre novamente.

---

**Fim do Glossário**. Para dúvidas adicionais, consulte os arquivos específicos:
- [ARQUITETURA.md](./ARQUITETURA.md) - Estrutura técnica
- [FLUXOS_PRINCIPAIS.md](./FLUXOS_PRINCIPAIS.md) - Detalhes dos fluxos
- [REGRAS_NEGOCIO.md](./REGRAS_NEGOCIO.md) - Regras parametrizadas
- [COMPONENTES.md](./COMPONENTES.md) - APIs e modelos de dados
