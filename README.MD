## 11wo4
```
core/
├── CMakeLists.txt                    # Main build configuration
├── include/
│   └── 11wo4/
│       ├── types.hpp                 # Core types and constants
│       ├── game_state.hpp            # Game state management
│       ├── observation.hpp           # Observation space definition
│       ├── action.hpp                # Action space definition
│       ├── environment.hpp           # Main interface for agents
│       ├── pattern_tables.hpp        # Pattern lookups/validation
│       ├── move_validator.hpp        # Move validation logic
│       ├── scoring.hpp               # Scoring system
│       └── utils.hpp                 # Utility functions
│
├── src/
│   ├── types.cpp
│   ├── game_state.cpp
│   ├── observation.cpp
│   ├── action.cpp
│   ├── environment.cpp
│   ├── pattern_tables.cpp
│   ├── move_validator.cpp
│   ├── scoring.cpp
│   └── utils.cpp
│
├── bindings/
│   ├── CMakeLists.txt
│   └── python/
│       ├── bindings.cpp              # Main bindings file
│       ├── observation_bindings.cpp  # Observation space bindings 
│       ├── action_bindings.cpp       # Action space bindings
│       └── environment_bindings.cpp  # Environment bindings
│
├── python/                           # Python package
│   ├── setup.py
│   └── 11wo4/
│       ├── __init__.py
│       ├── environment.py            # High-level environment wrapper
│       ├── visualization/
│       │   ├── __init__.py
│       │   ├── renderer.py           # State visualization
│       │   └── replay.py             # Game replay system
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── metrics.py            # Performance metrics
│       │   └── patterns.py           # Pattern analysis
│       └── agents/
│           ├── __init__.py
│           ├── base.py               # Base agent class
│           ├── random_agent.py       # Random baseline
│           └── rule_based.py         # Rule-based baseline
│
└── tests/
    ├── cpp/
    │   ├── CMakeLists.txt
    │   ├── test_game_state.cpp
    │   ├── test_observation.cpp
    │   ├── test_action.cpp
    │   ├── test_pattern_tables.cpp
    │   └── test_scoring.cpp
    └── python/
        ├── test_environment.py
        ├── test_visualization.py
        └── test_agents.py
```