# Scotland Yard Live — Visual Identity & Experience

Status: working design direction for the visual foundation  
Edition target: Milton Bradley 1985  
Product mode: private multiplayer rooms; this document does not define game rules or canonical board data.

## 1. Design philosophy

Scotland Yard Live is a confidential metropolitan pursuit room. It should feel like a working police casefile opened on a desk: tactile, intelligent, urgent, and quietly cinematic. The board is the evidence surface; the surrounding interface is the operations layer that helps players read it.

The product personality is investigative rather than theatrical. It favors precise labels, restrained stamps, confident typography, and strong hierarchy over decorative detective clichés. Every flourish must either establish the world, clarify state, or reward an important interaction.

The central design test is: can a player understand whose turn it is, what they can do, and where the action is on the board within two seconds?

## 2. Creative direction

Working title: **Metropolitan Pursuit — A Confidential Scotland Yard Casefile**.

The visual language combines four references:

- Period London cartography: warm paper, ink lines, district fields, river blue, and a visibly printed map surface.
- Police casework: evidence tabs, docket numbers, ruled dividers, classified states, and short operational metadata.
- Noir editorial design: deep ink fields, crimson signal moments, asymmetrical labels, and a controlled sense of tension.
- Tactical instrumentation: clear states, keyboard focus, reliable zoom/pan, and compact data readouts.

The supplied React Bits, Motion Primitives, and unslop references are used as technique references, not as a visual template. Prefer source-owned, small interactions; motion that explains state; and a deliberate audit of hierarchy, spacing, copy, and surface treatment before adding decoration.

## 3. Colour system

| Token               | Value     | Semantic use                                       |
| ------------------- | --------- | -------------------------------------------------- |
| `--ink-950`         | `#0B1018` | Application shell and deepest background           |
| `--ink-900`         | `#151D28` | Command bar, dossiers, tactical surfaces           |
| `--ink-800`         | `#242A32` | Raised panels, map frame, dark controls            |
| `--charcoal-700`    | `#343A42` | Rules, muted controls, secondary borders           |
| `--paper-100`       | `#E9DDC5` | Map base and primary paper surface                 |
| `--paper-200`       | `#F5EBD8` | Paper highlights and high-contrast labels          |
| `--paper-300`       | `#CDBB9C` | Paper borders, muted fills, map annotation         |
| `--text-ink`        | `#202A32` | Text on paper                                      |
| `--text-muted`      | `#87939A` | Secondary interface text                           |
| `--signal-red`      | `#D71920` | Active pursuit, Mr X, alerts, selected evidence    |
| `--blood-red`       | `#8F171C` | Deep crimson fills and stamped states              |
| `--signal-gold`     | `#D9A83F` | Detective emphasis, selected tickets, active state |
| `--muted-brass`     | `#9E8150` | Quiet metadata and aged hardware cues              |
| `--taxi-yellow`     | `#D6A928` | Taxi route                                         |
| `--bus-green`       | `#39846A` | Bus route                                          |
| `--underground-red` | `#B94A4B` | Underground route                                  |
| `--water-blue`      | `#4F86A5` | River and boat route                               |
| `--focus-blue`      | `#2E77B7` | Keyboard focus only                                |

Use colour by role, not as decoration. Signal red should be scarce enough to carry urgency. Route types must always be differentiated by a combination of colour, stroke pattern, and legend label.

## 4. Typography

Use three roles:

- **Editorial display:** Playfair Display, Source Serif 4, or Cormorant Garamond for case titles, location reports, and major headings. Use sentence case and tight leading.
- **Interface sans:** DM Sans, Inter, or IBM Plex Sans for controls, roster names, instructions, and body copy. Prioritize legibility at compact sizes.
- **Operational mono:** DM Mono, IBM Plex Mono, or another readable mono for room codes, station IDs, timestamps, ticket counts, and stamps.

Display typography carries the world; sans typography carries action; mono typography carries evidence. Do not use mono for paragraphs or use uppercase for every label. Small uppercase labels should be short and tracked, never dense walls of shouting text.

## 5. Spacing, sizing, and surfaces

Use a compact 4px base unit with a preferred rhythm of 8, 12, 16, 24, 32, and 48px. The board should receive the most space on desktop; side panels should feel like attached dossier leaves, not equal dashboard columns.

Surface rules:

- Dark panels use a 1px translucent rule and a single restrained shadow.
- Paper surfaces use a warm base, a fine static grain, and thin ink rules.
- Crimson stamps may be slightly rotated by 1–2 degrees, but only for meaningful status labels.
- Avoid stacked cards with identical radii. Prefer one composed surface with internal dividers.
- Use 2px or 3px top rules for section identity and 1px rules for information grouping.
- Reserve rounded corners for controls and markers; casefile surfaces should remain mostly square.

## 6. Texture and illustration

Texture is atmosphere, not content. Use lightweight CSS or SVG patterns: paper grain at low opacity, cartographic grid lines, district washes, river paths, contour-like street lines, neighbourhood labels, and small editorial registration marks. Texture must never sit above station numbers or interactive text.

The board may include simplified geography, but it must never imply canonical station placement or connectivity unless the source data is verified. Any synthetic fixture must remain visibly labelled as demo data.

## 7. Board visualization principles

The board is a renderer of typed board data, not a rules engine. Its layers are:

1. Paper and geography.
2. Fine street/cartographic detail.
3. Transport routes.
4. Station markers and labels.
5. Move hints supplied by authoritative state.
6. Visible pawns.
7. Selection and focus treatment.
8. Confirmed effects and reveal states.

Keep the SVG coordinate system stable. Keep station hit targets larger than visible markers. Preserve aspect ratio. Pan and zoom should transform the whole scene, while the evidence rail and inspector remain outside the SVG.

Station states include default, hover, keyboard focus, selected, connected-to-selection, occupied, revealed, and disabled. The selected state should use a clear ring or paper pin treatment plus a nearby report card; never rely on a colour change alone.

## 8. Player and pawn language

Mr X is represented by a classified red marker and language such as “Location concealed.” Detectives use distinct but restrained identity colours and a letter or simple pawn silhouette. Pawn colours should be reinforced by names, labels, or position text. Avoid emoji, character portraits, and toy-like 3D pieces in the core map.

Presence is a small status dot, not a large badge. Active player state should be a rule, a crimson edge, or a gold signal rather than a full glowing card.

## 9. Ticket and transport language

The ticket folio is a compact evidence ledger made from small printed-ticket rows. Each ticket has a name, transport letter/icon, remaining count, selected state, and disabled explanation where applicable. Perforation cues, clipped ticket edges, transport-specific insignia, and a subtle selected lift create tactility without turning the panel into a skeuomorphic prop cabinet. Selected tickets use a crimson edge and small physical-card shift; the count should remain stable and easy to scan.

Routes use the same vocabulary as the physical game: taxi is solid gold, bus is differentiated green with a dotted or patterned stroke, underground is crimson and broken, and boat is river blue. Provide a legend and never communicate type by colour alone.

## 10. Component principles

- Command bar: operational identity first, then room and connection metadata, then compact utilities.
- Personnel dossier: one case title, one roster, one clear active state, and a short simulated/canonical status.
- Board frame: board hero plus controls and metadata; do not bury the map in card chrome.
- Tactical rail: current turn first, tickets second, public movement history third.
- Station inspector: a location report that communicates ID, demo/canonical status, transport summary, occupancy, and clear selection.
- Stamps and labels: sparse, meaningful, and repeated consistently.

Avoid placeholder buttons. If a control is demo-only, label it as demo state or make it a real local interaction.

## 11. Motion principles

Motion should explain a state change and then get out of the way. Recommended durations are 160–220ms for hover/selection, 240–420ms for panel entrance, and up to 600ms for a confirmed movement or reveal.

Use a single calm ease-out curve for UI transitions. A selected station may pulse once or settle with a brief ring. Ticket selection may shift the ticket edge and count emphasis. A movement log entry may enter from 6–8px below. Mr X reveal should use a restrained crimson stamp and map focus, never a full-screen effect.

Do not animate continuously, delay urgent actions, or animate a state that has not been server-confirmed. Under `prefers-reduced-motion`, remove loops and replace movement with immediate state changes.

## 12. Responsive principles

- Wide desktop: three-part layout with board dominant.
- Laptop: keep the board dominant and move the evidence rail into a drawer if needed.
- Tablet: retain board and compact dossier context; evidence rail becomes a labelled drawer.
- Mobile: board remains the main surface, controls stay reachable, and case notes become an accessible drawer.

Never force page-level horizontal scrolling. The SVG can pan internally, but the surrounding layout must fit the viewport. Mobile controls need touch targets of at least 44px where practical.

## 13. Accessibility

Every station has an accessible name and keyboard target. Map controls have visible labels and focus rings. Selection is not communicated by colour alone. Text and controls must meet WCAG contrast expectations against their actual surfaces.

The board uses an application landmark with a short instruction. Escape clears selection or closes the current inspector. Plus/minus and zero support zoom/reset; arrow keys pan while the board is focused. Hidden-information rules are enforced by server-filtered payloads in later stages, never by CSS concealment.

## 14. Performance

Keep SVG geometry data-driven and split into reusable layers. Avoid large raster textures and expensive blur filters. Prefer CSS gradients and small inline patterns. Do not add an animation library until motion complexity justifies it; source-owned CSS is enough for the current visual foundation.

If the canonical board grows beyond comfortable SVG performance, profile first. Reassess label simplification, route virtualization, or a different rendering strategy only from measured evidence.

## 15. Tokens and conventions

Keep semantic tokens in one stylesheet and reference them from components. Use `.section-kicker`, `.section-heading`, `.stamp`, `.ticket-row`, `.station-marker`, and `.transport-edge` as shared vocabulary rather than inventing one-off names for every screen.

Data boundaries should be explicit: `BoardFixture` is synthetic visual data; future verified board data should arrive through a separate canonical package or contract. Renderer components may present state but must not decide movement legality, hidden locations, or server authority.

## 16. Future multiplayer states

Future states to design deliberately:

- Reconnecting: persistent non-blocking status with a recovery action.
- Waiting for player: clear active turn and readiness state without fake countdowns.
- Ticket confirmation: summary of ticket and destination before submit.
- Confirmed movement: server-confirmed pawn transition and public log entry.
- Mr X reveal: authorized reveal only, with a crimson evidence stamp and focus treatment.
- Cornered/game over: result panel while the final board remains visible.

These states should extend the same casefile vocabulary rather than introduce a second visual language.
