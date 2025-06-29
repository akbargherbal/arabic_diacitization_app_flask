Excellent. Based on my comprehensive review of the project's architecture, UI, and detailed user flow, I have a clear recommendation.

This application is a perfect example of a system that requires a **hybrid state management strategy**, with a clear distinction between data state and UI session state.

The overarching pattern is **Pattern 5: Complex, Composite & Extended States**, which should be managed by a global `Alpine.store()`. This global store will be supported by localized instances of **Pattern 1 (Simple & Independent)** and **Pattern 3 (Exclusive & Competing)**.

Here is a detailed breakdown of the analysis and the proposed implementation strategy.

### Overall Recommendation: A Global Store for Session State

The "Interactive Arabic Diacritization Engine" is a single, cohesive unit of functionality. Multiple, disparate components (the footer, the main editor, the sidebar inspector) all need to react to a shared set of "session state" variables. A global store is the ideal solution to manage this complexity without resorting to prop-drilling or messy event bus implementations.

This approach honors the project's core philosophy of **"HTML as the Source of Truth."** The server-generated HTML provides the _initial, immutable data state_ (the characters, their IDs, their correct diacritics). The `Alpine.store` will manage the _transient UI session state_ (what's currently active, what mode we're in, is the app locked?).

I propose creating a global store named `editor`.

#### Proposed `Alpine.store('editor', ...)` Structure:

This store will act as the "smart home hub" for the entire application, centralizing the control logic.

| Property              | Type            | State Pattern Applied    | Explanation                                                                                                                     | Components Using This State           |
| :-------------------- | :-------------- | :----------------------- | :------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------ |
| `isAppLocked`         | Boolean         | 5. Composite (Global)    | The master switch for the entire app. When `true`, all keyboard/mouse inputs are disabled.                                      | Footer (toggle), Main Editor, Sidebar |
| `navigationMode`      | String          | 3. Exclusive & Competing | Holds either `'character'` or `'word'`. This single variable dictates the behavior of arrow keys and the spacebar.              | Footer (toggle), Main Editor (keys)   |
| `activeCharId`        | String / `null` | 5. Composite (Global)    | The unique ID of the currently focused character `<span>`. This is the "you are here" pointer for the entire application.       | Main Editor, Sidebar Inspector        |
| `activeWordId`        | String / `null` | 5. Composite (Global)    | The unique ID of the word containing the active character. Used to apply the `.word-focus` class.                               | Main Editor                           |
| `totalChars`          | Number          | 5. Composite (Global)    | The total number of interactive characters, calculated on initialization.                                                       | Footer (progress display)             |
| `currentCharIndex`    | Number          | 5. Composite (Global)    | The 1-based index of the active character, derived from `activeCharId`.                                                         | Footer (progress display)             |
| **Methods**           | **Function**    | **(Logic)**              | **Encapsulated logic for state transitions.**                                                                                   | **(Event Handlers)**                  |
| `toggleAppLock()`     | Function        | -                        | Flips the `isAppLocked` boolean.                                                                                                | Footer (toggle button)                |
| `setNavigationMode()` | Function        | -                        | Sets the `navigationMode` to the chosen value.                                                                                  | Footer (mode switcher)                |
| `setActiveChar()`     | Function        | -                        | Updates `activeCharId`, `activeWordId`, and `currentCharIndex`. This is the central method called by all navigation events.     | Main Editor (key/mouse events)        |
| `setDiacritic()`      | Function        | -                        | The action triggered by the Numpad. It takes a diacritic value, finds the element with `activeCharId`, and updates its content. | Sidebar (Numpad)                      |

### Supporting Patterns in Use

While the global store is the central nervous system, simpler patterns are essential for keeping individual components clean and self-contained.

#### Pattern 1: Simple & Independent State (`x-data`)

This is the default choice for UI state that is entirely local to one component and doesn't need to be shared.

1.  **Sidebar Visibility:**

    - **State:** `sidebarOpen: true`
    - **Justification:** Whether the sidebar is open or closed has no bearing on the `navigationMode` or `isAppLocked` state. It is a purely cosmetic preference for the user's workspace.
    - **Implementation:** A simple `x-data="{ sidebarOpen: true }"` on a parent container, as shown in the mockup.

2.  **Numpad `Ctrl` Toggle:**
    - **State:** `isCtrlActive: false`
    - **Justification:** The `Ctrl` key's state is only relevant to the Numpad palette itself. It determines which set of diacritic symbols and names to display on the buttons. The main editor doesn't need to know or care about this; it only cares about the final diacritic value sent by the `setDiacritic()` method.
    - **Implementation:** A local `x-data="{ isCtrlActive: false }"` scoped to the Numpad `div`.

#### Pattern 3: Exclusive & Competing States (Mutex)

This pattern is implemented _within_ the global store.

1.  **Navigation Mode (`navigationMode`):**
    - **Justification:** The application can only be in **"Character Flow Mode"** OR **"Word Focus Mode"**. They are mutually exclusive. Selecting one must de-select the other.
    - **Implementation:** A single string variable (`$store.editor.navigationMode`) in the global store perfectly models this. The UI buttons simply call a method like `$store.editor.setNavigationMode('word')`, and all components that depend on this state (like the keyboard event listeners) will react accordingly.

The application does **not** require a **Sequential / FSM (Pattern 4)** approach for its primary navigation, as the user is free to jump between characters and words at will, rather than following a strict, unskippable sequence like a checkout flow.

By adopting this hybrid strategy, the application remains true to its architectural principles while providing a robust, centralized, and highly maintainable way to manage the complexities of its interactive session state.
