# SecureNote Manual Test Cases

**Tester:** [BinkCodes]
**Date:** [9/29/25]
**Build:** v0.1

---

## Test Case 1: Adding a Valid Note

*   **Objective:** Verify a user can add a new note with a title and content.
*   **Pre-condition:** App is running at http://127.0.0.1:5000. No notes are present.
*   **Steps:** 
    1. In the "Note Title" field, enter "My First Note".
    2. In the "Note Content" field, enter "This is the content of my first note."
    3. Click the "Add Note" button.
*   **Expected Result:**
    *   A green success message "Note added successfully! is displayed.
    *   The new note "My First Note: This is the content..." appears in the list of notes.
*   **Actual Result:** "My First Note: This is the content of my first note [DELETE]" appeared in the list of notes
*   **Status:** PASS

---
## Test Case 2: Adding a Note with Empty Content

*   **Objective:** Verify the app correctly handles a note with empty content.
*   **Pre-condition:** App is running at http://127.0.0.1:5000.
*   **Steps:** 
    1. In the "Note Title" field, enter "An Empty Note".
    2. Leave the note field empty.
    3. Click the "Add Note" button.
*   **Expected Result:**
    *   A red error message "Note content cannot be empty!" is displayed
    *   The note is not added to the list
*   **Actual Result:** "Note content cannot be empty!" is displayed (no red text)
*   **Status:** PASS
*   **Bug Found?:** Just need to add the color feature.

---   
## Test Case 3: Adding a Note with an Empty Title

*   **Objective:** Verify the app handles a note with an empty title.
*   **Pre-condition:** App is running at http://127.0.0.1:5000.
*   **Steps:**
    1.  Leave the "Note Title" field blank.
    2.  In the "Note Content" field, enter "This note has no title.".
    3.  Click the "Add Note" button.
*   **Expected Result:**
    *   The note is added, but the title should display as "Untitled" or similar.
    *   OR, an error message prompts for a title.
*   **Actual Result:** Note was added, but the title was empty.
*   **Status:** FAIL
*   **Bug Found?:** Yes. The note is added with a completely blank title. This is poor user experience.

---

## Test Case 4: Deleting a Note

*   **Objective:** Verify a user can delete an existing note.
*   **Pre-condition:** At least one note exists in the list.
*   **Steps:**
    1.  Click the "[Delete]" link next to an existing note.
*   **Expected Result:**
    *   A green success message "Note deleted successfully!" is displayed.
    *   The deleted note is removed from the list.
*   **Actual Result:** "Note deleted successfully" flash appeared (not green) 
*   **Status:** PASS
*   **Bug Found?:** Just need to add the color feature.