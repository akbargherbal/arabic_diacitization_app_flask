### 1. Simple & Independent States

**Analogy:** Power Strip, Desk Lamp with Dimmer, Filing Cabinet. Each control is self-contained.

**Web Development Context:** **Local Component State.**

This is the most common and fundamental type of state. It's state that "belongs" to a single component and doesn't need to be shared with others. In frameworks like React, this is managed with the `useState` hook.

**Example 1: A "Show/Hide" Password Field**

*   **Component:** `PasswordInput.js`
*   **State:** A single boolean, `const [isPasswordVisible, setIsPasswordVisible] = useState(false);`
*   **Behavior:** A toggle button inside the component flips this boolean. The component's internal logic uses this state to change the input's `type` attribute from `"password"` to `"text"`.
*   **Independence:** The visibility of this password field has no effect on any other part of the application. It's entirely local.

**Example 2: An Accordion or FAQ Item**

*   **Component:** `AccordionItem.js`
*   **State:** A boolean, `const [isOpen, setIsOpen] = useState(false);`
*   **Behavior:** Clicking the item's header toggles the `isOpen` state. The component uses this state to conditionally render the answer/content panel below the header.
*   **Independence:** One FAQ item being open or closed is independent of the others (unless they are designed as a group, which becomes a different pattern).

### 2. Dependent States (Master / Sub-System)

**Analogy:** Car's Ignition, Building Water Main. A master state enables or disables a group of sub-features.

**Web Development Context:** **Conditional Rendering & Feature Flags.**

This pattern governs whether entire sections of the UI are rendered or if features are available based on a single, often global, condition.

**Example 1: User Authentication**

*   **Master State:** `user: { isLoggedIn: true, name: 'Alice' }` (often stored in a global context or store).
*   **Behavior:**
    *   If `isLoggedIn` is `false`, the entire application shows only the `<LoginPage />` component.
    *   If `isLoggedIn` is `true`, the application renders the main `<Dashboard />`, `<ProfilePage />`, etc. The login state is the "master switch" that enables the rest of the app's UI. The Profile page is a "sub-system" dependent on the "ignition" of a successful login.

**Example 2: A "Settings" Checkbox**

*   **Component:** A settings panel.
*   **Master State:** A boolean, `const [enableAdvancedMode, setEnableAdvancedMode] = useState(false);`
*   **Behavior:** A form has basic fields, but there's a checkbox for "Enable Advanced Options". When this checkbox is ticked (`enableAdvancedMode` becomes `true`), a whole new section of the form with more complex inputs (`<AdvancedOptions />`) becomes visible. This section is a "sub-system" dependent on the master checkbox.

### 3. Exclusive & Competing States (Mutex)

**Analogy:** Car Gear Shifter, VCR Buttons, Shower Diverter. Only one option from a group can be active.

**Web Development Context:** **Tabbed Interfaces, Radio Buttons, and Filter Groups.**

This pattern is used anytime you have a set of choices where selecting one must automatically de-select the others.

**Example 1: A Tabbed Component**

*   **Component:** `Tabs.js`
*   **State:** A string or number representing the active tab, `const [activeTab, setActiveTab] = useState('profile');`
*   **Behavior:** The component displays three tab buttons: "Profile", "Settings", and "Billing". When a user clicks "Settings", the `setActiveTab('settings')` function is called. The component's rendering logic does two things:
    1.  It applies an "active" CSS class to the "Settings" button and removes it from all others.
    2.  It displays the `<SettingsPanel />` and hides the others.
*   **Exclusivity:** The state can only hold one value, ensuring only one tab and panel are active at once.

**Example 2: Sorting/Filtering Controls**

*   **Component:** An e-commerce product list.
*   **State:** `const [sortBy, setSortBy] = useState('price_asc');`
*   **Behavior:** The user sees buttons for "Sort by Price (Low to High)", "Sort by Price (High to Low)", and "Sort by Popularity". Clicking one updates the `sortBy` state to a single, exclusive value (`'price_asc'`, `'price_desc'`, `'popularity'`), triggering a re-fetch or re-sort of the product data.

### 4. Sequential & Process-Based States (Finite State Machines - FSM)

**Analogy:** Washing Machine, ATM Transaction, Traffic Light. A process with a strict, unskippable order of steps.

**Web Development Context:** **Multi-Step Forms, Wizards, and API Request Lifecycles.**

FSMs are perfect for managing any process that has a defined lifecycle, preventing invalid states and managing side effects at each stage.

**Example 1: A Multi-Step Checkout Flow**

*   **Component:** `CheckoutWizard.js`
*   **States:** `shipping` -> `payment` -> `confirm` -> `success`
*   **Behavior:** The component's state is `const [step, setStep] = useState('shipping');`.
    *   When on the `shipping` step, it displays the shipping form. The "Next" button is disabled until the form is valid.
    *   On a successful form submission, the state transitions: `setStep('payment')`. The component now renders the payment form.
    *   It's impossible for the user to see the payment form (`payment` state) before completing the shipping form (`shipping` state).

**Example 2: Handling an API Request**

*   **States:** `idle` -> `loading` -> `success` | `error`
*   **Behavior:** A component that fetches data starts in an `idle` state.
    *   When a "Fetch" button is clicked, it transitions to the `loading` state. In this state, it shows a spinner and disables the button.
    *   If the API call returns successfully, it transitions to `success` and displays the data.
    *   If the API call fails, it transitions to `error` and displays an error message.
*   **Robustness:** This FSM prevents bugs like the user clicking "Fetch" again while a request is already `loading`.

### 5. Complex, Composite & Extended States

**Analogy:** Smartphone, Smart Home Hub. A single large state object with diverse data types that drives the entire UI.

**Web Development Context:** **Global Application State.**

This is the "big picture" state for an entire application, typically managed by a dedicated state management library like **Redux, Zustand, Vuex, or Pinia**.

**Example: A Social Media Dashboard**

*   **State Store:** `globalStore.js`
*   **State Object:**
    ```javascript
    {
      currentUser: { id: 'u1', name: 'Akbar', avatarUrl: '...' }, // Object
      notifications: {
        messages: 3, // Number
        friendRequests: 1 // Number
      },
      feed: {
        posts: [ { id: 'p1', ... }, { id: 'p2', ... } ], // Array of objects
        status: 'success' // String (FSM state for the feed itself)
      },
      currentTheme: 'dark', // String
      isMobileMenuOpen: false // Boolean
    }
    ```
*   **Behavior:** Different components subscribe to different "slices" of this global state object:
    *   `<Navbar />` uses `currentUser.name` and `isMobileMenuOpen`.
    *   `<NotificationBell />` uses `notifications.messages` to display a badge.
    *   `<Feed />` uses `feed.posts` to render the list and `feed.status` to show a loading spinner or error.
    *   The root `App` component uses `currentTheme` to apply a CSS class to the `<body>` tag.
*   **Composition:** The entire user experience is a composition derived from this single, complex state object.