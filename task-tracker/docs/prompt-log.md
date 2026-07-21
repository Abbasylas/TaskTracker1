First feature: Search + combined filters
Weak Stories Prompt: give me 3-5 user story tasks to implement Search + combined filters

Results: ChatGPT gave 5 unspecific stories, it did not mention search by assignee which was one of the important features, It did not mention code logic, case sensitivity or supporting matches. It also did not mention response logic.

Generate user stories for the Search + combine filters feature in the Task Tracker folder in the same format and quality as this example.
Example:
Story: As a user, I want to create a task so that I can track work.
Acceptance Criteria:
- Title is required; missing or blank title returns HTTP 422.
- Description is optional.
- A created task appears in the task list with status, priority, and assignee.
Now generate five more stories in the same format.
Constraints:
- Use "User" as the user role.
- Do not mention login, authentication, user accounts, admin roles, notifications, mobile, or real-time updates.
Expected frontend changes: Add a compact filter/search bar above the board. Keep columns visible and preserve empty states.	
Good features to include: Search title/description, combine status + priority, no matches returns 200 with [], invalid filter value returns 422 if backend validates it.
Output format:
Return each story with Story and Acceptance Criteria headings.
The output is found in the user stories file.

Mini-ADR prompt: You are a senior backend developer helping me evaluate lightweight architectures for a learning project.
Context:
I am building a Task Tracker application with a Python/FastAPI backend and a simple web frontend.
Reviewed requirements:
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
Constraints:
- This is a learning project, not production software.
- The backend must use Python, FastAPI, and Pydantic for validation.
- I am using a REST API backend and a separate simple web frontend. 
- Keep the tech stack simple, well-documented, and easy to run locally.
- No authentication or multi-tenancy.
- Do not suggest microservices, Docker, cloud deployment, or production database setup.
Task:
Propose two different lightweight architectures:
- Option A should be the simplest local-storage approach appropriate for a first learning project.
- Option B may use a lightweight local database approach if it improves realism without overcomplicating the project.
For each option, provide:
1. Tech stack and data storage choice
2. Folder structure
3. Data model sketch with Pydantic fields and constraints
4. Three trade-offs compared to the other option
Output format:
Return Option A and Option B in clearly separated sections. Do not choose for me. 

Output B:Pros:

✅ Real database querying (filtering done via SQL)
✅ Persistent storage by default
✅ More realistic backend experience

Cons:

❌ Slightly more complex setup (DB + ORM)
❌ Query building adds learning overhead
❌ Harder to debug compared to plain Python lists

Output A: Trade-offs (vs Option B)

Pros:

✅ Extremely simple to implement and debug
✅ No database knowledge required
✅ Fast iteration (perfect for learning filtering logic)

Cons:

❌ No real querying → filtering done manually in Python
❌ Data resets on restart (unless JSON added)
❌ Not realistic compared to real-world backend systems

I chose output A

Prompt for Cursor AI: 
Context: I am working in the Module 2 Task Tracker repository for an AI-Assisted Coding course.
Current project:
- Backend: Python/FastAPI Task Tracker API.
- Main task fields: id, title, description, status, priority, assignee.
- Status values are exactly: ToDo, InProgress, Done.
- Priority values are exactly: Low, Medium, High.
- The frontend will live in frontend/index.html using vanilla HTML, CSS, and JavaScript.
Module 3 goal:
Build a browser-based Kanban board with three status columns, cards sorted by priority, loading/empty/error/ready states, drag-and-drop that
PATCHes the backend, and a create/edit modal with title trimming and server 422 handling.
Workflow rules:
- Work in small steps.
- Do not rewrite the whole file unless I explicitly ask.
AI-Assisted Coding - Module 3 Prompt Library
- Do not add frameworks, build tools, auth, accounts, real-time sync, or new backend features.
- Treat your answer as a draft. I will inspect, run, test, and refine it.

Ouput: AI mentioned all the files in the project, the languages used as well as the logic used.

Feature 2: Task Comments
Stories prompt: Generate user stories for the Task comments feature in the Task Tracker folder in the same format and quality as this example.

Expected function: Add comment model or task comment list. Support list/add/delete comment behavior with non-blank text validation and not-found handling.

Frontend: Add a comments section in the edit modal or a small task detail area. Show comment count on cards if useful.

Backend: Add comment, reject blank comment, list comments for a task, delete comment, 404 for missing task/comment.



Example:

Story: As a user, I want to create a task so that I can track work.

Acceptance Criteria:

- Title is required; missing or blank title returns HTTP 422.

- Description is optional.

- A created task appears in the task list with status, priority, and assignee.

Now generate five more stories in the same format.

Constraints:

- Use "User" as the user role.

- Do not mention login, authentication, user accounts, admin roles, notifications, mobile, or real-time updates.

Output format:

Return each story with Story and Acceptance Criteria headings.

mini-ADR Prompt: You are a senior backend developer helping me evaluate lightweight architectures for a learning project.

Context:

I am building a Task Tracker application with a Python/FastAPI backend and a simple web frontend.

Reviewed requirements:

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

Constraints:

- This is a learning project, not production software.

- The backend must use Python, FastAPI, and Pydantic for validation.

- I want a REST API backend and a separate simple web frontend.

- Keep the tech stack simple, well-documented, and easy to run locally.

- No authentication or multi-tenancy.

- Do not suggest microservices, Docker, cloud deployment, or production database setup.

Task:

Propose two different lightweight architectures:

- Option A should be the simplest local-storage approach appropriate for a first learning project.

- Option B may use a lightweight local database approach if it improves realism without overcomplicating the project.

For each option, provide:

1. Tech stack and data storage choice

2. Folder structure

3. Data model sketch with Pydantic fields and constraints

4. Three trade-offs compared to the other option

Output format:

Return Option A and Option B in clearly separated sections. Do not choose for me.

Refactor Prompt: 
Create an 8-item behavior contract for my two newly added Module 3 features before refactoring: the search/filter bar and task comments.

Behaviors that must be covered:
- Search matches task titles and descriptions case-insensitively.
- Multiple filters work together using AND logic, including status, priority, assignee, tag, and due date.
- Clearing the search and filters restores the complete Kanban board.
- No-match and backend-error states are displayed correctly.
- A valid comment can be added and appears immediately with its creation timestamp.
- Empty or whitespace-only comments are rejected with validation feedback.
- Comments load in oldest-first order, remain associated with the correct task, and tasks without comments show an empty state.
- Deleting a comment updates the comment list and count, while deletion errors show the server message and preserve or restore the comment.

Output format:
Return a table with these columns:
ID, Behavior, How to check manually, Pass/Fail notes.

Use exactly 8 items.
Do not write, refactor, or change any code.