## Project Manual: Interactive Arabic Diacritization Engine (Definitive Edition)

### 1. Architectural Philosophy: HTML as the Source of Truth

This project is built on a powerful and deliberate architectural pattern that prioritizes server-side logic and minimizes client-side complexity. The core philosophy is that **the server-generated HTML is the primary source of truth for the application's state.**

This approach defines a clear separation of concerns:

1.  **The Server (Python): The Architect.**

    - The Python backend is responsible for all heavy lifting and business logic. It processes the raw text, understands the rules of Arabic diacritization, and calculates the initial state of every character and word.
    - Its final output is not data (like JSON) that the client must interpret and render, but a fully-formed, "smart" HTML document.

2.  **The HTML Document: The Interactive Blueprint.**

    - The HTML is more than just a static view; it is the application's state, made tangible.
    - **`data-*` attributes** are the critical annotations on this blueprint. They embed the necessary state and metadata (unique IDs, correct values, relationships) directly onto the DOM elements they describe. This creates a declarative, self-contained, and easily debuggable representation of the application.

3.  **The Client (Alpine.js): The Skilled Executor.**
    - The role of the front-end JavaScript, powered by Alpine.js, is not to manage a complex, parallel state object. Its job is to **read the state from the HTML blueprint** and bring it to life.
    - Alpine.js acts as a lightweight layer that listens for user events (clicks, key presses) and manipulates the DOM based on the information already present in the `data-*` attributes.

This pattern sidesteps a major source of bugs in web development—state synchronization—and allows us to leverage the strengths of Python for logic and the simplicity of Alpine.js for interactivity.

### 2. Foundational Data (`ar_data.py`)

This file is the "source of truth" and defines the basic linguistic elements for the entire system. Without this, the engine cannot function.

- `list_ar_alpha`: A `list` containing all characters the system recognizes as a valid Arabic letter.
  - **Domain Knowledge:** This list is comprehensive and mission-critical. It correctly includes not just the base letters (ب, ت, ث...), but also all forms of the Hamza (ء, أ, ؤ, إ, ئ), Alif (ا, آ), Taa Marbuta (ة), and Alif Maqsura (ى). Any character _not_ in this list will be treated as non-alphabetic (e.g., punctuation, numbers, Latin characters).
- `set_ar_dia`: A `set` containing all recognized diacritical marks (`َ`, `ً`, `ُ`, `ٌ`, `ِ`, `ٍ`, `ْ`, `ّ`).
  - **Domain Knowledge:** This set defines what the system considers a diacritic. Using a `set` data structure provides a highly efficient O(1) time complexity for checking if a character is a diacritic, a check that is performed frequently during processing.

### 3. The Processing Engine (`utils.py`)

This file contains the core logic for generating the interactive HTML blueprint.

#### `split_arabic_text(word: str)`

- **Purpose:** To correctly tokenize a word by grouping each base character with its subsequent diacritics.
- **Arabic Domain Logic:** This function solves a fundamental challenge of processing Arabic text. In Unicode, diacritics are "combining characters"—separate code points that follow the base letter they modify. A simple string iteration would misinterpret them. For example, the word "عَهْدَ" is stored in memory as `['ع', 'َ', 'ه', 'ْ', 'د', 'َ']`.
- **How it Works:** It uses a carefully crafted regular expression.
  1.  First, it defines two patterns based on `set_ar_dia`:
      - `pattern_non_dia`: `[^{"".join(set_ar_dia)}]` — Matches a single character that is **NOT** a diacritic.
      - `pattern_dia`: `[{"".join(set_ar_dia)}]*` — Matches zero or more characters that **ARE** diacritics.
  2.  It combines them into `f"{pattern_non_dia}{pattern_dia}"`. This master pattern translates to: "Find a sequence that starts with exactly **one non-diacritic character**, followed by **any number of diacritic characters**."
  3.  `re.findall()` then scans the word. For `عَهْدَ`, it finds the list `['عَ', 'هْ', 'دَ']`.
  4.  Finally, it processes this list into tuples of `(base_char, diacritics_string)`, resulting in `[('ع', 'َ'), ('ه', 'ْ'), ('د', 'َ')]`. This structured output is the foundation for all subsequent processing.

#### `create_*_span()` functions

- **Purpose:** These are the template generators that build the "smart" HTML elements.
- **Logic:** They construct HTML `<span>` strings with the `data-*` attributes that form the **contract between the Python backend and the Alpine.js frontend**.
  - `data-global-dia-idx`: The primary key for each interactive character.
  - `data-wd-idx`, `data-char-idx`: Positional metadata.
  - `data-dia`: The initial state value.

#### `char_has_dia(char, dia, mode)`

- **Purpose:** This is the central "gatekeeper" function. It determines whether a character should be made interactive based on the application's operating mode.
- **Logic Breakdown:**
  - `mode == "train"`: Returns `True` only if the character is an Arabic letter (`char in list_ar_alpha`) **AND** it already has a diacritic in the source text (`dia` is a non-empty string). This is for the **training/testing mode**, where the user is only quizzed on characters that are supposed to be diacritized.
  - `mode == "dicr"`: Returns `True` simply if the character is an Arabic letter (`char in list_ar_alpha`). This is for the **free-form diacritization mode**, where the user should be able to add a diacritic to _any_ Arabic letter.

#### `text_to_html_spans(text, mode="dicr")`

This is the main orchestrator that assembles the blueprint.

- **Workflow:**
  1.  **Initialize & Tokenize:** It prepares for processing and breaks down the text into words and then into `(char, diacritics)` pairs using `split_arabic_text`.
  2.  **Classify & Annotate:** For each character, it calls `char_has_dia()` to check if it's an interactive target.
  3.  **Render the Blueprint:**
      - **If `True` (it's a target):** It generates the rich HTML `<span>`s, embedding all necessary state into the `data-*` attributes. This is the element that an Alpine.js component (`x-data`) will later attach to and control.
      - **If `False` (not a target):** It's rendered as a simple, non-interactive `<span>`, preserving all other characters like punctuation and numbers without adding client-side overhead.
  4.  **Return the Blueprint and Server-Side Model:** It returns the complete HTML string, ready for the browser and Alpine.js, along with the server-side data model (`wd_dict`, `char_dict_global`, etc.) which provides a complete metadata map of the processed text.

### 4. Known Limitations & Edge Cases

The system's logic is robust but relies entirely on the definitions in `ar_data.py`.

- **The "Non-Arabic Letter with Diacritic" Case:** If a typo results in a non-Arabic character (e.g., a Latin 'a') being followed by an Arabic diacritic, `split_arabic_text` will correctly group them, e.g., `('a', 'َ')`. However, the `char_has_dia` gatekeeper function will return `False` because `'a'` is not in `list_ar_alpha`. The system will render it as a non-interactive character. This is a reasonable and predictable failure mode that correctly handles the unexpected input without crashing.

### 5. Path Forward: Embracing the HTML-First Architecture

The path forward is to fully commit to this architecture, ensuring a clear division of labor. The Python code handles all linguistic processing and state definition. The front-end, using Alpine.js, consumes this pre-processed HTML blueprint and adds interactivity declaratively, minimizing the need for complex, imperative JavaScript. This creates a more maintainable, readable, and robust application.

### 5. The User Interface (UI) and Workflow

The core of this application is the **"Focused Editor"**, a single-page interface designed for efficient, keyboard-first proofreading of Arabic diacritics. The design balances a minimalist aesthetic with powerful, accessible tools.

#### **5.1. UI Components**

1.  **Main Editing Area:** The central canvas where the diacritized Arabic text is displayed in a large, readable font.
2.  **Collapsible Sidebar:** A command center on the left that can be hidden for a "zen mode." It contains the Character Inspector.
3.  **Character Inspector:** A dynamic panel within the sidebar featuring:
    - **Zoom View:** A large, magnified display of the currently active character and its diacritic.
    - **Info Display:** Shows the English name of the current diacritic (e.g., "Fatha").
    - **Stateful Numpad Palette:** A LTR-oriented numpad grid that serves as the primary mouse-input method and a visual reference for keyboard shortcuts. It has two layers, toggled by a `Ctrl` button, to handle all 14 diacritic combinations.
4.  **Footer Status Bar:** A slim bar at the bottom displaying metadata and global controls.

#### **5.2. The Editor Session Workflow**

**Phase 1: Initialization and Global State**

- **On Load:** The editor loads with the first sentence, and the **first character is automatically focused**. The application is **Active** by default.
- **Global App State (Active/Locked):**
  - A **Lock/Unlock toggle** is present in the footer.
  - In the **Locked** state, all keyboard and mouse inputs related to editing are disabled, and the UI is dimmed to prevent accidental changes. This allows the user to safely pause their work.
  - The default state is **Active**.

**Phase 2: The Core Editing Loop & Navigation Modes**

The user's interaction with the text is governed by one of two navigation modes, selectable from the footer.

- **Mode A: "Character Flow Mode" (Default)**

  - **Goal:** For quick, linear proofreading across the entire sentence.
  - **`Right/Left Arrows`:** Moves focus to the next/previous character sequentially, crossing word boundaries.
  - **`Ctrl + Right/Left Arrows`:** Jumps to the first character of the next/previous word.

- **Mode B: "Word Focus Mode"**
  - **Goal:** For carefully correcting a single word before moving on.
  - **Activation:** The user selects this mode from the footer or clicks on any character with the mouse. The entire word containing the focused character receives a visual highlight (`.word-focus`).
  - **`Spacebar`:** Cycles focus to the _next_ character within the currently highlighted word (loops around).
  - **`Shift + Spacebar`:** Cycles focus to the _previous_ character within the word.
  - **`Ctrl + Right/Left Arrows`:** Jumps the entire word focus to the next/previous word.

**Phase 3: Diacritic Modification & Session Completion**

- **Input:** With a character in focus, the user can modify its diacritic by:
  1.  Using the **Numpad keys (0-9)**.
  2.  Using **`Ctrl` + Numpad keys** for "Shadda" combinations.
  3.  **Clicking** the corresponding button on the Numpad Palette in the sidebar.
- **Completion:** After finishing the sentence, the user clicks the **"حفظ و التالي" (Save and Next)** button. This action saves the current work and loads the next sentence, resetting the editor to the Phase 1 state.

This manual now fully captures the sophisticated yet intuitive workflow we've designed, providing a rock-solid plan for the implementation phase.
