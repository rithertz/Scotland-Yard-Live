# Scotland Yard Live — Video Art-Direction Reference

> **Status:** Approved visual reference addendum
> **Applies to:** Frontend visual system, game-room presentation, board framing, illustration and motion direction
> **Does not override:** Physical-board evidence, canonical game rules, board inventory, transport topology or the approved project architecture

## 1. Reference source

The project owner supplied a short video (`Video-79477.mp4`) as a visual-art reference. This addendum records the visual qualities to carry into Scotland Yard Live.

The video is a style reference, not a source for board geometry, station positions, route connections, game rules or edition identity. Do not copy its exact compositions, characters, logos, artwork or other potentially protected assets. Recreate the general visual language with original assets.

## 2. Visual qualities to carry forward

The reference has a distinctive, dramatic editorial language:

- **Palette:** vivid scarlet/crimson red, deep black, warm ivory/cream and restrained muted neutrals.
- **Illustration:** high-contrast, screen-printed and woodcut/engraving-inspired imagery; visible ink texture, rough edges, distressed marks and strong silhouette shapes.
- **Architecture and setting:** dramatic London/old-city architectural imagery, tall vertical forms, engraved or etched detail, theatrical framing and noir-like shadows.
- **Composition:** bold colour fields, hard-edged transitions, graphic panels, deliberate negative space and occasional oversized visual motifs.
- **Mood:** mysterious, tense, theatrical, investigative and editorial — closer to a premium crime-poster / illustrated case dossier than a generic SaaS dashboard.
- **Texture:** subtle paper grain, ink bleed, worn print character and restrained surface imperfections. Texture must never compromise legibility.

## 3. How this combines with the approved design direction

The existing project direction remains **Metropolitan Pursuit / Confidential Scotland Yard Casefile**. The video reference sharpens its art direction:

**A screen-printed London crime dossier: scarlet signal colour, black ink, aged ivory paper, engraved city imagery and restrained distressed-print texture, wrapped around a physically faithful Scotland Yard board.**

Use the reference to enrich the interface's identity, not to replace the board's original printed design.

### Recommended colour balance

- Use deep ink/near-black as the primary surrounding interface surface.
- Use warm ivory/aged paper for document-like panels, cards, logbook surfaces and selected content areas.
- Use scarlet/crimson as a strong identity and alert accent, in deliberate areas rather than as a full-screen flood.
- Keep the original transport colour semantics distinct and readable: taxi yellow, bus green, underground red and water/boat blue where supported by the source edition.
- Brass/gold may remain a restrained secondary accent from the approved design-system brief.
- Maintain accessible contrast for all operational text, controls and station labels.

The video’s scarlet should strengthen the existing signal-red role; it must not cause taxi, bus and underground route colours to be recoloured or confused.

## 4. Where to apply the style

### Surrounding interface

Appropriate places for the visual language include:

- Game-room opening / lobby and room identity.
- Header, section dividers, status panels and dossier framing.
- Player identity cards, role panels and case notes.
- Logbook, movement history and turn summaries.
- Empty states, loading transitions and game-end presentation.
- Original decorative illustrations: London rooftops, bridges, street lamps, detective silhouettes, archival stamps, case labels and engraved architectural fragments.

Create original illustrations or use appropriately licensed assets. Avoid generic stock-dashboard decoration.

### Board presentation

The physical Milton Bradley 1985 board is a separate fidelity requirement.

- Preserve the physical board's actual geography, printed landmarks, station numbering, route appearance, river, parks, borders and relative layout as supported by evidence.
- Do not convert the original board into a red-and-black poster, woodcut map or newly invented London map.
- Do not redraw uncertain route segments as if they were verified.
- Keep decorative overlays, paper texture and interface framing subordinate to station and route readability.
- The board may sit within a dark, dramatic casefile environment, while the map surface itself remains faithful to the photographed physical edition.

### Motion and transitions

Motion should feel deliberate and theatrical, not continuously animated:

- Use restrained reveals for dossier panels and confirmed turn changes.
- Use purposeful emphasis for Mr X surfacing, a capture, a critical move or a game-ending event.
- Small ink-stamp, paper-slide or print-reveal motifs may be explored for non-critical presentation transitions.
- Never obscure a station, route, ticket count, player action or hidden-information boundary.
- Respect reduced-motion preferences and provide immediate, understandable state changes.

## 5. What not to do

- Do not make the product look like a generic dark SaaS dashboard with a board embedded in it.
- Do not use a flat, clean corporate illustration style that loses the reference's printmaking character.
- Do not cover every surface in grunge, scratches, noise or distressed texture.
- Do not use scarlet as the only interactive or status colour.
- Do not sacrifice text contrast, board legibility, accessibility or responsive behaviour for atmosphere.
- Do not imitate the video's exact artwork, characters, logos, layouts or compositions.
- Do not mistake visual style for evidence about the original board.

## 6. Visual acceptance test

A design review should be able to answer yes to all of the following:

1. Does the experience feel like a premium, illustrated London pursuit dossier rather than a generic web dashboard?
2. Are scarlet, black and aged ivory used with the bold contrast and editorial confidence of the reference?
3. Is there a restrained screen-printed / engraved / distressed-print character in original decorative assets?
4. Does the physical board remain faithful and readable instead of being artistically reinterpreted?
5. Are the transport colours, station labels, game state and controls immediately understandable?
6. Does the atmosphere support the tension of the pursuit without distracting from play?

## 7. Instructions to design and coding agents

Read this addendum alongside:

- `docs/frontend/SCOTLAND-YARD-LIVE-DESIGN-SYSTEM-BRIEF.md`
- `docs/frontend/SCOTLAND-YARD-LIVE-MOTION-COMPONENT-CATALOGUE.md`
- `docs/frontend/VISUAL-IDENTITY-AND-EXPERIENCE.md`
- `SCOTLAND_YARD_LIVE_VISUAL_EXPERIENCE_SPEC.md`
- `docs/game/PHASE-3C3-COORDINATE-RECONSTRUCTION-BRIEF.md`

If a path differs in the live repository, locate the corresponding document rather than creating a duplicate.

For Phase 3C.3, apply this reference primarily to the bespoke SVG board's framing, surface treatment and any original decorative illustration. The board geometry, station positions and any route depiction must remain evidence-led. The video is not a substitute for the supplied board photographs.
