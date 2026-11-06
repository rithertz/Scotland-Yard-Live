# Scotland Yard Live --- Motion & Component Reference Catalogue

**Status:** Research and adoption shortlist\
**Design authority:** `SCOTLAND-YARD-LIVE-DESIGN-SYSTEM-BRIEF.md`\
**Purpose:** Identify reusable interaction and animation techniques for
the Casefile interface.\
**Important:** This is a shortlist for evaluation, not approval to
install dependencies or adopt every component.

## 1. Recommendation at a glance

Use **Motion for React** as the single animation foundation if the
repository does not already contain a suitable one. Treat **Motion
Primitives** as a source of focused, adaptable interface components.
Treat **React Bits** as a selective inspiration/source catalogue,
especially for expressive moments, not as the product's visual system.

The product should not use a component unchanged merely because it looks
impressive in a demo. Every adoption must be restyled to the Casefile
design system and checked for accessibility, reduced motion, bundle cost
and conflicts with the board's pan/zoom/pointer interactions.

Official references: - Motion Primitives:
https://motion-primitives.com/docs - Motion Primitives Dialog:
https://motion-primitives.com/docs/dialog - Motion Primitives Text
Effect: https://motion-primitives.com/docs/text-effect - Motion
Primitives Animated Background:
https://motion-primitives.com/docs/animated-background - Motion for
React: https://motion.dev/docs/react - React Bits:
https://www.reactbits.dev/ - React Bits component catalogue:
https://www.reactbits.dev/get-started/index

## 2. Core animation foundation

### Motion for React --- recommended foundation

**Role:** Shared animation engine for React UI and SVG-related
transitions.

Potential uses: - Enter/exit transitions for drawers, dialogs and
contextual inspectors. - Turn-state transitions and small status
changes. - Ticket selection feedback. - Pawn movement, only when driven
by authoritative source/destination coordinates. - Gesture interactions
where appropriate and carefully isolated from board pan/zoom.

Why it fits: - React-native declarative API. - Supports gestures, layout
transitions and presence/exit animations. - Can animate SVG and ordinary
interface elements. - Provides a common foundation rather than several
unrelated animation packages.

Adoption decision: **Recommended, subject to repository dependency
inspection.** Do not install it until Codex checks the current package
manifests and lockfile. If an existing compatible Motion installation is
already present, reuse it.

Reference: https://motion.dev/docs/react

## 3. Motion Primitives shortlist

Motion Primitives describes itself as a collection of reusable animated
components built around Motion and Tailwind CSS. Its components can be
customised to fit an existing UI kit. It is therefore a useful source of
implementation patterns, but its defaults should not dictate our visual
style.

  ---------------------------------------------------------------------------------
  Component /       Scotland Yard Live   Decision          Adaptation notes
  pattern           use
  ----------------- -------------------- ----------------- ------------------------
  Dialog            Join room,           **Strong          Restyle as restrained
                    confirmation, leave  candidate**       dark/paper casefile
                    room, game-end                         dialog. Verify focus
                    details                                trap, Escape behaviour
                                                           and focus return.

  Accordion /       Expandable move log, **Strong          Use compact ruled
  Collapsible       player details,      candidate**       dossier sections;
                    rules/help                             preserve clear keyboard
                                                           semantics.

  Animated          Active tab, selected **Strong          Use a subtle sliding
  Background        ticket, active       candidate**       paper/ink highlight, not
                    roster item                            a glowing gradient.

  Segmented Control Optional view/filter **Candidate**     Only where the choices
                    selectors                              are mutually exclusive
                                                           and the control is
                                                           genuinely useful.

  Popover           Compact station      **Candidate**     Avoid on the board if it
                    metadata or                            blocks nearby stations
                    secondary action                       or creates pointer
                                                           conflicts.

  Text Effect       Rare                 **Limited use**   Use short word/line
                    reveal/round-title                     fades; avoid
                    moment                                 character-by-character
                                                           spectacle for routine
                                                           status.

  Carousel          Not a primary game   **Generally       A board game is not a
                    interaction          reject**          marketing carousel; use
                                                           only if a real content
                                                           sequence requires it.

  Drag to Reorder   Not currently        **Reject for      Player order and game
                    required             current scope**   state are rules-driven,
                                                           not user-sortable
                                                           decoration.

  Magnetic /        Not appropriate for  **Reject for      Cursor-following motion
  Spotlight / Tilt  core board controls  board**           can impair precision,
  effects                                                  touch support and board
                                                           navigation.
  ---------------------------------------------------------------------------------

References: - Dialog: https://motion-primitives.com/docs/dialog - Text
Effect: https://motion-primitives.com/docs/text-effect - Animated
Background: https://motion-primitives.com/docs/animated-background -
Full catalogue: https://motion-primitives.com/docs

### Practical Motion Primitives guidance

-   The Dialog component supports controlled open state and custom
    enter/exit variants. This maps well to room and confirmation flows,
    provided accessibility behaviour is verified.
-   Text Effect supports word, character and line segmentation. For this
    product, prefer line/word treatments and reserve them for important
    moments.
-   Animated Background is useful for a moving selection indicator
    behind tabs or compact choices; adapt it to brass/paper/ink rather
    than copying its default styling.

## 4. React Bits shortlist

React Bits offers animated React components and backgrounds as source
that can be copied or installed, with JavaScript/TypeScript and
CSS/Tailwind options. That source-owning model is useful because we can
inspect and adapt the code. The catalogue is broad, including text,
background, cursor, UI and 3D/shader effects; most are not appropriate
for the live game surface.

  -----------------------------------------------------------------------
  Component /       Scotland Yard     Decision          Adaptation notes
  pattern           Live use
  ----------------- ----------------- ----------------- -----------------
  Split Flap Text   Optional round    **Limited         Only for a small,
                    number /          candidate**       non-critical
                    dispatch-board                      display; ensure
                    motif                               text remains
                                                        readable and
                                                        reduced-motion
                                                        fallback exists.

  Fold Text         Rare casefile     **Limited         Could evoke paper
                    title or reveal   candidate**       unfolding; do not
                    heading                             use for changing
                                                        live game data.

  Staggered Text /  Game-start or Mr  **Limited         Short, one-time
  Split Text        X reveal title    candidate**       entrance; avoid
                                                        per-character
                                                        animation in
                                                        routine UI.

  Animated List     New event         **Candidate**     Useful if events
                    appearing in                        are confirmed and
                    move/activity log                   ordered; never
                                                        animate
                                                        speculative or
                                                        unconfirmed moves
                                                        as fact.

  Modal Cards       Possibly game-end **Candidate with  Evaluate
                    dossier           caution**         semantics and
                    presentation                        keyboard
                                                        interaction;
                                                        avoid 3D card
                                                        theatrics.

  Simple Graph      No current core   **Defer**         Could support a
                    use                                 future admin
                                                        analytics view,
                                                        not the gameplay
                                                        board.

  Draggable Grid /  No current use    **Reject**        Unrelated to the
  Circle Gallery                                        core tactical
                                                        board experience.

  Smooth Cursor /   None              **Reject**        Can interfere
  Custom Cursor                                         with precision,
                                                        accessibility and
                                                        touch; do not
                                                        replace the
                                                        system cursor on
                                                        the board.

  Particle Text /   None in routine   **Reject**        Too decorative
  Text Scatter /    gameplay                            and potentially
  Glitch Text                                           reduces
                                                        legibility.

  3D cards, shader  None in core game **Reject**        Adds performance
  backgrounds,                                          and maintenance
  WebGL scenes                                          cost while
                                                        competing with
                                                        the physical
                                                        board.

  Parallax / scroll None in board     **Reject**        Board pan/zoom
  effects           viewport                            already owns
                                                        spatial
                                                        navigation; do
                                                        not layer
                                                        unrelated
                                                        pointer/scroll
                                                        motion over it.
  -----------------------------------------------------------------------

References: - React Bits home: https://www.reactbits.dev/ - Component
catalogue: https://www.reactbits.dev/get-started/index

## 5. Product-specific component mapping

  --------------------------------------------------------------------------------------
  Product surface           Recommended technique    Library source    Priority
  ------------------------- ------------------------ ----------------- -----------------
  Room                      Accessible dialog +      Motion Primitives High
  join/leave/confirmation   presence transition      Dialog + Motion
  dialogs

  Station inspector         Short slide/fade panel   Motion for React  High
                            transition

  Player roster active      Shared animated          Motion Primitives Medium
  marker                    selection background     Animated
                                                     Background

  Ticket selection          Small                    Motion for React  High
                            scale/outline/position   or CSS
                            feedback

  Move/activity log         New confirmed entry      Motion for React; Medium
                            fades/slides into place  React Bits
                                                     Animated List as
                                                     reference

  Turn change               Short transition of turn Motion for React  High
                            indicator and action
                            prompt

  Mr X reveal               Deliberate title/line    Motion + optional High, but rare
                            reveal plus board-state  adapted Text
                            transition               Effect/Fold Text

  Game start/end            One-time casefile-style  Motion + optional Medium
                            reveal                   adapted text
                                                     treatment

  Board station             Lightweight SVG/CSS      CSS first; Motion High
  hover/selection           treatment                only if needed

  Pawn movement             Coordinate-driven SVG    Motion for React  High,
                            transform                or SVG/CSS        evidence-gated
                                                     animation

  Decorative background     Static texture preferred CSS/static asset  Low; avoid
                                                                       animated
                                                                       background
  --------------------------------------------------------------------------------------

## 6. What not to animate

Do not animate: - The whole board as a decorative scene. - The map/board
in response to cursor position. - Every station marker continuously. -
Route lines with perpetual travelling particles. - All text on every
render. - Hidden Mr X information or a speculative destination. -
Unconfirmed network events as if they were accepted game moves. - Ticket
counts in a way that obscures the final value. - Anything that makes the
current legal action ambiguous.

## 7. Adoption and engineering checklist

Before adding a component: 1. Inspect the source code and exact
dependency requirements. 2. Confirm licence and attribution
requirements. 3. Check compatibility with the repository's React, Vite,
TypeScript and Tailwind/CSS setup. 4. Prefer the existing styling
approach; do not introduce Tailwind solely to use a component if the app
does not use it. 5. Check accessibility, focus order, keyboard
interaction and screen-reader semantics. 6. Implement
`prefers-reduced-motion`. 7. Check touch behaviour and narrow layouts.
8. Confirm it does not interfere with board pan/zoom, station hit
targets or pointer capture. 9. Check bundle impact and avoid duplicate
animation engines. 10. Add focused tests for state/interaction
behaviour; use manual visual checks for motion quality.

### Dependency policy

-   Do not install Motion Primitives as a monolithic dependency by
    default; evaluate individual source components and their actual
    dependencies.
-   Do not add React Bits as a blanket runtime dependency; treat it as
    source/reference and own only the components we choose to adapt.
-   Do not add GSAP, Three.js, shader libraries or a second animation
    engine for effects that Motion/CSS can handle.
-   CSS transitions remain preferable for simple hover, focus and colour
    changes.
-   Use Motion where coordinated state-driven transitions, gestures,
    presence or SVG animation materially improve the experience.

## 8. Suggested implementation sequence

1.  **Audit existing frontend dependencies and styling.** Confirm
    whether Motion or another animation package is already present.
2.  **Establish motion tokens and reduced-motion behaviour.** No
    component-library adoption yet.
3.  **Implement one representative dialog and one inspector
    transition.** Validate the casefile look and accessibility.
4.  **Implement ticket/roster selection feedback.** Keep it subtle and
    fast.
5.  **Implement event/turn transitions.** Ensure they are driven by
    confirmed state.
6.  **Implement pawn movement only after canonical coordinates and graph
    semantics are accepted.**
7.  **Add cinematic reveal treatment last.** It depends on reliable
    event/state semantics.

## 9. Important Phase 3C.3 boundary

This catalogue does not authorise the design agent to invent station
coordinates, transport links, starting positions or playable station
count. The canonical graph audit currently has no promoted edges because
evidence was insufficient. The visible station-200 marker remains
unresolved as to playable status.

The physical board artwork must be reconstructed from evidence, not
approximated to fit an animation demo. All pawn movement and legal-move
highlighting must wait for authoritative board/game data.

## 10. Decision summary

-   **Adopt as foundation (after audit):** Motion for React.
-   **Adapt selectively:** Motion Primitives Dialog,
    Collapsible/Accordion, Animated Background, limited Text Effect.
-   **Use as inspiration/source only:** React Bits Animated List, Split
    Flap/Fold/Staggered Text for rare events.
-   **Avoid in core gameplay:** custom cursors, cursor-following
    effects, particle-heavy backgrounds, shader/3D scenes, parallax,
    constant motion.
-   **Keep board interaction precise:** CSS/light SVG states first;
    coordinate-driven Motion for actual pawn movement later.
