# FEX final quality gates

Apply the gates relevant to the task. In CREATE and IMPROVE modes, material findings are fix-now items. In REVIEW, report them instead of editing unless the user asked for fixes.

## Functional
- Relevant build/typecheck/lint/tests pass.
- Existing behavior/data flows remain intact unless intentionally changed.
- Links, controls, forms, dialogs, menus, navigation, and critical states remain usable.

## Responsive
- No unintended horizontal scrolling.
- Hierarchy remains coherent around 390 px, 768–820 px, and 1440 px.
- Controls remain reachable and comfortably tappable.
- Long labels, realistic data, and dense states do not break layout.

## Accessibility
- Keyboard navigation and visible focus remain viable.
- Interactive controls have meaningful accessible names.
- Color is not the only state indicator and contrast is appropriate.
- Reduced-motion preference is respected.
- Form errors are associated with fields and understandable.

## Visual quality
- First-glance hierarchy is clear.
- Typography, measure, weight, spacing, density, and alignment are intentional.
- Repeated cards/pills/radii encode structure rather than acting as default decoration.
- Random gradients, glows, shadows, eyebrow labels, and fade-up animations are not used as substitute personality.
- When identity matters, at least one visual decision is specific to the product/subject.
- Empty/loading/error states look deliberate.

## Performance/engineering
For React/Next.js, apply relevant Vercel React rules rather than rewriting indiscriminately. Avoid obvious waterfalls, unnecessary client code/oversized imports, needless rerenders, and layout-shifting/unnecessarily heavy assets introduced by the change.

## Motion
- Motion communicates state/change or creates one deliberate focal moment.
- Dismissals feel quicker than entrances where appropriate.
- Staggers do not make the UI wait for itself.
- Content remains understandable with motion disabled.
