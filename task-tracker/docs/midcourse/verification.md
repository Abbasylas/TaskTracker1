# Mid-Course Verification and Break-Test Evidence

**Project:** Task Tracker  
**Features verified:** Task comments; search and combined filters  
**Verification date:** 25 July 2026  
**Overall result:** **PASS**

## 1. Verification Scope

This verification covers the two mid-course features:

1. Adding, listing, validating, counting, and deleting task comments.
2. Searching task titles and descriptions and combining search with status, priority, assignee, tag, and due-date filters.

The dedicated break-test suite is located in:

```text
Mid_project_test.py/test_mid_project.py
```

It contains exactly six tests: three comment tests and three search/filter tests. The tests use temporary JSON storage and do not modify `data/tasks.json`.

## 2. Dedicated Break-Test Cases

| ID | Test | Behaviour verified | Expected result | Result |
|---|---|---|---|---|
| BT-01 | `test_comments_can_be_added_and_listed` | A valid comment is created and immediately returned when comments are listed. | POST returns 201; GET returns 200 and contains the created comment. | PASS |
| BT-02 | `test_blank_comment_is_rejected` | A whitespace-only comment is invalid. | API returns HTTP 422. | PASS |
| BT-03 | `test_comment_count_updates_after_add` | Adding a comment updates the task's `comment_count`. | Task response reports `comment_count` equal to 1. | PASS |
| BT-04 | `test_search_matches_title_and_description` | Search checks both title and description without case sensitivity. | Searching for `API` returns both matching tasks. | PASS |
| BT-05 | `test_combined_filters_return_only_the_full_match` | Multiple filters use AND logic and text filters are case-insensitive. | Only the task satisfying every supplied filter is returned. | PASS |
| BT-06 | `test_invalid_filter_value_returns_422` | Unsupported enum filter values are rejected. | `status=Blocked` returns HTTP 422. | PASS |

### Execution command

```cmd
py -m pytest -q Mid_project_test.py
```

### Execution evidence

```text
......                                                                   [100%]
6 passed in 0.06s
```

## 3. Deliberate Break Test 1 — Description Search Removed

### Change introduced

The description-search condition was temporarily removed from `app/services.py`, leaving search to check only task titles.

Correct implementation:

```python
if cleaned_search in task.title.casefold() \
        or cleaned_search in (task.description or "").casefold()
```

Temporarily broken implementation:

```python
if cleaned_search in task.title.casefold()
```

### Targeted test

```cmd
py -m pytest -q tests/test_search_filters.py::test_search_matches_title_or_description_case_insensitively
```

### Failure evidence

```text
FAILED tests/test_search_filters.py::test_search_matches_title_or_description_case_insensitively
AssertionError: assert {'API Bug'} == {'API Bug', 'Update docs'}
1 failed
```

### Interpretation

The test failed because `Update docs` matched the search term only through its description. This confirms that the test detects removal of description searching.

### Restoration result

The description condition was restored. The targeted test and all related search/filter tests passed afterward.

## 4. Deliberate Break Test 2 — Missing-Task Comment Deletion Check Removed

### Change introduced

The missing-task check was temporarily removed from the comment deletion endpoint in `app/main.py`.

Correct implementation:

```python
if result is None:
    raise HTTPException(status_code=404, detail="Task not found")
```

Temporarily broken implementation:

```python
# Missing-task check removed for the break test.
```

### Targeted test

```cmd
py -m pytest -q tests/test_comments.py::test_delete_comment_from_missing_task_returns_404
```

### Failure evidence

```text
FAILED tests/test_comments.py::test_delete_comment_from_missing_task_returns_404
assert 204 == 404
1 failed
```

### Interpretation

Without the missing-task check, deleting a comment from a nonexistent task incorrectly returned HTTP 204. This confirms that the test detects the missing 404 error handling.

### Restoration result

The missing-task check was restored. The targeted test and all related comment tests passed afterward.

## 5. Full Regression-Test Evidence

### Execution command

```cmd
py -m pytest -q
```

### Final result

```text
..................................................                       [100%]
50 passed in 0.28s
```

The supplied project also records the following successful checks in `TEST_RESULTS.txt`:

```text
Validation completed successfully.

Full test suite:
50 passed

Requested mid-project break tests:
6 passed (3 task-comment tests + 3 search/filter tests)

Additional checks:
- Frontend JavaScript syntax check passed.
- Seed data JSON validation passed.
- Python application modules compiled successfully.
```

## 6. Behaviour Contract

| ID | Behaviour | Manual verification method | Pass condition |
|---|---|---|---|
| BC-01 | Search matches task titles and descriptions without case sensitivity. | Create one task with a unique word in its title and another with the same word only in its description. Search using different capitalization. | Both matching tasks appear and unrelated tasks do not. |
| BC-02 | Multiple filters work together using AND logic. | Apply status, priority, assignee, tag, and due-date filters that fully match only one task. | No partially matching task appears. |
| BC-03 | Clearing search and filters restores the complete Kanban board. | Apply search and filters, then clear or reset them. | All original cards, columns, and counts return without reloading. |
| BC-04 | Search and filters handle no matches and backend errors. | Search for nonexistent text, then stop the backend and attempt another request. | A clear empty state and a clear backend-error state are displayed without breaking the board. |
| BC-05 | A valid comment can be added and appears immediately. | Open an existing task, enter valid comment text, and submit. | The comment appears with its text and creation timestamp. |
| BC-06 | Blank comments are rejected. | Submit an empty comment and a whitespace-only comment. | Neither comment is created and validation feedback is shown. |
| BC-07 | Comments remain associated with the correct task. | Add different comments to two tasks and reopen each task. Also open a task with no comments. | Each task shows only its own comments in oldest-first order; a task with no comments shows an empty state. |
| BC-08 | Comment deletion and error handling work correctly. | Delete an existing comment, then attempt to delete a nonexistent comment or delete while the backend is unavailable. | The existing comment disappears and its count decreases; failures show an appropriate error without corrupting the task. |

## 7. Verification Conclusion

The dedicated six-test break suite passes, both deliberate faults are detected by the relevant automated tests, and the restored implementation passes all 50 regression tests. The comment and search/filter features therefore meet the tested acceptance criteria.
