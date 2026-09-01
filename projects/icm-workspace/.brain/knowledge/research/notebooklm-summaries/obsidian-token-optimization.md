# Obsidian Token Optimization

## Source

- NotebookLM notebook: AI Routing, Agent Skills, and Context Engineering Strategies
- Question: Based only on the notebook sources, what are the best practices for using an Obsidian-style markdown knowledge vault to reduce token usage and improve context routing for coding agents? Keep it concrete.

## Distilled answer

Building on our earlier discussion of structured build orders and secure filesystem-based pipelines, organizing your Markdown knowledge vault requires a careful balance between human-readability and machine-legible precision. 

To keep your coding agents fast, cost-efficient, and structurally constrained, you should construct and govern your Obsidian-style vault using these concrete best practices:

---

### **1. Structural Foundation: "One Fact, One File" (Atomic Memory)**
To prevent schema enforcement, querying, and context-packing from becoming unpredictable or "fuzzy," move away from storing extensive, unstructured prose about multiple concepts inside a single long note (e.g., `memory/projects/alpha.md`) [1].
*   **Decouple Narrative from Facts**: Keep human-readable narrative files for natural browsing in Obsidian [1, 2]. However, split durable, agent-readable facts into highly scoped, typed files under a dedicated folder structure (e.g., `memory/facts/{entity}/{predicate}.md`, such as `memory/facts/elena-voss/role.md` or `memory/facts/elena-voss/employer.md`) [1, 2].
*   **Filepaths as Primary Keys**: Treat the physical **filepath as a human-readable primary key**, define metadata structures using **YAML frontmatter as the schema**, and enforce constraints via a local linting tool (like `tools/lint.py`) [3].
*   **Materialized Read Models**: Rather than forcing your coding agents to crawl, search, and parse dozens of raw Markdown files during an active session, use local scripts (such as `rebuild_indexes.py` and `rebuild-views.sh`) to pre-compile them into a separate directory of **read-only materialized views** (under `memory/_views/` or `memory/_indexes/`) [2-4]. This minimizes file discovery overhead and optimizes token usage.

---

### **2. Context Delivery: The Five-Layer Hierarchy (ICM Separation)**
To prevent prompt entanglement and optimize how coding models handle task constraints, partition your knowledge vault into five distinct context layers [5-7]:
*   **Layer 0 (Global Identity - `CLAUDE.md`)**: Ingests workspace paths, folders, and conventions to orient the agent on "where it is" [5, 6].
*   **Layer 1 (Workspace Routing - `CONTEXT.md`)**: Details pipeline sequencing and stage routes [5, 6].
*   **Layer 2 (Stage-Specific Contracts - `CONTEXT.md` in stage folders)**: Establishes the exact inputs, processes, and outputs for a single workflow task [5, 6, 8, 9].
*   **Layer 3 (The Factory - Stable Reference Material)**: Stores persistent guidelines that remain stable across multiple runs (e.g., `voice.md`, `design-system.md`, style guides, or API notes) [5, 7, 10, 11]. The agent internalizes this layer as behavioral constraints [7, 10, 12, 13].
*   **Layer 4 (The Product - Working Artifacts)**: Consists of dynamic inputs and intermediate outputs that change with each run (such as `research-output.md` or `script_draft.md` inside `output/` folders) [5, 7, 8, 10, 11]. The agent processes this as raw input to transform [10, 12, 13].
*   **Scoping with Inputs Tables**: Each stage's `CONTEXT.md` contract must declare an explicit **Inputs table** specifying the exact Layer 3 and Layer 4 files to load [8, 9, 14]. This selective context engineering delivers a tight 2,000 to 8,000-token context window per stage, avoiding the 40,000+ token monolithic prompt bloat that causes "lost in the middle" cognitive degradation [15-18].

---

### **3. Capability Packaging: Progressive Disclosure & Lazy Loading**
When packaging procedural skills and knowledge, avoid overloading system prompts. Instead, adopt a **three-tier progressive disclosure loading strategy** to scale large libraries cleanly [19-23]:
1.  **Discovery (Startup)**: Load only a lightweight catalog containing the skill name and description from its YAML frontmatter (~50 tokens per entry) [19-22, 24]. This keeps startup costs negligible while making the agent aware of its capabilities [20, 21, 24].
2.  **Activation (Task Triggering)**: When a task matches the skill's description metadata, load the full `SKILL.md` instruction body into active context [19, 20, 22, 25]. Keep the core `SKILL.md` instructions compact, ideally **under 5,000 tokens** (and ideally between 500 to 2,000 tokens) to prevent displacing attention from other active task state [26-29].
3.  **Execution (Conditional Loading)**: Move heavy reference data (like error catalogs, templates, or exhaustive specifications) out of the main body and into separate `references/`, `scripts/`, or `assets/` folders [19, 28, 30-33]. Instruct the agent to load these files **conditionally and lazily** only when specific parameters are met (such as loading `references/api-errors.md` only if a tool returns a non-200 error code) [19-22, 28, 30, 31, 33].

---

### **4. Write Governance: Proposal & Transaction Lifecycles**
When multiple agents collaborate or execute in parallel, uncoordinated writes can corrupt Markdown files or introduce conflicting states. Implement a formal transactional write lifecycle [2, 34]:
*   **The Proposal Lifecycle**: Require a strict write-review path: **`draft` → `proposed` → `approved/rejected` → `applied`** [2, 4]. 
*   **Isolated Agent Inboxes**: Agents should never edit vault facts directly [1, 2]. Instead, they write proposed updates as temporary files to their dedicated inbox folders (e.g., `memory/_inbox/{agent-id}/ops/`) [2].
*   **Atomic Transactions**: Apply changes only after human or "Verifier Agent" approval [4, 35]. When approved, a Python transaction engine (like `tools/transact.py` or `tools/propose.py`) executes an atomic, idempotent write and outputs a permanent Markdown transaction receipt to `memory/_ops/applied/` [2, 4, 34].

---

### **5. Security and Context Discipline: Hard Ignore Boundaries**
Because AI coding agents (such as Claude Code, Cursor, and Copilot) run file discovery by scanning your filesystem directly, standard Git indexes are insufficient for context protection [36, 37].
*   **Git-Ignored is Not Agent-Invisible**: Agents will read files that are ignored by Git unless they are explicitly blocked by tool-specific ignore configurations [37, 38].
*   **Mirror Secrets and Bloat to AI Ignores**: Mirror all sensitive patterns and large generated folders into **tool-specific ignore files** (e.g., `.cursorignore`, `.aiexclude`, or `.aiignore`) [39-42].
*   **Exclude High-Waste Files**: Block agents from reading non-procedural token-wasters like `.tfstate` files (which can contain plaintext secrets), log dumps, `coverage/` reports, `.next/` or `dist/` folders, minified files (`*.min.js`), and SQLite databases (`*.sqlite`, `*.dump`) [41-45]. This keeps context windows clean and ensures the agent's blast radius is restricted [46, 47].
*   **Plain-Language Boundaries**: Use plain-language constraints in your global identity file (`CLAUDE.md`) to establish behavioral boundaries (e.g., "never modify the legacy/ folder"), which complements pattern-based glob ignores [41, 45, 48-50].

---

🗂️ **Would you like me to draft a fully fleshed-out template folder structure and configuration for your workspace identity (`CLAUDE.md`) and a tool-specific ignore file to prevent token waste in your workspace?**

## Links

- [[architecture/integrations]]
- [[decisions/vault-structure]]
