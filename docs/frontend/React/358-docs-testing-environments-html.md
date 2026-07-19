url: https://legacy.reactjs.org/docs/testing-environments.html
----

This document goes through the factors that can affect your environment and recommendations for some scenarios.

### [](#test-runners)Test runners

Test runners like [Jest](https://jestjs.io/), [mocha](https://mochajs.org/), [ava](https://github.com/avajs/ava) let you write test suites as regular JavaScript, and run them as part of your development process. Additionally, test suites are run as part of continuous integration.

* Jest is widely compatible with React projects, supporting features like mocked [modules](#mocking-modules) and [timers](#mocking-timers), and [`jsdom`](#mocking-a-rendering-surface) support. **If you use Create React App, [Jest is already included out of the box](https://facebook.github.io/create-react-app/docs/running-tests) with useful defaults.**
* Libraries like [mocha](https://mochajs.org/#running-mocha-in-the-browser) work well in real browser environments, and could help for tests that explicitly need it.
* End-to-end tests are used for testing longer flows across multiple pages, and require a [different setup](#end-to-end-tests-aka-e2e-tests).

### [](#mocking-a-rendering-surface)Mocking a rendering surface

Tests often run in an environment without access to a real rendering surface like a browser. For these environments, we recommend simulating a browser with [`jsdom`](https://github.com/jsdom/jsdom), a lightweight browser implementation that runs inside Node.js.

In most cases, jsdom behaves like a regular browser would, but doesn’t have features like [layout and navigation](https://github.com/jsdom/jsdom#unimplemented-parts-of-the-web-platform). This is still useful for most web-based component tests, since it runs quicker than having to start up a browser for each test. It also runs in the same process as your tests, so you can write code to examine and assert on the rendered DOM.

Just like in a real browser, jsdom lets us model user interactions; tests can dispatch events on DOM nodes, and then observe and assert on the side effects of these actions [(example)](/docs/testing-recipes.html#events).

A large portion of UI tests can be written with the above setup: using Jest as a test runner, rendered to jsdom, with user interactions specified as sequences of browser events, powered by the `act()` helper [(example)](/docs/testing-recipes.html). For example, a lot of React’s own tests are written with this combination.

If you’re writing a library that tests mostly browser-specific behavior, and requires native browser behavior like layout or real inputs, you could use a framework like [mocha.](https://mochajs.org/)

In an environment where you *can’t* simulate a DOM (e.g. testing React Native components on Node.js), you could use [event simulation helpers](/docs/test-utils.html#simulate) to simulate interactions with elements. Alternately, you could use the `fireEvent` helper from [`@testing-library/react-native`](https://testing-library.com/docs/react-native-testing-library/intro).

Frameworks like [Cypress](https://www.cypress.io/), [puppeteer](https://github.com/GoogleChrome/puppeteer) and [webdriver](https://www.seleniumhq.org/projects/webdriver/) are useful for running [end-to-end tests](#end-to-end-tests-aka-e2e-tests).

### [](#mocking-functions)Mocking functions

When writing tests, we’d like to mock out the parts of our code that don’t have equivalents inside our testing environment (e.g. checking `navigator.onLine` status inside Node.js). Tests could also spy on some functions, and observe how other parts of the test interact with them. It is then useful to be able to selectively mock these functions with test-friendly versions.

This is especially useful for data fetching. It is usually preferable to use “fake” data for tests to avoid the slowness and flakiness due to fetching from real API endpoints [(example)](/docs/testing-recipes.html#data-fetching). This helps make the tests predictable. Libraries like [Jest](https://jestjs.io/) and [sinon](https://sinonjs.org/), among others, support mocked functions. For end-to-end tests, mocking network can be more difficult, but you might also want to test the real API endpoints in them anyway.

### [](#mocking-modules)Mocking modules

Some components have dependencies for modules that may not work well in test environments, or aren’t essential to our tests. It can be useful to selectively mock these modules out with suitable replacements [(example)](/docs/testing-recipes.html#mocking-modules).

On Node.js, runners like Jest [support mocking modules](https://jestjs.io/docs/en/manual-mocks). You could also use libraries like [`mock-require`](https://www.npmjs.com/package/mock-require).

### [](#mocking-timers)Mocking timers

Components might be using time-based functions like `setTimeout`, `setInterval`, or `Date.now`. In testing environments, it can be helpful to mock these functions out with replacements that let you manually “advance” time. This is great for making sure your tests run fast! Tests that are dependent on timers would still resolve in order, but quicker [(example)](/docs/testing-recipes.html#timers). Most frameworks, including [Jest](https://jestjs.io/docs/en/timer-mocks), [sinon](https://sinonjs.org/releases/latest/fake-timers) and [lolex](https://github.com/sinonjs/lolex), let you mock timers in your tests.

Sometimes, you may not want to mock timers. For example, maybe you’re testing an animation, or interacting with an endpoint that’s sensitive to timing (like an API rate limiter). Libraries with timer mocks let you enable and disable them on a per test/suite basis, so you can explicitly choose how these tests would run.

### [](#end-to-end-tests-aka-e2e-tests)End-to-end tests

End-to-end tests are useful for testing longer workflows, especially when they’re critical to your business (such as payments or signups). For these tests, you’d probably want to test how a real browser renders the whole app, fetches data from the real API endpoints, uses sessions and cookies, navigates between different links. You might also likely want to make assertions not just on the DOM state, but on the backing data as well (e.g. to verify whether the updates have been persisted to the database).

In this scenario, you would use a framework like [Cypress](https://www.cypress.io/), [Playwright](https://playwright.dev) or a library like [Puppeteer](https://pptr.dev/) so you can navigate between multiple routes and assert on side effects not just in the browser, but potentially on the backend as well.

Is this page useful?[Edit this page](https://github.com/reactjs/reactjs.org/tree/main/content/docs/testing-environments.md)

* Previous article

  [Testing Recipes](/docs/testing-recipes.html)

----
