# Stage 10 PG agentic rescheduling activities and evidence

PG-only stage. Undergraduate students are not required to complete this record. UG-only groups retain this supplied template unchanged as intentionally not applicable; do not fabricate N/A responses. Optional UG help is voluntary and unassessed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage10_pg/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Protect the common Stage 9 SHA and UG Stage 12 pathway.

This is a blank student record. Use actual accessible links and concise evidence; do not invent an agent session, test result or approval. Retain this record's headings when linking equivalent issue/PR evidence.

Group/tutorial: Wednesday 2.30 to 4.30, Group 2
Assessed PG members and roles: Junaid Sayani (junaidSayani1). All roles
Optional UG contributors: None

## A Access baseline and recovery

- Confirmed GitHub Copilot feature/mode, version/environment and teaching-team approval reference: [response]
- Actual account access and tool permissions check: [response]
- Live route or convenor-confirmed equivalent staged interaction: [response]
- Access limitation and tutor resolution if applicable: [response]
- Protected Stage 9 common SHA / recoverable reference: 280884d755caacd8679ddac78b1dab4accaa05ef, the merge of PR #19 on main (https://github.com/DominicRDA-uc/st1-assignment-3/pull/19), on 8 Nov 2026 22:52 (UTC+11). It contains the Stage 9 pure queries (PR #16), service listing and console menu (PRs #17 and #18, which had merged into their parent branches and reached main through PR #19). Stays recoverable in main's Git history.
- Common baseline command / project working directory / actual result: git status --short (empty), git rev-parse HEAD (280884d755caacd8679ddac78b1dab4accaa05ef), then python -m pytest -q in project/ gave 37 passed (Python 3.13.12, pytest 8.3.5).
- Clean branch and preparer / recovery baseline: main at 280884d, working tree clean. Preparer: Junaid Sayani. The Stage 10 branch will be created from this SHA, and main is not to be force-pushed or overwritten.
- Evidence-only later SHA if different / explanation: none so far, the Stage 9 evidence record section H still needs its integrated SHA filled in. So SHA will be different once that comes in but still all versions are recoverable.

## B Tutorial activities

### B1 Rewrite the vague task

“Improve SmartCare appointment scheduling.” Write your bounded goal, requirements, exclusions, constraints, acceptance criteria and Definition of Done: 

Goal: Add an appointment rescheduling function to the existing SmartCare project and nothing else.

Requirements: A known SCHEDULED appointment can move to a valid free time, the same appointment object, ID, patient and practitioner are kept. 
A valid unknown ID raises LookupError and a blank or invalid ID raises ValueError, a clash with another SCHEDULED appointment of the same practitioner at the new time raises ValueError. 
A different practitioner at that time is allowed, CANCELLED and COMPLETED appointments raise ValueError without change.
A valid same time request performs no operation, the new time must be naive and minute precision, a failed request changes nothing, the old slot is free after a move, and lookup and listing show the new time in the same session. 

Exclusions:  notifications/reminders, patient self-service, recurring appointments, billing/payment, authentication redesign, external calendar packages, frameworks/ORM, database/schema redesign, SQLite or any file/restart persistence, unrelated Patient/Practitioner changes and changes to cancellation/history semantics.


Constraints: The domain object protects its own time and state, the service finds the appointment and checks the store for conflicts before changing anything, the store keeps the collections, reuse has_practitioner_conflict with exclude_appointment_id and the existing datetime validation, no cache or separate save step, and keep current names, signatures, exceptions and coding style. 

Acceptance criteria: 
AC-RES-01 valid free time slot move keeps identities and changes the time.
AC-RES-02 Service returns the same object with different time.
AC-RES-03  valid unknown appointment ID raises LookupError. Invalid/blank IDs raise
ValueError under the existing ID contract.
AC-RES-04 Another SCHEDULED appointment for the same practitioner at the
exact new datetime raises ValueError. Does not raise any error if different practitioner.
AC-RES-06-R2 Cancelled and completed appointment rejected.
AC-RES-05 :ookup and listing show the new time, plus self-exclusion and same-time no-op invalid time, old slot reuse and failed-state checks. 

Definition of Done: working code, architecture kept, meaningful positive and negative tests, existing tests still pass, focused and common and full suites passing, reviewed diff with no unrelated changes, AI contribution recorded and the approval explained by a human.

Predicted changed files and human test intentions: 
Files: project/smartcare/domain.py (Appointment.reschedule), project/smartcare/services.py (AppointmentService.reschedule_appointment), new project/tests/test_rescheduling.py or new tests in AppointmentService test file and TestStarter Domain test file..

Test Cases: A valid move changes only the time and returns the same object, unknown ID gives LookupError, invalid/blank ID and invalid datetimes (wrong type, timezone, seconds, microseconds) give ValueError. Same practitioner conflict is rejected/ValueErro, other practitioner at the same time is allowed, moving to its own current time works as a no operation, cancelled and completed targets are rejected even for the same time, a rejected request leaves fields and the stored list unchanged, the old slot can be booked after a move, and lookup and listing show the new time in order

### B2 Judge every proposed plan step

| Proposed step | Accept / Modify / Reject | Requirement evidence and reason |
|---|---|---|
| Redesign database schema | Reject | No requirement needs storage, database or schema work is out of scope and the project keeps data in memory for the session |
| Add notifications | Reject | Notifications are out of scope and none of RES-01 to RES-06 asks for them |
| Introduce calendar library | Reject | External calendar packages are out of scope and the existing datetime validation already covers the time rules |
| Modify Patient | Reject | Rescheduling only changes an appointment's time, unrelated Patient changes are out of scope |
| Add rescheduling | Modify | Accept the goal but bound it, a guarded Appointment.reschedule in the domain, a service method that finds the appointment and checks the conflict with has_practitioner_conflict (excluding itself) before changing anything, and focused tests in tests/test_rescheduling.py |
| Rewrite all tests | Reject | The common tests must stay as they are, only a new test file is added (or new test cases are added in prev file, the old stable code is not interfered) |

### B3 Six proposed changes

| File or action | Expected? | Review concern and evidence needed |
|---|---|---|
| Appointment in project/smartcare/domain.py | Yes | Is the state change bounded and validated, the diff should show one reschedule method that checks the SCHEDULED status, reuses validate_date_time, and leaves ID, patient and practitioner alone, plus tests showing a failed call leaves the time and status unchanged |
| project/smartcare/services.py | Yes | Does it keep the conflict and identity contracts, the diff should use the existing lookup, call has_practitioner_conflict with exclude_appointment_id before changing anything, and return the same object, with tests for conflict, self-exclusion and identity |
| Proposed sqlite_repository.py / schema change | No | No requirement allows storage and SQLite and schema work are out of scope, evidence is the file list in git status and the diff showing no new storage file |
| Patient fields in project/smartcare/domain.py | No | It is unrelated participant behaviour, evidence is a diff showing the Patient class unchanged |
| requirements-dev.txt adds calendar package | No | The dependency is not justified for this scope, evidence is that requirements-dev.txt is unchanged in git diff. |
| Existing appointment assertions weakened | No | Tests must still prove the required result, evidence is a diff of the existing test files showing no changed and no removed assertions. |

### B4 Approval gate

Agent says “All tests pass.” Give at least SIX distinct checks before approval.
1. Run the focused, common-only and full test commands myself from project/ and compare the count.
2. Read git status, git diff, git diff --cached and any new untracked files and compare them with the approved plan and the allowed files.
3. Read the assertions of every new test and check they test exact results, such as the new time and the same object, and not only that something is not None.
4. Check the existing test files for changed or removed assertions.
5. Check that each rejected request leaves the appointment fields and the stored list unchanged, using before and after snapshots.
6. Go through every requirement case one by one, valid move, unknown and blank ID, conflict, other practitioner, cancelled, completed, same-time no-op, old slot reuse and invalid datetimes, and see a test for each
Additional checks if useful: no new dependency, file, dependency, verify no boundary test cases/assertions are left out, and I can explain each changed method and its reason.

### B5 Exit question

Why does increasing AI autonomy increase rather than decrease the importance of software engineering discipline? 
The more an agent can change on its own, the more code can change without a person seeing it, so one wrong step can spread across many files. Plans, scope limits, diff review, independent tests and approval gates are how a person stays in control, and the person is still accountable for what is accepted. AI has made coding boiler plates and repetittive functions super easy and fast, that means to ship at speed, software engineering must also be up to that speed and strictness, by desigining, planning reviewing viewing diff by a human to keep everything in check.

## C Human task specification before AI

- Goal: Add guarded appointment rescheduling to the existing SmartCare project, Appointment.reschedule(new_date_time) and AppointmentService.reschedule_appointment(appointment_id, new_date_time), and nothing else
- Requirements RES-01–06 with RES-05-R2: RES-01 and RES-02, move a known SCHEDULED appointment to a valid free time, keep the same object, ID, patient and practitioner, and return that same object. RES-03, valid unknown ID raises LookupError, blank or invalid ID raises ValueError. RES-04, another SCHEDULED appointment of the same practitioner at the new time raises ValueError, the target itself is excluded and another practitioner is allowed. RES-05-R2, lookup and sorted listing show the new time in the same session. RES-06, CANCELLED and COMPLETED targets raise ValueError without change, even for the same time. A valid same-time request on a SCHEDULED appointment is a no-op, the datetime must be naive with minute precision, any rejection leaves everything unchanged, and a successful move frees the old slot
- Out of scope: notifications, patient self-service, recurring appointments, billing, authentication changes, external calendar packages, frameworks, database or schema work, SQLite and file or restart storage, unrelated Patient or Practitioner changes, changes to cancellation or history.
- Architecture constraints: the domain protects its own time and state and does not know the practitioner's schedule, the service finds the appointment and checks conflicts through SmartCareDataStore before changing anything, the store keeps the collections and has_practitioner_conflict is reused with exclude_appointment_id, queries see the new time with no cache in the same session.
- Acceptance criteria: 
AC-RES-01 valid free time slot move keeps identities and changes the time.
AC-RES-02 Service returns the same object with different time.
AC-RES-03  valid unknown appointment ID raises LookupError. Invalid/blank IDs raise
ValueError under the existing ID contract.
AC-RES-04 Another SCHEDULED appointment for the same practitioner at the
exact new datetime raises ValueError. Does not raise any error if different practitioner.
AC-RES-06-R2 Cancelled and completed appointment rejected.
AC-RES-05 :ookup and listing show the new time, plus self-exclusion and same-time no-op invalid time, old slot reuse and failed-state checks. 

Definition of Done: working code, architecture kept, meaningful positive and negative tests, existing tests still pass, focused and common and full suites passing, reviewed diff with no unrelated changes, AI contribution recorded and the approval explained by a human.

- Issue / PG owner: Junaid Sayani (junaidSayani1), issue link: [response]
- Human expected positive, negative and boundary tests: positive, valid move changes only the time and returns the same object, other practitioner at the same time is allowed, the old slot can be booked after the move, lookup and listing show the new time in order. Negative, unknown ID, blank ID, same practitioner conflict, cancelled target, completed target, each invalid datetime (wrong type, timezone, seconds, microseconds), each failure leaves fields and the stored list unchanged. Boundary, move to its own current time is a no-op and is not a self-conflict, cancelled or completed target with the same time still raises ValueError, appointment moved onto a time that only a CANCELLED appointment of the same practitioner holds is allowed
- Allowed files: project/smartcare/domain.py, project/smartcare/services.py, new project/tests/test_rescheduling.py, the project README PG note and this evidence file.
- Forbidden/unnecessary files and changes: data_store.py or common tests unless justified and reviewed, Patient and Practitioner, queries.py, console.py and main.py, requirements files and any new dependency, any storage or repository file, and any weakened or removed existing assertion.
- Baseline/recovery link: protected common Stage 9 SHA 280884d755caacd8679ddac78b1dab4accaa05ef (PR #19, https://github.com/DominicRDA-uc/st1-assignment-3/pull/19), recorded in section A, with 37 tests passing. The Stage 10 branch is created from it
- Evidence that human analysis preceded agent use: sections B and C were completed by Junaid before any Copilot agent prompt. 


## D Agent plan and approval

Actual plan-only prompt/context and response or confirmed equivalent artefacts: [links]

| Plan step / action | Requirement link | Reason | Expected files | Accept / Modify / Reject | Conditions / evidence |
|---|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] | [response] |

Approved bounded scope / forbidden changes / verification plan: [response]
Human plan approver and approval before edits: [actual evidence]
Tool permissions and any expanded-scope requests / decision: [response]

## E Production diff review

Actual proposal / branch diff / version reviewed: [links]

| File | Change purpose and reason | Requirement / test link | Expected? | Architecture OK? | Decision | Notes / correction |
|---|---|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] | [response] | [response] |

Every changed file inspected, including new/untracked files: [evidence]
Unexpected changes, scope creep, secrets/dependencies/configuration, unrelated cleanup: [response or none with evidence]

## F Separate test review

| Test | Criterion | Actual assertion | Assertion meaningful / adequate? | Agent changed expected behaviour? | Human or agent authorship | Decision and reason |
|---|---|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] | [response] | [response] |

Comparison with original common tests / any proposed weakening: [response]
Independent human checks and corrections: [response]

## G Actual verification

| Requirement / acceptance scenario | Test or demonstration | Meaningful expected result | Actual result | Evidence / version |
|---|---|---|---|---|
| RES-01 / AC-RES-01 successful move | [response] | [response] | [response] | [response] |
| RES-02 same object and participant identities | [response] | [response] | [response] | [response] |
| RES-03 / AC-RES-02 unknown and invalid IDs | [response] | [response] | [response] | [response] |
| RES-04 / AC-RES-03 conflicting practitioner | [response] | [response] | [response] | [response] |
| AC-RES-04 different practitioner allowed | [response] | [response] | [response] | [response] |
| RES-06 / AC-RES-05 cancelled and completed | [response] | [response] | [response] | [response] |
| RES-05-R2 / AC-RES-06-R2 lookup and listing order | [response] | [response] | [response] | [response] |
| Self-exclusion and same-time no-op | [response] | [response] | [response] | [response] |
| Invalid datetime and failed-state snapshots | [response] | [response] | [response] | [response] |
| Successful old-slot reuse | [response] | [response] | [response] | [response] |

| Suite | Command / working directory | Code SHA | Actual count and result | Evidence |
|---|---|---|---|---|
| Focused PG | [response] | [response] | [response] | [response] |
| Common independently | [response] | [response] | [response] | [response] |
| Full cumulative | [response] | [response] | [response] | [response] |
| Integrated retest | [response] | [response] | [response] | [response] |

Failures / diagnosis / corrections and reruns / unresolved concerns: [response]

## H Decisions corrections and independent review

| Significant agent action | Human review and evidence | Accept / Modify / Reject and reason | Manual correction or recovery | Recheck evidence |
|---|---|---|---|---|
| [response] | [response] | [response] | [response] | [response] |

Final proposal decision: [Accepted / Accepted after modification / Rejected]
Evidence supporting decision: [response]
If rejected, how the required feature was subsequently completed and verified: [response or not applicable]
Saved proposal and targeted recovery details if needed: [response or not applicable]
Human explanation of every changed method and limitations: [response]
Another PG / willing UG / tutor reviewer, actual PR/diff review and feedback: [links]
Corrections, recheck and actual approval before integration: [links]
Integrated PG SHA / common protected SHA: [response]
Each assessed PG member's implementation, supervision and test contribution: [response and links]
Optional UG help, acknowledged separately: [response or none]

## I Four reflections

1. Which agent change had the greatest blast radius? [response]
2. Did the plan predict it? [response]
3. What did you reject or manually correct? [response; report honestly if none]
4. What evidence justified final approval? [response]

## J Ten formative questions

1. What is the difference between an AI assistant and an engineering agent? [response]
2. What is the simplified agent loop used in Stage 10? [response]
3. Why should an agent plan be reviewed before repository edits begin? [response]
4. What is meant by the blast radius of a software change? [response]
5. Why is diff review essential for agentic changes? [response]
6. What is a human approval gate? [response]
7. What is test accommodation and why is it dangerous? [response]
8. What is rollback in the context of agentic software engineering? [response]
9. Who remains accountable for accepted agentic changes? [response]
10. What is the Stage 10 engineering rule? [response]

## K Completion and Stage 11 handover

- [ ] Common Stage 9 checkpoint protected; UG pathway unaffected.
- [ ] RES-01–06 and RES-05-R2 implemented in the same project.
- [ ] Domain/service boundaries, current exceptions and coding standard preserved.
- [ ] Positive/negative/boundary cases and failed-state checks verified.
- [ ] Common tests remain valid and independently passing; full suite passes.
- [ ] Plan reviewed before bounded actions; every file and test diff inspected.
- [ ] Actual agent route, decisions, corrections and rechecks recorded honestly.
- [ ] No unrelated features, persistence, dependencies or staff solutions introduced.
- [ ] Another-member or tutor review and integrated retest complete.
- [ ] Tutorial, four reflections, ten formative responses and PG contributions complete.
- [ ] Each PG member can explain their code and supervision.
- [ ] README PG note, actual integrated SHA and limitations recorded.

Unresolved issues / owner / action: [response]
Stage 11 handover references to extension, tests, dependencies and actual AI/review evidence: [response]
Submitted SHA / explanation if later than tested code: [response]
Stage 11 materials are supplied from the beginning. Begin Stage 11 only after Stage 10 has been integrated, verified and recorded. UG follows the protected common code from Stage 9 to Stage 12.
