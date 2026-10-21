# Reliable Offers Tasks

## Sequence

### T1 — Establish test baseline

**Depends on:** none  
**Where:** `tests/`, `requirements.txt`  
**Done when:** parser, matcher and database tests run in a clean venv.

### T2 — Unify configuration and runner

**Depends on:** T1  
**Where:** `run_*.py`, `src/config.py`  
**Done when:** one production entrypoint owns capture, commands and notification;
phase scripts are removed or clearly marked as historical.

### T3 — Implement robust parsing

**Depends on:** T1  
**Where:** `src/extractor.py`, `tests/test_extractor.py`  
**Done when:** à vista wins over installments and `R$ 200,00 x 10` yields 2000.

### T4 — Implement matching and store registry

**Depends on:** T1  
**Where:** `src/matcher.py`, store modules, `src/database.py`  
**Done when:** aliases/exclusions are normalized, all matches are returned, URL
domains identify stores, and global blocks are configurable.

### T5 — Migrate offer persistence

**Depends on:** T2, T4  
**Where:** `src/database.py`, migration code, integration tests  
**Done when:** existing database data is preserved and origin/delivery state is
persisted without URL collisions across products.

### T6 — Add eligibility and deduplication

**Depends on:** T3, T4, T5  
**Where:** pipeline/domain module, tests  
**Done when:** target price, blocked store and 30-minute product+URL+price window
are evaluated deterministically.

### T7 — Harden notification and commands

**Depends on:** T2, T5, T6  
**Where:** `src/notifier.py`, bot commands, tests  
**Done when:** owner authorization, HTTP status handling, source metadata and
explicit delivery failures work.

### T8 — Publish installation

**Depends on:** T7  
**Where:** `README.md`, `.env.example`, requirements, CI/Git metadata  
**Done when:** a clean Linux/macOS/Windows setup is documented and secrets,
sessions and local databases are excluded.

## Verification gates

- Unit tests for every parsing and matching acceptance criterion.
- Migration test against a copy of the current SQLite schema/data.
- Manual Telegram UAT with private group, 2FA, blocked store and repeated URL.
- Compile and clean-install checks.

