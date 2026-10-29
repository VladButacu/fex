# Frontend Excellence router

FEX is the orchestration layer. The user is allowed to speak in outcomes: “this looks cheap,” “make it premium,” “build this dashboard,” “review the UI.” FEX translates that into frontend decisions and specialist work.

## Prime directive

**Do not make the user act as the frontend engineer.** Inspect the repository, infer technical constraints, choose the specialists, execute, validate visually when possible, fix material findings, and report the result.

**Inspect before asking technical questions.** Do not ask the user to choose frameworks, CSS methodology, breakpoints, component libraries, animation libraries, state libraries, font scales, spacing scales, accessibility techniques, rendering strategies, or performance patterns when the repository or standard practice can answer them. Ask only for missing product/brand facts that materially change the outcome and cannot be inferred.

## Mode

The caller supplies `FEX_MODE`:

- `AUTO`: infer CREATE, IMPROVE, or REVIEW from the request and current repo.
- `CREATE`: new page/screen/component/system or a redesign where existing composition is not authoritative.
- `IMPROVE`: default for an existing interface that should look/work substantially better while preserving product behavior and real content.
- `REVIEW`: audit only. Do not modify source unless the user also asks to fix findings.

When AUTO is ambiguous: existing frontend + improvement language → IMPROVE; no existing surface/build from scratch → CREATE; critique/audit language → REVIEW.

## Mandatory first pass

Before design work, inspect enough context to identify:

1. repository instructions (`AGENTS.md`, `CLAUDE.md`, README, relevant docs)
2. framework/runtime, package manifests, and build tooling
3. styling system, component library, shared layout primitives
4. design tokens, CSS variables, themes, Tailwind/config, typography, icon set
5. official brand assets/guidelines
6. target route/component plus neighboring screens
7. real copy/data/assets already present
8. tests/lint/build commands and browser/screenshot tooling

Never assume React, Next.js, Tailwind, shadcn/ui, or any other stack when the project can answer it.

## Authority order

1. explicit user requirements
2. repository/project instructions
3. documented brand identity and official design tokens
4. accessibility/usability requirements
5. established product interaction conventions
6. selected primary visual specialist
7. implementation/performance guidance
8. motion/polish guidance

Repeated undocumented legacy styling is evidence, not law.

## Classify the surface

Choose one primary class:

- **Marketing/public page**: landing/product/portfolio/campaign/public content.
- **Product/app screen**: dashboard/settings/admin/analytics/inbox/editor/workflow/console/tool.
- **Isolated component**: one component, section, form, dialog, navigation element, selector, empty state, etc.
- **Standalone interactive prototype**: no production repo; the artifact itself is the deliverable.

Mixed products are allowed. A marketing page that shows product UI uses page rules outside and app-screen rules inside the product fragment.

## Specialist loading

Read `specialist-map.md`. Bootstrap and read only the needed upstream `SKILL.md` files. Their upstream instructions are authoritative within the bounded job assigned to them. Use **exactly one primary visual authority** for a surface; do not have Taste, UI/UX Pro Max, and Frontend Design independently invent competing systems.

## Execution

### 1. Establish constraints

Internally capture mode, surface class, stack, brand constraints, behavior/content to preserve, target files, and visual tooling.

### 2. Choose the primary visual authority

- Marketing/public page → Taste (`taste-skill`)
- Product/app screen → UI/UX Pro Max (`ui-ux-pro-max`)
- Isolated component → Frontend Design (`frontend-design`)
- Standalone interactive prototype → Web Artifacts Builder (`web-artifacts-builder`) for implementation; establish visual direction first

For a tiny mechanical change with an already-established visual solution, skip art direction and follow the system.

### 3. Add bounded specialists

Use UI/UX Pro Max for targeted accessibility/responsive/forms/navigation/charts/touch/stack concerns when it is not primary. Use React Best Practices only for React/Next.js. Never let Web Artifacts Builder replace a production repo's architecture merely because it is available.

### 4. Build the static interface before decorative motion

The UI must look complete with non-essential motion off. Fix composition, hierarchy, typography, density, spacing, responsive structure, imagery, color, and states first.

### 5. Add purposeful motion

Use Transitions.dev (`transitions-dev`) when interaction motion genuinely communicates state or materially improves interaction. Then use Transitions Polish if existing/new motion needs timing/easing/distance/blur/scale consistency. Respect `prefers-reduced-motion`.

### 6. Visual QA

When browser/screenshot tooling exists, inspect representative widths around **390 px**, **768–820 px**, and **1440 px**, plus critical states: focus/hover as relevant, menus/dialogs open, empty/loading/error, and the densest realistic content. For CREATE/IMPROVE, fix material problems and inspect again.

If visual tooling is unavailable, perform the strongest code-level review possible and explicitly state that pixel-level inspection was unavailable.

### 7. Final quality gates

Read `qa-gates.md`. Use Frontend Design Audit (`frontend-design-audit`) for the final interface/accessibility/UX review. On React/Next.js, also apply relevant React best-practice review. Review motion when motion changed. Run project tests/build/lint/typecheck that are relevant.

Do not declare CREATE/IMPROVE complete while material findings remain unfixed unless a fix would violate explicit requirements or needs unavailable product information.

## Vague aesthetic feedback

For “it doesn't look good,” “make this premium,” “feels generic,” or equivalent:

1. inspect the current result
2. identify the 3–5 highest-impact visual/UX issues
3. route to the correct primary specialist
4. fix those issues
5. inspect again

Do not reflexively add centered heroes, rounded card grids, purple gradients, random shadows, floating ornaments, decorative eyebrow labels, or fade-up animations.

## Reporting

Return a concise lead-level summary: what materially changed/found, resulting direction in plain language, important constraints preserved, validation performed, and any remaining limitation. Do not dump frontend theory unless asked.
