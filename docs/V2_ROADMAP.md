# V2.0 Development Roadmap

## Overview
V2.0 will transform this from a proof-of-concept into a production-ready
system suitable for distribution.

## Technical Milestones

### Phase 1: Local LLM (Weeks 1-2)
- [ ] Install Ollama on Raspberry Pi
- [ ] Test Llama 2 7B performance
- [ ] Benchmark vs OpenAI latency
- [ ] Implement grandmother personality prompt
- [ ] Facial animation or lip syncing with single image input
- [ ] Verify response quality

**Success Criteria**: <4s LLM latency, equivalent response quality

### Phase 2: Optimization (Week 3)
- [ ] Voice synthesization module for mimicing voice using a ~10 second sample
- [ ] Increase rate of fidelity without comprimising on performance
- [ ] Finetune and train model for adaptive learning and "natural" conversation
- [ ] Performance test
- [ ] PCB design for small form factor design (If feasible hardware supports)

**Success Criteria**: at least a 25% improvement in latency and fidelity from phase 1 and natural responses through voice emulation

### Phase 3: Housing (Weeks 4-5)
- [ ] CAD Design housing solution
- [ ] CFD analysis for thermal solutions
- [ ] Single source power supply solution
- [ ] Assemble for long term thermal and power consumption analysis
    - [ ] Full performance metrics analysis as well 

**Success Criteria**: Single assembled unit as a complete device runs at least 4 hours without a decrease in performance

### Phase 5: Blank Slate (Weeks 6)
- [ ] Complete documentation on V2.0 with a demo
- [ ] Modify framework to act as a blank slate to accept user customization options
- [ ] Integrate web-based procedure to upload configuration and customization options
- [ ] Full system deployment test and metrics analysis
- [ ] Push final updated version and tag V2.0 

**Success Criteria**: Similar performance metrics with custom configuration options