# Scotland Yard Live --- Final Visual Direction & Design-System Brief

**Status:** Approved design direction\
**Product:** Scotland Yard Live\
**Purpose:** Design authority for the frontend and board presentation
during Phase 3C.3 preparation\
**Scope exclusions:** This document does not define canonical board
topology, coordinates, station inventory, game rules, authoritative
state, or multiplayer protocol.

## 1. Approved design decisions

  -----------------------------------------------------------------------
  Dimension                           Decision
  ----------------------------------- -----------------------------------
  Visual personality                  **Metropolitan Casefile** ---
                                      vintage detective dossier, paper,
                                      ink, brass and investigative
                                      editorial design

  Interface density                   **Balanced** --- board dominates;
                                      essential game information remains
                                      accessible

  Animation                           **Expressive** --- noticeable,
                                      purposeful transitions and
                                      cinematic moments, not constant
                                      motion

  Board presentation                  **Physical** --- preserve the
                                      original board's visual character
                                      and geography; do not modernise it
                                      into a generic map

  Surrounding interface               **Dark** --- deep ink/navy shell
                                      around warm paper dossier surfaces
  -----------------------------------------------------------------------

**Design statement:** Scotland Yard Live is a confidential metropolitan
pursuit casefile: a dark, premium investigative operations room wrapped
around a physically faithful London board, brought to life with
expressive, purposeful motion and uncompromising tactical clarity.

### Central usability test

Within approximately two seconds, a player should understand: 1. Whose
turn it is. 2. What action is currently available or expected. 3. Where
the relevant action is on the board. 4. What important information has
changed.

The board is the primary evidence surface. The surrounding interface is
the operations layer.

## 2. Product personality and art direction

The product should feel investigative rather than theatrical:
confidential, precise, tactical, period-London, quietly cinematic. Use
precise labels, docket numbers, evidence tabs, ruled dividers,
classified states and compact operational metadata.

Every flourish must establish the world, clarify game state, guide
attention, reward an important interaction, or communicate a meaningful
transition.

Avoid detective clichés used as decoration: magnifying glasses
everywhere, cartoon fingerprints, fake red-string walls, excessive
distressed textures, ornamental badges without meaning, and generic SaaS
dashboard styling.

### Visual hierarchy

1.  Canonical physical board --- largest and primary visual focus.
2.  Turn/action state --- immediately visible and unmistakable.
3.  Player/pawn status and ticket resources --- accessible without
    obscuring the board.
4.  Station inspector and move history --- contextual and compact.
5.  Atmosphere and decoration --- subordinate to functional information.

Balanced density does not mean every panel must always be open. Use
progressive disclosure, drawers, compact summaries and contextual
inspectors. Do not hide essential turn/action information behind
navigation.

Reference language: period London cartography, police casework, noir
editorial design and tactical instrumentation. Motion Primitives and
React Bits are technique/component sources, not visual templates.
Richup.io is explicitly not a visual reference.

## 3. Approved colour tokens

These existing tokens remain the baseline. Refinements require
justification; do not silently replace their semantic roles.

  -----------------------------------------------------------------------
  Token                   Value                   Role
  ----------------------- ----------------------- -----------------------
  `--ink-950`             `#0B1018`               Deepest application
                                                  background

  `--ink-900`             `#151D28`               Command bar, dossiers,
                                                  primary dark surfaces

  `--ink-800`             `#242A32`               Raised panels, board
                                                  frame, dark controls

  `--charcoal-700`        `#343A42`               Secondary borders and
                                                  muted controls

  `--paper-100`           `#E9DDC5`               Main board base and
                                                  paper surfaces

  `--paper-200`           `#F5EBD8`               Paper highlights and
                                                  high-contrast labels

  `--paper-300`           `#CDBB9C`               Paper borders,
                                                  annotations and muted
                                                  fills

  `--text-ink`            `#202A32`               Text on paper

  `--text-muted`          `#87939A`               Secondary text on dark
                                                  surfaces

  `--signal-red`          `#D71920`               Mr X, pursuit signals,
                                                  urgent alerts, selected
                                                  evidence

  `--blood-red`           `#8F171C`               Deep crimson fills and
                                                  meaningful stamps

  `--signal-gold`         `#D9A83F`               Detective emphasis,
                                                  selected tickets,
                                                  active state

  `--muted-brass`         `#9E8150`               Metadata and aged
                                                  hardware cues

  `--taxi-yellow`         `#D6A928`               Taxi route

  `--bus-green`           `#39846A`               Bus route

  `--underground-red`     `#B94A4B`               Underground route

  `--water-blue`          `#4F86A5`               River and boat route

  `--focus-blue`          `#2E77B7`               Keyboard focus only
  -----------------------------------------------------------------------

Colour rules: - Use colour semantically, not decoratively. Signal red
must remain scarce. - Do not use crimson for generic selection if it
could be confused with Mr X or danger. - Transport modes must differ
through colour, line pattern and visible legend/label; never colour
alone. - Maintain strong contrast on dark and paper surfaces. - Keyboard
focus must be distinct from game selection.

## 4. Typography

Use three clear roles:

-   **Editorial display:** Playfair Display, Source Serif 4 or Cormorant
    Garamond. Case titles, major headings and selected editorial
    moments. Sentence case, controlled tracking and readable leading.
-   **Interface sans:** DM Sans, Inter or IBM Plex Sans. Controls,
    player names, instructions and body copy. Prioritise compact-size
    legibility.
-   **Operational mono:** DM Mono, IBM Plex Mono or another readable
    monospace. Room codes, station IDs, timestamps, ticket counts and
    short stamps.

Do not use monospace for paragraphs or uppercase for every label.
Inspect existing font loading before adding dependencies. Prefer a small
set of families/weights, robust fallbacks and no font-loading layout
shifts.

## 5. Layout, spacing and surfaces

### Spacing

Use a 4px base unit and preferred rhythm: `4, 8, 12, 16, 24, 32, 48px`.
Centralise tokens rather than scattering arbitrary values.

### Desktop

-   Give the board the largest share of available space.
-   Side panels are attached dossier leaves, not equal dashboard
    columns.
-   Keep turn/action state visible near the board.
-   Avoid panel widths that make the board hard to interpret.
-   Visually distinguish the warm paper board from the dark operations
    shell.

### Mobile/narrow layouts

-   Preserve the board as the central interaction surface.
-   Move secondary dossiers/history into drawers, sheets or compact
    tabs.
-   Do not merely shrink the desktop dashboard.
-   Keep primary turn/action information available.
-   Maintain practical touch targets and avoid overlap with station hit
    targets.

### Surface rules

-   Dark panels: 1px translucent rule and one restrained shadow.
-   Paper: warm base, fine static grain and thin ink rules.
-   Crimson stamps: meaningful statuses only; optional 1--2° rotation,
    never generic decoration.
-   Avoid stacks of identical rounded cards; prefer composed surfaces
    and internal dividers.
-   Use 2--3px top rules for section identity and 1px rules for
    information grouping.
-   Reserve rounded corners mainly for controls, markers and interactive
    elements; casefile surfaces remain mostly square.
-   Texture is atmosphere, never content; it must not reduce
    station-number or label legibility.

## 6. Board presentation --- physical fidelity is mandatory

The board must preserve the original board's visual character, relative
geography, route styling, station-number treatment, river and meaningful
printed details **where supported by verified evidence**. Physical
fidelity is an evidence constraint, not permission to invent.

### Canonical-data boundary

The board renderer is a presentation layer for typed board data. It is
not the source of truth for station inventory, coordinates, topology,
starting positions, movement legality, turn order or ticket accounting.

The current synthetic board fixture remains explicitly demo-only until
canonical reconstruction and validation are complete.

The transport graph audit concluded that evidence was insufficient to
promote a canonical graph. Do not infer canonical connections from
styling, provisional candidates or an attractive rendering. Station 200
is visibly printed, but its playable-inventory status is unresolved; do
not silently choose 199 or 200. Rulebook-supported boat legs do not by
themselves prove that the photographed board is the exact matching
edition. Preserve provenance and uncertainty.

### Board rendering layers

1.  Paper base and verified geography.
2.  Fine cartographic detail.
3.  Verified transport routes.
4.  Station markers and labels.
5.  Legal-move hints supplied by authoritative state.
6.  Visible pawns.
7.  Selection and keyboard-focus treatments.
8.  Confirmed effects and reveal states.

The renderer must not create gameplay truth from visual effects.

### Geometry and interaction

-   Maintain a stable SVG coordinate system and preserve board aspect
    ratio.
-   Pan/zoom the board scene as one coherent surface.
-   Keep inspector and evidence/history panels outside the SVG scene.
-   Make station hit targets larger than visible markers.
-   Keep labels legible at useful zoom levels.
-   Support keyboard focus and pointer selection.
-   Avoid hit-target overlap; document unavoidable crowded areas.

### Station states

Support default, hover, keyboard focus, selected, connected-to-selection
(only when supplied by valid data/state), occupied, revealed and
disabled/unavailable states. Selection must not rely on colour alone;
use a clear ring/pin treatment and nearby inspector/report. Occupancy
and disabled states must remain distinguishable.

### Pawns and hidden information

Pawn identity must be consistent across board, roster, tickets and
history. Mr X uses a classified crimson identity and language such as
**"Location concealed."** Never expose hidden Mr X information in client
state or presentation unless the server-authorised projection says it is
revealed.

## 7. Interface inventory

  -----------------------------------------------------------------------
  Area                    Treatment               Priority information
  ----------------------- ----------------------- -----------------------
  Command/header          Dark ink, compact       Room, round,
                          metadata, restrained    connection/game status
                          brass

  Main board              Warm paper inside dark  Board and active
                          frame                   pursuit

  Turn/action indicator   High-contrast           Whose turn; expected
                          operational panel       action

  Player/personnel        Dark shell with paper   Player, pawn and status
  dossier                 details

  Station inspector       Paper report/dossier    Station ID and
                          leaf                    authorised context

  Ticket folio            Tactile ticket/card     Ticket type and
                          treatment               remaining count

  Move history            Ruled logbook/timeline  Recent confirmed
                                                  moves/events

  Mr X dossier            Classified dark/crimson Authorised visible
                          treatment               information only

  Dialogs                 Focused premium modal   One task at a time

  Notifications           Short, high-signal      Important changes only
                          treatment
  -----------------------------------------------------------------------

Avoid repeating the same information across panels unless repetition
materially improves immediate game comprehension.

## 8. Motion direction --- expressive, purposeful and controlled

The approved animation personality is **expressive**. Meaningful
interactions may have noticeable transitions and cinematic emphasis. The
screen must not constantly move.

Motion must clarify cause/effect, establish hierarchy, make important
events consequential, help track state changes and preserve spatial
continuity. It must never delay or obscure a time-sensitive multiplayer
action.

### Motion tiers

  -----------------------------------------------------------------------
  Tier                    Examples                Character
  ----------------------- ----------------------- -----------------------
  Micro                   Button press, ticket    Immediate, crisp,
                          selection, focus/hover  subtle

  Interface               Drawer, inspector,      Smooth, clearly
                          dialog, panel           noticeable

  Game event              Pawn movement, turn     Expressive and
                          change, ticket use      spatially coherent

  Cinematic               Mr X reveal, game       Strongest emphasis;
                          start/end, decisive     rare and brief
                          capture
  -----------------------------------------------------------------------

### Suggested initial timing ranges

These are starting points for implementation and playtesting, not rigid
mandates.

  Motion                     Initial duration
  ------------------------ ------------------
  Hover/press feedback              90--160ms
  Small state transition           140--220ms
  Panel/drawer                     200--320ms
  Pawn movement                    250--450ms
  Turn transition                  250--400ms
  Important reveal                 450--750ms
  Game start/end                   500--900ms

Prefer transform and opacity. Use consistent easing: responsive ease-out
for entrances, ease-in for exits and deliberate but not sluggish curves
for game events.

### Board animation constraints

-   Animate a pawn between exact source/destination coordinates supplied
    by canonical data/state.
-   Never draw or imply an unverified route connection.
-   Do not interpolate through unrelated station markers if it implies
    false movement.
-   Keep camera and pawn coordinate systems aligned.
-   Avoid simultaneous camera/pawn movement that makes the destination
    hard to track.
-   Final pawn position must match authoritative state, not animation
    progress.
-   Reconcile late/out-of-order events to authoritative state.
-   Effects must not obscure station IDs or pawns.

Reserve strongest effects for Mr X reveal rounds, capture/game-ending
events, game start and important confirmed state changes. Do not
dramatise every ordinary move.

### Accessibility

Respect `prefers-reduced-motion`. Replace long travel animations with
short fades/direct position changes; remove parallax, large scale
effects and continuous decorative movement. Preserve feedback through
labels, focus, contrast and concise status text. Information must never
be available only through animation.

## 9. Motion Primitives and React Bits adoption policy

Use the libraries as component/technique sources, not as wholesale
design systems.

-   Prefer one coherent Motion-based animation foundation where
    justified.
-   Inspect package versions, lockfile, current installation
    instructions and APIs before adding dependencies.
-   Avoid duplicate animation engines.
-   Copy/adapt only components that can be restyled to this design
    system.
-   Candidate Motion Primitives use: dialogs, accordions/expandable
    panels, limited text transitions and reusable interface patterns.
-   Candidate React Bits use: restrained micro-interactions, limited
    text effects, selective emphasis/spotlight and subtle surface
    techniques.

Avoid particle-heavy backgrounds, cursor-following board effects,
distortion, excessive 3D cards, neon/glow-heavy treatments and
decorative motion with no information value.

For each adopted component, record: 1. Source/component and license. 2.
Product rationale. 3. Dependency and bundle impact. 4.
Accessibility/keyboard behaviour. 5. Reduced-motion behaviour. 6.
Theming compatibility. 7. Potential conflict with board pan/zoom or
pointer handling. 8. Tests/manual acceptance checks.

Prefer owning a small, understandable amount of adapted source over
importing an entire visual framework when that provides better control.

## 10. Technical boundaries

The frontend may own local presentation state: selected station,
selected ticket/control, viewport transform, open panels and animation
progress.

It must not own authoritative game state, movement legality, ticket
accounting, canonical board data, hidden Mr X location or server
validation. The server-authorised projection is the source for visible
multiplayer state.

Keep separate: - Canonical board data and provenance. - SVG rendering. -
Viewport pan/zoom. - Selection and inspector presentation. -
Authoritative legal-move hints. - Pawn/event animation.

Existing frontend foundation includes: -
`apps/web/src/features/board/components/BoardSvg.tsx` -
`apps/web/src/features/board/components/BoardViewport.tsx` -
`apps/web/src/features/board/data/demo-board-fixture.ts` -
`apps/web/src/features/game-room/components/GameRoomShell.tsx` -
`apps/web/src/styles.css` -
`docs/frontend/VISUAL-IDENTITY-AND-EXPERIENCE.md`

Preserve the synthetic fixture boundary and tests until verified
canonical data is ready. Do not casually replace the existing viewport
interaction model; any proposed change must explain rationale,
interaction consequences and migration/testing.

## 11. Accessibility, responsiveness and performance

### Accessibility

-   All actions keyboard reachable.
-   Visible focus distinct from selection.
-   Never rely on colour alone.
-   Use semantic controls and meaningful accessible names.
-   Announce important state changes without overwhelming assistive
    technology.
-   Respect reduced motion.

### Responsiveness

-   Desktop composition prioritises a large board.
-   Mobile is deliberately composed, not merely shrunken.
-   Touch targets remain practical.
-   Drawers/panels must not cover the only board controls.
-   Avoid hover-only functionality.

### Performance

-   Prefer transform/opacity animation.
-   Avoid rerendering the full SVG scene for transient effects.
-   Keep textures lightweight.
-   Avoid large image/video backgrounds.
-   Profile with realistic station/route counts.
-   Keep the application responsive during live updates.

## 12. Design-system deliverables

Centralise tokens for colour, typography, spacing, borders/dividers,
surfaces/shadows, z-index/layers, motion durations/easing, focus and
interaction states. Avoid duplicated magic values.

Required outputs: 1. Revised visual identity document referencing this
brief. 2. Centralised CSS variables/tokens. 3. Typography
loading/fallback strategy. 4. Styling rules for dark shell and paper
surfaces. 5. Motion tokens and reduced-motion handling. 6. Component
inventory with adopted/rejected library references. 7. Desktop and
narrow-screen composition rules. 8. Manual visual QA checklist.

Do not implement canonical board artwork or invent coordinates as part
of generic design-system work. Board reconstruction/geometry must follow
the evidence-gated Phase 3C.3 process.

## 13. Visual QA acceptance checklist

-   [ ] Experience reads as a confidential metropolitan casefile.
-   [ ] Surrounding interface is predominantly dark ink/navy.
-   [ ] Paper surfaces are warm and physical, not flat white.
-   [ ] Board is visually dominant.
-   [ ] Physical board appearance is preserved where evidence supports
    it.
-   [ ] Information density is balanced.
-   [ ] Turn/action state is quickly identifiable.
-   [ ] Typography roles are distinct and readable.
-   [ ] Route types are not distinguished by colour alone.
-   [ ] Station numbers/routes remain legible.
-   [ ] Selection, occupancy, focus and reveal states are
    distinguishable.
-   [ ] Important motion is expressive; routine motion remains
    efficient.
-   [ ] Reduced-motion mode remains usable.
-   [ ] Narrow layouts are deliberately composed.
-   [ ] No visual effect implies unverified topology or rules.
-   [ ] No hidden Mr X information is exposed.
-   [ ] Existing pan/zoom remains coherent.
-   [ ] No unnecessary animation or component dependency is introduced.

## 14. Explicit non-goals

This brief does not authorise custom maps or a board editor, new game
rules, invented coordinates/connections, technology-stack changes, full
UI framework replacement, generic dashboard redesign, Richup-inspired
design, constant decorative motion, client-side authority over hidden
information, matchmaking or speculative scale features.

## 15. Agent handoff instructions

Before implementation, an agent must: 1. Read the consolidated project
plan and existing visual identity document. 2. Inspect current frontend
components, styles, dependencies and lockfile. 3. Distinguish
implemented behaviour from design targets. 4. Produce a gap analysis and
component adoption proposal before broad changes. 5. Avoid changing
canonical board data or gameplay rules. 6. Perform no Git operations.
The repository owner alone creates commits, pushes, branches, merges and
changes GitHub settings. 7. Work in bounded, reviewable slices with
appropriate tests. 8. Report changed files, dependencies, checks,
limitations and decisions requiring owner approval.

### Phase 3C.3 boundary

The upcoming coordinate reconstruction and canonical SVG board are
high-risk work. This design direction informs presentation but does not
override evidence. A beautiful but geometrically or topologically
inaccurate board is a failed result. Evidence, provenance, uncertainty
and review gates take precedence over visual completion.
