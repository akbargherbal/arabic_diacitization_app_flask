### **Revised Editor Workflow: Phases 1 & 2**

#### **Phase 1: Initialization & Global State Control**

Your suggestion for a global "active" toggle is a fantastic addition. It addresses a key usability concern.

**Updated Phase 1 Flow:**

1.  **Initialization:** The page loads as before: first sentence displayed, first character focused, sidebar open.
2.  **Default State: Active.** The application is "live" by default. Keyboard inputs (arrow keys, numpad) immediately affect the text.
3.  **Global App Toggle (The "Lock"):**
    - **UI Element:** We will add a new, distinct icon to a corner of the screen—perhaps a "Lock" or "Power" icon in the footer status bar.
    - **Action:** The user clicks this "Lock" icon.
    - **System Response:**
      - The app enters a "Locked" or "Inactive" state.
      - The icon changes to show its locked status (e.g., a closed lock).
      - A subtle visual cue is applied to the entire editor, perhaps a slight dimming (`opacity-75`) and a `cursor-not-allowed` style over the main text area.
      - Crucially, **all keyboard listeners for navigation and diacritic changes are disabled.** The numpad buttons in the sidebar are also disabled. The user can no longer make accidental changes.
    - **Re-enabling:** Clicking the "Lock" icon again returns the app to its active state, removing the overlay and re-enabling all controls.

- **Design Rationale:** This provides a necessary "panic button" or "pause" state. It gives the user full control over when the app is listening, preventing frustration from accidental key presses. It's an essential feature for a polished tool.

---

#### **Phase 2: The Core Editing Loop with Navigation Modes**

Your idea of distinct navigation modes is powerful. It acknowledges that proofreading isn't a one-size-fits-all process. Let's formalize these modes and ensure they work together seamlessly.

**Introducing the "Navigation Mode" Switch:**

- **UI Element:** We will add a small, clear toggle in the sidebar or footer that lets the user switch between the two modes. It could be a simple button group: `[ Character ]` `[ Word ]`. The active mode would be highlighted. Let's place it in the footer for now to keep the sidebar clean.
- **Default Mode:** We can default to "Sentence-Wide Character Navigation" (your Mode B) as it's the most straightforward, but this is an easy parameter to change.

Let's refine the behavior of each mode:

---

### **Mode A: "Word Focus Mode"**

This mode is optimized for carefully correcting a single word before moving on.

- **Entering this Mode:**

  - The user clicks the "Word" button in the navigation mode switcher.
  - The user clicks on any character with the mouse. This action automatically selects both the character _and_ its parent word. The entire word could get a faint highlight to show its "active" status.

- **Navigation within the Word:**

  - **Action:** User presses **Spacebar**.
  - **System Response:** The `.char-focus` moves to the _next_ character within the currently active word. If it's on the last character, it loops back to the first character of that same word.
  - **Action:** User presses **Shift + Spacebar** (a common reverse-cycle pattern).
  - **System Response:** The focus moves to the _previous_ character within the word, looping from first to last.
  - **Arrow Keys (`←`/`→`):** These could behave identically to Spacebar/Shift+Spacebar, or we could reserve them for sentence-wide navigation. For clarity, let's say in this mode, they _also_ only navigate within the current word.

- **Navigating Between Words:**
  - **Action:** User presses **Ctrl + Right Arrow** (or `Ctrl + Spacebar` as you suggested; arrow keys are often more conventional for forward/backward movement).
  - **System Response:** The entire "word focus" jumps to the **first character of the next word**.
  - **Action:** User presses **Ctrl + Left Arrow**.
  - **System Response:** The "word focus" jumps to the **first character of the previous word**.

---

### **Mode B: "Character Flow Mode" (Sentence-Wide)**

This mode is for quickly scanning through the entire sentence character by character.

- **Entering this Mode:** The user clicks the "Character" button in the navigation mode switcher.

- **Navigation:**
  - **Action:** User presses **Right Arrow (`→`)**.
  - **System Response:** The `.char-focus` moves to the very next character in the sentence, seamlessly crossing word boundaries.
  - **Action:** User presses **Left Arrow (`←`)**.
  - **System Response:** The focus moves to the previous character.
  - **Jumping Between Words:** `Ctrl + Right Arrow` and `Ctrl + Left Arrow` work exactly as in Mode A, jumping to the beginning of the next/previous word. This provides a consistent "power user" shortcut across both modes.
  - **Spacebar:** In this mode, the spacebar should probably do nothing to avoid conflicting with its role in Word Focus Mode. This keeps the modes distinct.

### **Unified Logic Summary**

| Action                | Mode A: "Word Focus"                                        | Mode B: "Character Flow"                                     |
| --------------------- | ----------------------------------------------------------- | ------------------------------------------------------------ |
| **Right/Left Arrows** | Moves to next/prev character **within the active word**.    | Moves to next/prev character **across the entire sentence**. |
| **Spacebar**          | Moves to next character **within the active word**. (Loops) | Does nothing.                                                |
| **Shift + Spacebar**  | Moves to prev character **within the active word**. (Loops) | Does nothing.                                                |
| **Ctrl + Right/Left** | Jumps to the first character of the next/prev **word**.     | Jumps to the first character of the next/prev **word**.      |
| **Mouse Click**       | Selects a character and sets its parent word as "active".   | Selects a character.                                         |

This refined system provides a clear, powerful, and flexible set of controls. The user can choose the macro-level tool (Word vs. Character mode) that best suits their immediate task, while the micro-level actions (diacritic input) remain consistent.

#### **Phase 3: Session Control & Completion**

These are the actions that manage the overall session state.

1.  **Toggling the Sidebar (Entering/Exiting Zen Mode):**

    - **Action:** The user clicks the `X` / `≡` button at the top right.
    - **System Response:** The sidebar animates closed or open. The core editing functionality remains unchanged. This is purely a user preference for their workspace layout.

2.  **Completing the Work:**

    - **Action:** The user has proofread the entire sentence and is satisfied with the corrections. They click the **"حفظ و التالي" (Save and Next)** button.
    - **System Response (The Ideal Flow):**
      1.  The current state of the corrected text is saved (in memory for now, eventually to the backend).
      2.  The editor loads the _next_ sentence from the document.
      3.  The entire view resets to the **Phase 1** state for the new sentence: focus on the first character, inspector updated, progress bar reset for the new sentence.

3.  **Exiting the Session:**
    - **Action:** The user simply closes the browser tab or navigates away.
    - **System Response (Future Goal):** The app should ideally auto-save the user's progress periodically to `localStorage`. When the user returns later, the system can ask if they want to resume their "in-progress" session, loading the text and their position exactly where they left off. For now, closing the tab simply ends the session.

This detailed workflow defines exactly what should happen on this page. It gives us a clear blueprint for the Alpine.js implementation, as we now know all the states (`activeCharIndex`, `isCtrlActive`, etc.) and all the methods (`nextChar()`, `setDiacritic()`, etc.) we will need to build.

### **6. The State Management Blueprint: From Data to Interaction**

While the Python-generated HTML serves as the immutable _data state_ (the "what"), we require a robust system to manage the transient _session state_ (the "what now?"). This session state includes user-driven information like the currently selected character, the active navigation mode, and whether the application is locked.

Our approach is a hybrid model that uses a centralized, global store for all session logic, supported by localized states for component-specific UI concerns.

#### **6.1. Primary Pattern: The Global `editor` Store (Pattern 5)**

The entire editor interface acts as one large, composite application. Therefore, we will instantiate a single global store using `Alpine.store('editor', ...)`. This store will be the central nervous system for all interactive logic, preventing state inconsistencies and creating a single, predictable source of truth for the session.

**Global Store (`editor`) Structure:**

| Property / Method               | Type             | Initial Value | Description                                                                                                                                |
| :------------------------------ | :--------------- | :------------ | :----------------------------------------------------------------------------------------------------------------------------------------- |
| `isAppLocked`                   | `Boolean`        | `false`       | The master switch for the app. If `true`, all editing inputs are disabled. This is toggled by the Lock/Unlock button in the footer.        |
| `navigationMode`                | `String`         | `'character'` | The Mutex (Pattern 3) that governs navigation. Holds either `'character'` or `'word'`. Determines the behavior of arrow and spacebar keys. |
| `activeCharId`                  | `String \| null` | `null`        | The `data-global-dia-idx` of the currently focused character. This is the primary key for the editor's focus state.                        |
| `activeWordId`                  | `String \| null` | `null`        | The `data-wd-idx` of the word containing the active character. Used to apply the `.word-focus` visual style.                               |
| `currentCharIndex`              | `Number`         | `0`           | The 1-based index of the `activeCharId` among all interactive characters. Used for the "Progress" display in the footer.                   |
| `totalChars`                    | `Number`         | `0`           | The total count of interactive characters, calculated on initialization. Used for the "Progress" display.                                  |
| `init()`                        | `Function`       | -             | An initialization method to be run once. It will scan the DOM for all interactive spans, populate `totalChars`, and set the initial focus. |
| `toggleAppLock()`               | `Function`       | -             | Toggles the `isAppLocked` state.                                                                                                           |
| `setNavigationMode()`           | `Function`       | -             | Accepts `'character'` or `'word'` and updates the `navigationMode` state.                                                                  |
| `setActiveChar()`               | `Function`       | -             | The core focus-updater. Takes a character ID, then updates `activeCharId`, `activeWordId`, and `currentCharIndex` accordingly.             |
| `setDiacritic()`                | `Function`       | -             | Accepts a diacritic value (e.g., `'َ'`). Finds the element matching `activeCharId` and updates its text content.                           |
| `nextChar()`, `prevChar()` etc. | `Function`       | -             | Helper methods that contain the DOM-querying logic for navigation, which then call `setActiveChar()`.                                      |

#### **6.2. Supporting Pattern: Local Component State (Pattern 1)**

To keep the global store clean and focused on session logic, we will use localized `x-data` scopes for UI state that is purely cosmetic or encapsulated within a single component.

1.  **Sidebar Visibility (`sidebarOpen`):** The state of the collapsible sidebar (`open` or `closed`) has no impact on the editing logic. It's a user preference for their workspace layout and is perfectly managed by a local `x-data="{ sidebarOpen: true }"` on a parent `<div>`.

2.  **Numpad `Ctrl` Key (`isCtrlActive`):** The state of the `Ctrl` toggle on the Numpad palette only affects the Numpad's own display (showing "Shadda" variants). The global store doesn't need to know about this intermediate state; it only receives the final diacritic value from the `setDiacritic()` call. This is a perfect example of encapsulation, managed by a local `x-data="{ isCtrlActive: false }"` on the Numpad component.

#### **6.3. Reactive Behavior in Action: A User's Journey**

This architecture creates a powerful, reactive data flow. Consider this sequence of events when the user presses the `→` (Right Arrow) key:

1.  **Event:** A `keydown` event is triggered on the `window`.
2.  **Listener:** A global keyboard listener, part of our main Alpine component, catches the event.
3.  **Condition:** The listener first checks the global state: `if ($store.editor.isAppLocked) return;`.
4.  **Logic:** The listener then checks `$store.editor.navigationMode`. Based on the mode (`'character'` or `'word'`), it calls the appropriate navigation method (e.g., `nextChar()`). This method finds the current `<span>` using `$store.editor.activeCharId`, queries the DOM for the next interactive sibling, and gets its ID.
5.  **Action:** The navigation method calls the central mutator: `$store.editor.setActiveChar(newCharId)`.
6.  **Store Reaction:** Inside the `setActiveChar` method, the store updates its own properties:
    - `this.activeCharId` is set to `newCharId`.
    - `this.activeWordId` is updated by reading the `data-wd-idx` from the new element.
    - `this.currentCharIndex` is recalculated.
7.  **UI Reaction (The Magic of Reactivity):**
    - **Main Editor:** The `<span>` elements, which have a `:class` binding like `:class="{ 'char-focus': $store.editor.activeCharId === myId }"`, automatically update. The highlight moves to the new character.
    - **Sidebar Inspector:** The "Zoom View", which is bound to `$store.editor.activeCharId`, automatically re-renders to show the new character and its diacritic.
    - **Footer:** The "Progress" text, bound to `$store.editor.currentCharIndex`, instantly updates from `1 / 85` to `2 / 85`.

This entire UI update happens automatically and declaratively, simply by changing the state in one central location. This fulfills our architectural goal of a clean, maintainable, and powerful interactive system.
