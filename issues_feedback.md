# Task Tracking & Developer Feedback


## Issue #TST-100: Application runs in Debug Mode

*   **Reporter:** BinkCodes 
*   **Priority:** High (Security)
*   **Status:** OPEN
*   **Description:** The Flask application is started with `debug=True`. This exposes a security risk in a production-like environment, as it can allow arbitrary code execution.
*   **Steps to Reproduce:** Observe the console output when starting the app: `* Debug mode: on`.
*   **Expected Result:** Debug mode should be disabled for any build that is not for development.
*   **Feedback for Developers:** Please change `app.run(debug=True)` to `app.run(debug=False)` or, better yet, use an environment variable to control the debug setting.

---

