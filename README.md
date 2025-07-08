# arabic_diacitization_app_flask

Arabic Diacritization Editing App using Flask

## Expected Behavior

### Phase 1: Initial Page Load

When the application first loads, it should automatically initialize itself and focus on the first interactive character.

**✅ Expected Visual Behavior:**

- The first Arabic letter of the verse has a blue underline (`.char-focus`).
- The word containing that first letter has a semi-transparent grey highlight (`.word-focus`).
- The background of the main editing area is light blue (`bg-sky-200`), indicating the app is active.

**✅ Expected Console Log Trace:**
You will see a sequence of initialization logs as Alpine.js starts the component and the store.

```console
%c Alpine.data('diacriticEditor').init()      // The UI component's init function runs first.
%c   -> Setting up watchers...
%c Alpine.store('editor').init()              // The UI init calls the store's init.
%c Alpine.store('editor').setActiveChar()     // The store init finds the first char and sets it as active.
  {id: "0"}
%c $watch('$store.editor.activeCharId')       // The watcher fires because activeCharId changed from null to "0".
  {from: null, to: "0"}
%c $watch('$store.editor.activeWordId')       // The watcher fires because activeWordId changed from null to "0".
  {from: null, to: "0"}
```

---

### Phase 2: Mouse Interaction

When you click on any interactive character.

**✅ Expected Visual Behavior:**

- The blue underline and the grey word highlight instantly move from the previously focused character to the one you just clicked.

**✅ Expected Console Log Trace:**
The trace shows the UI capturing the click and telling the store to update its state, which in turn triggers the reactive watchers.

```console
%c UI Event: clickElement()                   // The UI's @click handler fires.
  {target: span.char}
%c Alpine.store('editor').setActiveChar()     // The handler calls the store's state-setting function.
  {id: "5"} // (The ID of the character you clicked)
%c $watch('$store.editor.activeCharId')       // The watcher reacts to the state change, updating the UI.
  {from: "0", to: "5"}
%c $watch('$store.editor.activeWordId')
  {from: "0", to: "1"} // (Assuming you clicked a character in the next word)
```

---

### Phase 3: Keyboard Interaction

This covers both changing diacritics and navigating.

#### A. Setting a Diacritic

**Event:** With a character focused, you press a number key (e.g., `1` for Fatha).

**✅ Expected Visual Behavior:**

1.  The diacritic of the focused character instantly changes to a Fatha (`َ`).
2.  The focus (blue underline and grey highlight) immediately moves to the _next_ character in the sentence.

**✅ Expected Console Log Trace:**
This is a chain reaction: the key press is dispatched, sets the diacritic, and triggers a navigation action.

```console
%c UI Event: listenToKeyPress()               // The key press is captured.
  {key: "1", ctrl: false}
%c   -> Dispatched to Diacritic Handler
%c Alpine.store('editor').setDiacriticByKey() // The store function is called.
  {key: "1", isCtrl: false}
%c   -> Setting diacritic to 'َ'             // The store logs the change it's making to the DOM.
%c Alpine.store('editor').navigate()          // The function then calls navigate() to auto-advance.
  {direction: "nextChar", mode: "character"}
// ... The logs for setActiveChar() and the watchers will follow.
```

#### B. Navigating with Arrow Keys

**Event:** You press the right arrow key (`→`).

**✅ Expected Visual Behavior:**

- The focus (blue underline and grey highlight) moves to the next character.

**✅ Expected Console Log Trace:**

```console
%c UI Event: listenToKeyPress()               // The key press is captured.
  {key: "ArrowRight", ctrl: false}
%c   -> Dispatched to Navigation Handler
%c Alpine.store('editor').navigate()          // The navigate function is called.
  {direction: "nextChar", mode: "character"}
// NOTE: In a full implementation, this would be followed by setActiveChar() and watcher logs.
```

---

### Phase 4: Global State Change (Locking the App)

**Event:** You double-click the main editing area or press the `Escape` key.

**✅ Expected Visual Behavior:**

- The background turns grey (`bg-slate-300`).
- All keyboard inputs (except `Escape` to unlock) and mouse clicks will no longer have any effect on character focus or diacritics.

**✅ Expected Console Log Trace:**
The store's `toggleAppLock` method is called, and it logs its own state change.

```console
%c Alpine.store('editor').toggleAppLock()     // This could be triggered by listenToKeyPress or a double-click.
%c   -> isAppLocked is now: true
```

When you press `Escape` again to unlock it, you will see the same logs, but the final state will be `false`.

---

### Phase 5: Session Completion (HTMX "Save and Next")

**Event:** You click the "حفظ و التالي (Save and Next)" button.

**✅ Expected Visual Behavior:**

1.  The current Arabic verse is completely replaced with the new verse sent from the server.
2.  The focus is reset to the very first interactive character of this _new_ sentence, with the corresponding blue underline and word highlight.

**✅ Expected Console Log Trace:**
This is the most complex trace and confirms that HTMX and Alpine are working together perfectly.

```console
// 1. HTMX receives the new content and injects its <script> tag.
HTMX response received. Updating Alpine store... // This comes from partials/sentence.html

// 2. That script immediately calls the store's init() method, starting the re-initialization process.
%c Alpine.store('editor').init()
%c Alpine.store('editor').setActiveChar()
  {id: "0"}

// 3. The watchers fire again, applying the focus styles to the new sentence's elements.
%c $watch('$store.editor.activeCharId')
  {from: "15", to: "0"} // (Assuming the old sentence had 16 chars)
%c $watch('$store.editor.activeWordId')
  {from: "4", to: "0"}
```

If your application follows these visual cues and console log patterns, your code is working exactly as designed.

### **Quick List for Flask Testing Prompts**

- **Test Structure:** Structure every test using the **Arrange, Act, Assert (AAA)** pattern. Use descriptive names like `test_login_fails_if_password_is_incorrect`.

- **Database Isolation:** For database tests, use a **separate, temporary database** (e.g., in-memory SQLite) managed by a `pytest` fixture. Never use the development DB.

- **Data Creation:** All necessary test data (e.g., User, Product models) **must be created within the test or its fixtures** using the SQLAlchemy session (e.g., `db.session.add()`, `db.session.commit()`).

- **Endpoint Integration Testing:** Use **Flask's `app.test_client()`** to make in-memory requests to endpoints (e.g., `client.get('/my-route')`). Do not use the `requests` library for internal testing.

- **E2E Browser Testing:**

  - Use the **`live_server` fixture** (from `pytest-flask`) to run the Flask app on a real server for Playwright to access.
  - Prioritize locating elements with a **`data-testid`** attribute. Fall back to user-facing locators (role, label, text).
  - **Strictly avoid** brittle locators based on complex CSS paths or position (`div > span:nth-child(3)`).
  - **Never use `time.sleep()`**. Wait for a definite outcome using Playwright's `expect()` assertions (e.g., `expect(locator).to_be_visible()`).

- **Test Setup (DRY Principle):** Encapsulate all repeated setup (like creating a user, product, or `test_client`) into reusable `pytest` fixtures. Use `yield` for reliable teardown.

---
