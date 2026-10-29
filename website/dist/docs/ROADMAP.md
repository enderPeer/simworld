# SimWorld — Roadmap

A bottom-up emergent simulation. No hardcoded rules for anything above the
bottom layer: everything from chemistry to civilization must **emerge** from
the quantum seed. The checkmarks in each phase are the progress markers —
a phase is only done when the layer above it can actually emerge from it.

Guiding principles:

1. **Compute, don't table.** Elements are derived from electron physics, not
   looked up in a periodic table. Every combination of every substance must
   be calculable, not enumerated.
2. **Emergence over scripting.** No scripted events, no scripted tech tree.
   Tools, agriculture, nations, markets and memes must be consequences of
   agents interacting with a consistent physical world.
3. **One coherent timeline.** Big bang → now → future, one world-state, no
   resets, no seams. History is whatever actually happened in the sim.
4. **Perception-centric existence.** Anything outside every agent's field of
   view and memory is down-sampled to its nearest coupled neighbours. You
   exist where you are observed and remembered.
5. **Deterministic seed, irreducible randomness.** True quantum randomness
   (pre-observation) is allowed, but the world must be reproducible from its
   seed and observation log.

---

## Phase 0 — World Rules (the first principles)

Answer these before writing any code. They define what everything else is made of.

- [ ] Define **the quant**: the primitive unit of existence (discrete packet of
      field excitation). What is stored on it: energy, spin, charge, phase,
      position-as-probability, entanglement links.
- [ ] Define **the field substrate**: which fields exist at the start and how
      particles are excitations of them (don't hardcode particles, hardcode
      fields + symmetry breaking).
- [ ] Define **the Big Bang initial condition**: the seed. Minimal constants
      (c, ħ, field coupling strengths, expansion rate) from which all particle
      properties fall out.
- [ ] Define **observation**: what collapses a quantum state into a classical
      fact, and how unobserved regions stay cheap (superposition = compressed
      probability state, not simulated detail).
- [ ] Define **change**: time as discrete ticks at the quantum layer, with
      emergent continuous time at higher layers. Time ↔ velocity ↔ speed ↔
      power: power is travel, thermodynamics, geometry and emergent complexity.

## Phase 1 — Quantum Layer

- [ ] Particles as field excitations; superposition and probability clouds.
- [ ] True random events until observation; entanglement as a data structure
      (shared state, non-local correlation without signal).
- [ ] Observation/collapse mechanic hooked into the perception system (Phase 14).
- [ ] Seeded RNG + observation log for reproducibility.

## Phase 2 — Nuclear Layer

- [ ] Protons/neutrons, strong force, nuclear binding energy curve.
- [ ] Fusion (H→He and stellar nucleosynthesis → all elements emerge).
- [ ] Fission, radioactive decay chains, half-lives as emergent constants.
- [ ] Radiation: alpha/beta/gamma, penetration, ionization damage (feeds
      biology later: cancer, mutation, super-resilient bacteria).

## Phase 3 — Atomic Layer (elements must be calculated, not tabulated)

- [ ] Electron shells from first-principles quantum mechanics (solved
      approximations, not lookups): ionization energy, electronegativity,
      valence all derived.
- [ ] Periodic table as an **output**, verifiable against real values.
- [ ] Isotopes, plasma state, ionization.

## Phase 4 — Chemistry Layer

- [ ] Bonds (ionic, covalent, metallic) computed from electron configurations.
- [ ] Reaction engine: any combination of any substances is calculable —
      combustion, oxidation, acid/base, precipitation, polymers.
- [ ] Organic chemistry: carbon chains → plastics, fuels, pharmaceuticals.
- [ ] Compound registry is emergent cache, never an exhaustive list.

## Phase 5 — Materials & Substances

- [ ] Earth metals, clay, stone, salts.
- [ ] Oil, carbon forms, water (3 phases), air, gases.
- [ ] Magma, ice, vegetation matter.
- [ ] Derived material properties: hardness, ductility, melting point,
      conductivity — from composition, not per-material constants.

## Phase 6 — Physics Layer

- [ ] Mechanics: gravity, collision, momentum, fluids (water and air flow).
- [ ] Thermodynamics: heat transfer, phase transitions, engines, entropy.
- [ ] Light: spectrum, radiation, photosynthesis input, vision later.
- [ ] Sound: waves, propagation, hearing later.
- [ ] Electricity and magnetism: charge, current, electromagnetism, planetary
      magnetic field (from molten iron core convection).

## Phase 7 — Planet & Space

- [ ] Planet formation from accretion; layered interior: iron core, mantle,
      crust; plate tectonics, volcanism, mountain building.
- [ ] Surface systems: oceans, continents, islands, reefs, forests, swamps,
      deserts; water cycle, weather, climate, ice ages.
- [ ] Emission/absorption cycles: carbon, oxygen, nitrogen; fauna cleaning
      the air; waste breakdown; microplastic and dust transport later.
- [ ] Solar system, sun as fusion reactor, radiation environment.
- [ ] Milky Way, other star systems, time & space at scale (for spaceflight
      and observation), cosmic background as timeline anchor.

## Phase 8 — Life: Abiogenesis → Ecosystems

- [ ] Self-replicating chemistry from Phase 4 (no "create life" button).
- [ ] Bacteria, archaea; viruses as parasitic information packets.
- [ ] Antiviral and immune systems emerge (resistance arms races: super
      resilient bacteria, antiviral systems, antibiotics from moulds).
- [ ] Cells → plants, fungi, vegetation layers; bees and insects as working
      fauna (pollination, decomposition).
- [ ] Animals: body plans as constrained generative models, energy budgets.
- [ ] Ecosystems: food webs, nutrient cycles, population dynamics.
- [ ] Evolution with mutation + selection across **epochs**:
      [ ] first in the water
      [ ] onto land
      [ ] reptiles / dinosaurs
      [ ] mammals
      [ ] humans
- [ ] Pressure-driven adaptation: mutation, invasive species crossing into
      new biomes (into cities), species adapting to industry and radiation.

## Phase 9 — First Humans & Epochs of Civilization

- [ ] Fire and cooking (digestion/brain feedback loop).
- [ ] Stone age: knapping, tools, shelters.
- [ ] Bronze age: ore → smelting → alloy, driven by real chemistry.
- [ ] Farming, domestication, herding, settlements.
- [ ] Middle age: trades — bakers, shoemakers, woodcutters, table makers,
      bike producers analogues — professions as economic attractors.
- [ ] Modern times: industry, car industry, medical industry.
- [ ] Future: whatever emerges next, unplanned.

## Phase 10 — Technology Tree (emergent, research-driven)

- [ ] Research as agents experimenting with the real chemistry/physics world.
- [ ] Categorisation and culture of knowledge; science as a social practice.
- [ ] Mechanics → steam → electricity generation and distribution: energy
      plants, heating units, grids, city lights, timing, traffic.
- [ ] Transistors → computers → calculators → consoles → games → software.
- [ ] Radio: wave generation and observation → communication → radar →
      radiocommunication of everything.
- [ ] Transport chain: ships → trains → cars → flight → submarines → drones.
- [ ] Robotics + AI: simulated brains, brute-force capability, the ability to
      create artificial worlds inside the world (nested simulation).
- [ ] Biotech ladder: selective breeding → genetic optimisation of animals
      and plants → mushroom-derived drugs → antibiotics → gene editing
      (CRISPR analogue) → manipulation of life itself.
- [ ] Space program: observation of waves → rockets → satellites → ships.
- [ ] Internet, memes, platforms, apps, games made in-game by in-game people.

## Phase 11 — People & Society

- [ ] Agents with needs, roles, rights, morals, health, mental health
      (psychotic to healthy as a spectrum emerging from neurochemistry).
- [ ] Jobs and labour: cleaners, lawyers, doctors, barbers, office workers,
      musicians, athletes, artists — roles emerge from supply/demand.
- [ ] Education systems, learning curves, knowledge inheritance.
- [ ] Languages (emergent), nations, countries, cities, ethnicity, cultures,
      religions — including religious wars and meaning-making.
- [ ] Communities, values, laws, crime, conflict, martial arts, weapon arts,
      sports, olympic professions, party/scene creation.
- [ ] Warfare escalation: melee → armies → drone warfare → cyberwarfare.

## Phase 12 — Money, Power, Politics

- [ ] Barter → money → fiat → crypto; deflation, inflation, printing,
      manipulation, stealing.
- [ ] Banks, central power systems, regulation, taxes.
- [ ] Political systems as emergent regimes: fair and unfair governments,
      democracies, dictators, communism, capitalism, inequality dynamics.
- [ ] Propaganda and manipulation feedback loops (media, memes, religion).

## Phase 13 — Infrastructure, Industry, Externalities

- [ ] Roads, houses, districts, energy distributors, traffic with different
      driving conventions per region.
- [ ] Food production, transportation chains, emissions.
- [ ] Waste management and recycling loops (water recycling included).
- [ ] Damage vectors on bodies and land: pollution, bad air, industry metals,
      microplastics, gases, dust, space trash, radiation.
- [ ] Infrastructure-induced harm: accidents, collapse, occupational damage.

## Phase 14 — Perception, LOD & Existence (the render/sim contract)

- [ ] Reality is rendered only to what is observable and relevant.
- [ ] Field of view + shared perception as the center of existence.
- [ ] Detail connects only to what is close-related; everything else decays
      to a compressed state.
- [ ] Memory: agents sweep the band memory, store, and transmit information
      to each other (rumour, culture, news as data propagation).
- [ ] Per-agent perceived frame rate as a real stat: time as experienced
      processing; the sim gives every being a constant frame budget.

## Phase 15 — Hyperoptimized Runtime

- [ ] Data-oriented, cache-friendly ECS over the quantum→society layers.
- [ ] Tiered tick rates: quantum ticks only where observed; biology ticks
      slow; society ticks slower still; unobserved regions jump-state.
- [ ] CPU/GPU split: physics + chemistry on GPU, agent cognition on CPU,
      narrow bandwidth between them.
- [ ] Whole world reproducible from seed + observation log.
- [ ] Budget targets: how many atoms, agents, reactions per ms — measured,
      not guessed.

## Phase 16 — The Full Emergent Loop (definition of done)

- [ ] Seed the quantum layer → elements → planet → life → evolution →
      humans → fire → bronze → farms → cities → grids → radios → internet →
      AI building artificial worlds inside SimWorld — **with no step
      scripted**, only the Phase 0 world rules.
- [ ] A coherent playable timeline: explore, advance, and observe a living
      world that keeps running and inventing itself.

---

## Open questions (park first, resolve in Phase 0)

- What exactly is the quant? Discrete lattice or continuous field sampled on demand?
- How expensive is "true" electron-shell computation, and where do we cheat
  with provably equivalent shortcuts (cached eigenstates)?
- What is the observation criterion that collapses probability into fact —
  agent perception, or any interaction above a decoherence threshold?
- How much of history do we let emerge vs. seed as initial conditions
  (e.g. do we evolve life, or fast-forward it with an evolution run offline)?
