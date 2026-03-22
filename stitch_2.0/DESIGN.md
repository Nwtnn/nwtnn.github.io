# Design System Specification: The Kinetic Console

## 1. Overview & Creative North Star
**Creative North Star: The Sovereign Terminal**
This design system moves beyond the cliché "hacker" aesthetic of the 90s to create a high-end, editorialized command center. It is a digital environment that prioritizes raw utility and brutalist precision. By rejecting the "softness" of modern web trends—no rounded corners, no soft shadows—we create a signature experience that feels engineered rather than "designed." 

The system breaks the standard template look through **Intentional Asymmetry**. Layouts should mimic a tiled window manager (like i3 or bspwm), where content blocks are sized by their data density rather than a rigid 12-column grid. We use overlapping "scan-line" overlays and monospace typography to convey an atmosphere of high-level technical authority.

## 2. Colors & Surface Architecture

### The Palette
The core of the system is built on an absolute void (`#131313`), punctuated by high-frequency accents.

*   **Primary (The Pulse):** `primary_container` (#00ff41). This is your high-voltage neon green. Use it sparingly for primary actions and "system active" states.
*   **Secondary (The Subsystem):** `secondary_fixed` (#9cf0ff). A cold cyan for data visualization and secondary navigation.
*   **Tertiary (The Warning):** `tertiary_fixed_dim` (#ffba38). An amber tone used exclusively for "Read-Only" states, warnings, or legacy data strings.

### The "No-Line" Rule & Surface Hierarchy
Traditional 1px solid borders are strictly prohibited for sectioning. We define space through **Tonal Volumetric Shifts**:
*   **Base Layer:** `surface` (#131313) for the main viewport.
*   **Inset Modules:** Use `surface_container_lowest` (#0e0e0e) for recessed code blocks or terminal inputs to create a "carved" effect.
*   **Raised Modules:** Use `surface_container_low` (#1c1b1b) for hover states or active "windows."
*   **The Glass & Gradient Rule:** For hero sections, use a subtle vertical gradient from `surface` to `surface_container_high` (#2a2a2a) to simulate the slight light falloff of an old CRT monitor.

## 3. Typography: The Monospace Manifesto
All communication happens through `spaceGrotesk` (configured as a monospace-adjacent utility font) to maintain a cohesive, "code-first" hierarchy.

*   **Display (The Logotype):** `display-lg` (3.5rem). Use for massive, impactful headlines. Letter-spacing should be set to `-0.02em` to create a dense, blocky "wall of text."
*   **Headline (The Command):** `headline-md` (1.75rem). Used for section titles. Always prefix with a `>` character (e.g., `> WORK_HISTORY`).
*   **Body (The Data):** `body-md` (0.875rem). Optimized for legibility. Use `on_surface_variant` (#b9ccb2) for long-form text to reduce eye strain against the black background.
*   **Label (The Metadata):** `label-sm` (0.6875rem). Use for timestamps, file sizes, and status tags. Always uppercase.

## 4. Elevation & Depth: Tonal Layering
In a "flat" hacker aesthetic, depth is an illusion created by light, not physical height.

*   **The Layering Principle:** Instead of shadows, use "Phosphor Glow." When an element needs to stand out, apply a subtle outer glow using the `primary` color at 10% opacity, mimicking the light bleed of a high-contrast screen.
*   **The "Ghost Border" Fallback:** If a boundary is required for a blocky button or input, use `outline_variant` (#3b4b37) at 20% opacity. It should look like a faint guide-line in a CAD program, not a decorative border.
*   **CRT Flicker & Scanlines:** Apply a global overlay using a repeating linear gradient (1px lines) at 3% opacity. This adds a "tactile" digital texture that makes the flat surfaces feel alive.

## 5. Components

### Buttons (Command Triggers)
*   **Primary:** Sharp 90-degree corners. Background: `primary_container`. Text: `on_primary_container`. On hover, trigger a "glitch" transition where the background shifts to `primary_fixed` and the text jitters by 1px.
*   **Secondary:** Ghost style. Border: 1px `outline`. On hover, fill with `surface_container_high`.

### Inputs (Terminal Prompts)
*   **Text Fields:** No background. A simple `outline_variant` bottom border. The cursor should be a solid `primary` block that blinks (0.5s interval).
*   **Syntax Highlighting:** Within code blocks, use `secondary` for strings, `tertiary` for functions, and `primary` for keywords.

### Cards & Modules
*   **Forbid Dividers:** Use `spacing-8` (1.75rem) to separate content.
*   **Structure:** Every card must have a "header bar" using `surface_container_highest` with a small `label-sm` indicating the "file name" or "module ID."

### Navigation (The Directory)
*   Vertical orientation on the left-hand side. Active links should be prefixed with an asterisk `*` and use the `primary` color.

## 6. Do’s and Don’ts

### Do:
*   **Embrace the Grid:** Align everything to the `0.2rem` spacing increments. Precision is the soul of this system.
*   **Use Functional Animation:** Transitions should be "instant" (0ms to 100ms) or use a "stepped" easing function to mimic terminal rendering.
*   **Maximize Contrast:** Ensure all primary data strings use `on_surface` (#e5e2e1) against the dark background.

### Don’t:
*   **No Border Radii:** Never use `border-radius`. Everything is a sharp 90-degree angle.
*   **No Soft Shadows:** If it doesn't exist in a terminal, it doesn't exist here. Use color shifts for hierarchy.
*   **No Imagery with Soft Edges:** If photos are used, apply a high-contrast greyscale filter or a duotone (Green/Black) effect to make them feel integrated into the "system."