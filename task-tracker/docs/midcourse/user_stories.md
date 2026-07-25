Feature 1: Search + Combined Filters

User Story 1: Search Tasks by Title & Description
As a user, I want to search tasks by text in the title or description so that I can quickly find relevant tasks.

Acceptance Criteria:

GET /tasks?search=keyword
Matches title OR description
Case-insensitive
Supports partial matches
Returns 200 OK with filtered results

User Story 2: Filter Tasks by Status and Priority
As a user, I want to filter tasks by status and priority so that I can focus on specific categories of work.

Acceptance Criteria:

GET /tasks?status=InProgress&priority=High
Valid status: ToDo, InProgress, Done
Valid priority: Low, Medium, High
Uses AND logic (both must match)
Returns 200 OK with filtered results

User Story 3: Combine Search with Multiple Filters
As a user, I want to combine search with filters (status, priority, assignee, etc.) so that I can narrow down tasks precisely.

Acceptance Criteria:

Example: GET /tasks?search=api&status=ToDo&priority=High&assignee=John
Uses AND logic across all parameters
Supports optional filters: assignee, tag, due_date (if implemented)
Returns only matching tasks

User Story 4: Handle No Matching Results
As a user, I want the API to return an empty list when no tasks match so that I can clearly see that nothing fits my criteria.

Acceptance Criteria:

No matches returns []
Response status is 200 OK
No error is thrown

User Story 5: Validate Query Parameters
As a developer, I want invalid filter values to be rejected so that the API remains reliable and predictable.

Acceptance Criteria:

Invalid values return 422 Unprocessable Entity
Example: status=Started, priority=Urgent
Validation handled via enums or schema validation
Error message clearly identifies invalid fields
User Story 1: Search Tasks by Title & Description
As a user, I want to search tasks by text in the title or description so that I can quickly find relevant tasks.

Acceptance Criteria:

GET /tasks?search=keyword
Matches title OR description
Case-insensitive
Supports partial matches
Returns 200 OK with filtered results
Correction: I emphasized supporting partial matches 

User Story 2: Filter Tasks by Status and Priority
As a user, I want to filter tasks by status and priority so that I can focus on specific categories of work.

Acceptance Criteria:

GET /tasks?status=InProgress&priority=High
Valid status: ToDo, InProgress, Done
Valid priority: Low, Medium, High
Uses AND logic (both must match)
Returns 200 OK with filtered results
Correction: Added matching uses AND logic which ChatGPT missed

User Story 3: Combine Search with Multiple Filters
As a user, I want to combine search with filters (status, priority, assignee, etc.) so that I can narrow down tasks precisely.

Acceptance Criteria:

Example: GET /tasks?search=api&status=ToDo&priority=High&assignee=John
Uses AND logic across all parameters
Supports optional filters: assignee, tag, due_date (if implemented)
Returns only matching tasks
Correction: Added assignee to the optional filters supported

User Story 4: Handle No Matching Results
As a user, I want the API to return an empty list when no tasks match so that I can clearly see that nothing fits my criteria.

Acceptance Criteria:

No matches returns []
Response status is 200 OK
No error is thrown

User Story 5: Validate Query Parameters
As a developer, I want invalid filter values to be rejected so that the API remains reliable and predictable.

Acceptance Criteria:

Invalid values return 422 Unprocessable Entity
Example: status=Started, priority=Urgent
Validation handled via enums or schema validation
Error message clearly identifies invalid fields
Correction: Emphasized clearly displaying invalid fields in error messages.

Feature 2: Adding task comments

Story: As a User, I want to add a comment to a task so that I can record notes or updates.
Acceptance Criteria:

Comment text is required; missing or blank text returns HTTP 422 (Updated).
A comment is successfully added to the specified task when valid text is provided.
Adding a comment to a non-existing task returns HTTP 404.
The newly added comment appears in the task’s comment list immediately after creation.

Story: As a User, I want to view all comments for a task so that I can understand its history and context.
Acceptance Criteria:

The system returns a list of comments associated with a given task ID (Updated).
Each comment includes its text and creation timestamp.
Requesting comments for a non-existing task returns HTTP 404.
If a task has no comments, an empty list is returned.

Story: As a User, I want to delete a comment so that I can remove incorrect or unnecessary information.
Acceptance Criteria:

A comment can be deleted using its unique identifier (Updated).
Deleting a non-existing comment returns HTTP 404.
Deleting a comment from a non-existing task returns HTTP 404.
Once deleted, the comment no longer appears in the task’s comment list.

Story: As a User, I want to see the number of comments on a task so that I can quickly gauge its activity.
Acceptance Criteria:

Each task displays a comment count based on its associated comments (Updated).
The comment count updates correctly after adding or deleting a comment.
Tasks with no comments display a count of zero.
The comment count is visible in the task list or card view.

Story: As a User, I want to view and manage comments in the task details area so that I can interact with them easily.
Acceptance Criteria:

A comments section is available in the task edit modal or detail area (Updated).
The section lists all comments in chronological order.
Users can add a new comment from this section.
Users can delete existing comments from this section.
The UI reflects changes (add/delete) without requiring a full page refresh.