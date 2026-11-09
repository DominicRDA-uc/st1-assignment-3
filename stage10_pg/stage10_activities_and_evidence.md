# Stage 10 PG agentic rescheduling activities and evidence

PG-only stage. Undergraduate students are not required to complete this record. UG-only groups retain this supplied template unchanged as intentionally not applicable; do not fabricate N/A responses. Optional UG help is voluntary and unassessed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage10_pg/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Protect the common Stage 9 SHA and UG Stage 12 pathway.

This is a blank student record. Use actual accessible links and concise evidence; do not invent an agent session, test result or approval. Retain this record's headings when linking equivalent issue/PR evidence.

Group/tutorial: Wednesday 2.30 to 4.30, Group 2
Assessed PG members and roles: Junaid Sayani (junaidSayani1). All roles
Optional UG contributors: None

## A Access baseline and recovery

- Confirmed GitHub Copilot feature/mode, version/environment and teaching-team approval reference: Agentic Mode -> Specifically Plan Mode in Github Copilot - then manuall approval based implementation after final plan.
- Actual account access and tool permissions check: Granted
- Live route or convenor-confirmed equivalent staged interaction: NA
- Access limitation and tutor resolution if applicable: NA
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

- Issue / PG owner: Junaid Sayani (junaidSayani1), issue link: https://github.com/DominicRDA-uc/st1-assignment-3/issues/20
- Human expected positive, negative and boundary tests: positive, valid move changes only the time and returns the same object, other practitioner at the same time is allowed, the old slot can be booked after the move, lookup and listing show the new time in order. Negative, unknown ID, blank ID, same practitioner conflict, cancelled target, completed target, each invalid datetime (wrong type, timezone, seconds, microseconds), each failure leaves fields and the stored list unchanged. Boundary, move to its own current time is a no-op and is not a self-conflict, cancelled or completed target with the same time still raises ValueError, appointment moved onto a time that only a CANCELLED appointment of the same practitioner holds is allowed
- Allowed files: project/smartcare/domain.py, project/smartcare/services.py, new project/tests/test_rescheduling.py, the project README PG note and this evidence file.
- Forbidden/unnecessary files and changes: data_store.py or common tests unless justified and reviewed, Patient and Practitioner, queries.py, console.py and main.py, requirements files and any new dependency, any storage or repository file, and any weakened or removed existing assertion.
- Baseline/recovery link: protected common Stage 9 SHA 280884d755caacd8679ddac78b1dab4accaa05ef (PR #19, https://github.com/DominicRDA-uc/st1-assignment-3/pull/19), recorded in section A, with 37 tests passing. The Stage 10 branch is created from it
- Evidence that human analysis preceded agent use: sections B and C were completed by Junaid before any Copilot agent prompt. 


## D Agent plan and approval

Actual plan-only prompt/context and response or confirmed equivalent artefacts: GitHub Copilot in the IDE, handout section 5 prompt. First plan had four todos without requirement mapping. Revised plan then implemented. 

My Prompt (Plan Mode):
Goal: add appointment rescheduling only to our existing SmartCare.
Use RES-01 to RES-06, with RES-05-R2 session visibility.
Only SCHEDULED targets may move. Preserve the same appointment,
ID and participant objects. Reject unknown IDs, invalid times
and another SCHEDULED same-practitioner/time conflict.
Exclude the target itself; permit a valid same-time no-op.
Failures must not mutate state. Release the old slot on success;
lookup and ordered listing must show the new time in this session.
Use the current domain, service and SmartCareDataStore contracts.
Expected code: domain.py, services.py, tests/test_rescheduling.py.
Reuse the existing conflict helper and datetime validation.
No storage/schema/repository redesign, notifications, billing,
authentication, patient self-service, recurring appointments,
external packages/frameworks or unrelated participant changes.
Keep cancellation/history and all correct common tests unchanged.
Use synthetic data only. No console extension is required.
First inspect the repository and propose a plan ONLY. List each
step, requirement, reason, affected file and verification case.
Do not edit files or execute commands until I approve the plan.
After approval, implement only the approved scope and tests.
Request review before expanding scope. Do not weaken assertions.
Summarise actual changed files, test commands/results and concerns.
Stop for human review; do not commit, merge or deploy autonomously.

COPILOT Plan Response:
Appointment Rescheduling Plan

## Problem and approach

Add in-session appointment rescheduling to SmartCare while preserving its existing domain/service/store architecture. The appointment domain object will guard its own state and time changes using the existing datetime validator. The appointment service will resolve the ID and check the existing practitioner-conflict helper, excluding the target appointment, before making any change. The in-memory store remains unchanged.

## Todos

1. Add guarded `Appointment.reschedule` behavior: validate a naive, minute-precision datetime, permit same-time no-op only for scheduled appointments, and reject cancelled or completed appointments without mutation.
2. Add `AppointmentService.reschedule_appointment`: find the appointment, reject non-scheduled appointments, check conflicts with `exclude_appointment_id`, and return the same appointment after a valid move.
3. Add focused tests for identity preservation, validation and error contracts, conflicts, no-op and failed-state immutability, old-slot reuse, and lookup/list visibility.
4. Run the focused tests and existing project suite, then review the diff for scope.

## Notes and considerations

- Keep changes limited to `project/smartcare/domain.py`, `project/smartcare/services.py`, and a focused test module under `project/tests/`.
- Reuse `validate_date_time` and `SmartCareDataStore.has_practitioner_conflict`; do not add persistence, a save step, caching, UI, or unrelated behavior.
- No pre-existing worktree changes were reported.
- Tests should run from `project` with `python -m pytest`.


My Response (Revising the Plan, still Plan Mode):

The plan is close. Please revise it before I approve any edits.
1. Map each todo to RES-01 to RES-06 with the reason, affected file and verification case.
2. Name the test file project/tests/test_rescheduling.py and list each test case, including each invalid datetime separately, same-time no-op, cancelled and completed with the same time, move onto a time held only by a CANCELLED appointment, different practitioner, failed-state snapshots, old-slot reuse, and lookup and listing order.
3. Do not edit existing tests. Do not commit. Stop for my review after implementing.


Copilot Response:
# Appointment Rescheduling Plan

## Problem and approach

Add in-session appointment rescheduling while preserving the existing domain/service/store architecture. `Appointment.reschedule` will own time/state validation and mutation, using the existing datetime validator. `AppointmentService.reschedule_appointment` will resolve the appointment and check the existing practitioner conflict helper with `exclude_appointment_id` before changing anything. The store collections remain the source of truth; no save step, cache, persistence, or UI change is added.

## RES requirement map

| Requirement | Reason | Affected file | Verification case |
|---|---|---|---|
| RES-01 | The domain object must guard its own time and state, retaining identity and preventing invalid mutations. | `project/smartcare/domain.py` | Valid reschedule changes only time; invalid datetime cases and terminal-state requests preserve the original object fields. |
| RES-02 | The service must return the same stored object and perform appointment lookup before rescheduling. | `project/smartcare/services.py` | Valid move returns the original object; valid unknown ID raises `LookupError`; blank/invalid ID raises `ValueError`. |
| RES-03 | Datetimes must satisfy the existing naive, minute-precision contract. | `project/smartcare/domain.py`; `project/tests/test_rescheduling.py` | Separate wrong-type, timezone-aware, nonzero-seconds, and nonzero-microseconds cases each raise `ValueError` with no change. |
| RES-04 | Only a SCHEDULED appointment for the same practitioner at the exact proposed datetime conflicts. | `project/smartcare/services.py`; `project/tests/test_rescheduling.py` | Same-practitioner scheduled conflict rejected; different practitioner allowed; a slot held only by a CANCELLED appointment allowed; target excluded from its own conflict check. |
| RES-05 | Successful moves, no-ops, same-session reads, and failure atomicity must work with existing in-memory collections. | `project/smartcare/domain.py`; `project/smartcare/services.py`; `project/tests/test_rescheduling.py` | Same-time scheduled request is a no-op; failed-state snapshots unchanged; old slot can be booked after move; lookup and listing show the new time in the expected insertion order. |
| RES-06 | CANCELLED and COMPLETED appointments must not be rescheduled, even if the requested time is unchanged. | `project/smartcare/domain.py`; `project/tests/test_rescheduling.py` | Separate cancelled/same-time and completed/same-time requests raise `ValueError` and preserve state. |

## Todos

1. **Add guarded domain rescheduling** — RES-01, RES-03, RES-06. Reason: enforce time validation and scheduled-only mutation inside the appointment. File: `project/smartcare/domain.py`. Verify: valid time change; wrong-type, aware, seconds, and microseconds failures; cancelled/completed requests including same-time; same-time scheduled no-op.
2. **Add service rescheduling** — RES-02, RES-04, RES-05. Reason: coordinate lookup and conflict checks before domain mutation, while retaining the stored object. File: `project/smartcare/services.py`. Verify: known/unknown/blank IDs; conflict/self-exclusion; different practitioner; cancelled-only occupied slot; same-object return.
3. **Add focused rescheduling tests** — RES-01 through RES-06. Reason: capture each acceptance behavior without modifying existing tests. File: new `project/tests/test_rescheduling.py`. Verify each listed test case below.
4. **Verify and review changes** — RES-01 through RES-06. Reason: demonstrate behavior and confirm no unrelated changes. Files checked: changed implementation files and new test file. Verify: focused test module, complete pytest suite, and diff review.

## Test cases for `project/tests/test_rescheduling.py`

1. Valid move changes only the appointment time and retains appointment, ID, patient, and practitioner identities.
2. Service returns the exact same appointment object after a valid move.
3. Valid but unknown appointment ID raises `LookupError`.
4. Blank appointment ID raises `ValueError`.
5. Invalid appointment ID type raises `ValueError`.
6. Non-datetime proposed time raises `ValueError`.
7. Timezone-aware proposed datetime raises `ValueError`.
8. Proposed datetime with nonzero seconds raises `ValueError`.
9. Proposed datetime with nonzero microseconds raises `ValueError`.
10. Same-time request for a SCHEDULED appointment is a no-op.
11. Same-practitioner SCHEDULED appointment at the exact new time raises `ValueError`.
12. Conflict check excludes the target appointment itself.
13. Different practitioner at the exact same new time is allowed.
14. A time held only by a CANCELLED appointment is allowed.
15. CANCELLED target rejects a same-time request without mutation.
16. COMPLETED target rejects a same-time request without mutation.
17. Each failed request preserves appointment fields and the stored appointment list (state snapshots).
18. Moving the appointment frees its old slot for a new SCHEDULED appointment with the same practitioner.
19. Appointment lookup reflects the new time in the same store session.
20. Practitioner listing reflects the new time and preserves expected list order.

## Scope and constraints

- Do not edit existing tests or commit changes.
- Restrict repository edits to `project/smartcare/domain.py`, `project/smartcare/services.py`, and the new `project/tests/test_rescheduling.py`.
- Reuse `validate_date_time` and `SmartCareDataStore.has_practitioner_conflict`; do not change store collections, cancellation/history semantics, UI, persistence, or other excluded features.
- Once implementation and verification are complete, stop for human review; do not commit.


--Approved the Plan, and put it in Implementation Mode, approving each single condition and guiding through implementation.


| Plan step / action | Requirement link | Reason | Expected files | Accept / Modify / Reject | Conditions / evidence |
|---|---|---|---|---|---|
| Add Appointment.reschedule | RES-01, RES-02, RES-06 | Domain guards status and time | domain.py | Accept | Reuse validate_date_time, same-time no-op, no mutation on fail |
| Add AppointmentService.reschedule_appointment | RES-01 to RES-04 | Lookup then conflict then move | services.py | Accept | Use has_practitioner_conflict with exclude_appointment_id, return same object |
| Add focused tests | all RES and extra checks | Prove move, errors, listing | tests/test_rescheduling.py | Modify | Name that file, list each invalid datetime and snapshots |
| Run tests and review diff | Definition of Done | Independent check | none | Accept | Focused, common-only and full commands, no commit |

Approved bounded scope / forbidden changes / verification plan: Only domain.py, services.py and tests/test_rescheduling.py. No store, console, dependencies or existing-test edits. Verify with the three pytest commands.
Human plan approver and approval before edits: I (Junaid) approved the revised plan, then Copilot edited. 
Parameter names later renamed to new_date_time by myself (Junaid).
Tool permissions and any expanded-scope requests / decision: Plan first, then bounded edits. No extra files or packages requested.

## E Production diff review

Actual proposal / branch diff / version reviewed: branch stage10/Task/Agentic_rescheduling, uncommitted on top of 0716b11. git status --short, git diff --stat, git diff.

| File | Change purpose and reason | Requirement / test link | Expected? | Architecture OK? | Decision | Notes / correction |
|---|---|---|---|---|---|---|
| project/smartcare/domain.py | Appointment.reschedule | RES-01, RES-02, RES-06, test_rescheduling.py | Yes | Yes | Accept after rename | Parameter renamed to new_date_time |
| project/smartcare/services.py | AppointmentService.reschedule_appointment | RES-01 to RES-04, test_rescheduling.py | Yes | Yes | Accept after rename | Conflict check uses exclude_appointment_id |
| project/tests/test_rescheduling.py | New focused tests | all G rows | Yes | Yes | Accept | New file only, existing tests unchanged |

Every changed file inspected, including new/untracked files: Yes, git status showed those three only, verified changes through git diff.
Unexpected changes, scope creep, secrets/dependencies/configuration, unrelated cleanup: none, just renamed datetime parameter according to handout.

## F Separate test review

| Test | Criterion | Actual assertion | Assertion meaningful / adequate? | Agent changed expected behaviour? | Human or agent authorship | Decision and reason |
|---|---|---|---|---|---|---|
| test_valid_move_preserves_appointment_and_participant_identities, test_service_returns_same_stored_object_after_move, test_domain_reschedule_changes_time_on_the_same_object | RES-01, RES-02 | same object, ID, patient, practitioner, new time | Yes | No | Copilot | Accept |
| test_valid_unknown_appointment_id_raises_lookup_error, test_blank_appointment_id_raises_value_error, test_non_string_appointment_id_raises_value_error | RES-03 | LookupError or ValueError | Yes | No | Copilot | Accept, blank and non-string have no snapshot |
| test_same_practitioner_scheduled_conflict_is_rejected_without_mutation, test_failed_conflicting_move_preserves_complete_store_snapshot | RES-04 | ValueError, snapshot unchanged | Yes | No | Copilot | Accept |
| test_different_practitioner_at_new_time_is_allowed, test_cancelled_appointment_at_new_time_does_not_conflict | AC-RES-04 | move succeeds | Yes | No | Copilot | Accept |
| test_cancelled_target_rejects_same_time_without_mutation, test_completed_target_rejects_same_time_without_mutation | RES-06 | ValueError, snapshot unchanged | Yes | No | Copilot | Accept |
| test_lookup_and_practitioner_listing_show_new_time_in_order | RES-05-R2 | find and list show new time in order | Yes | No | Copilot | Accept |
| test_same_time_scheduled_reschedule_is_no_op, test_conflict_check_excludes_the_appointment_being_moved | no-op and self-exclusion | same snapshot, same object | Yes | No | Copilot | Accept, second test repeats the no-op |
| test_non_datetime_time, test_timezone_aware_time, test_time_with_seconds, test_time_with_microseconds | invalid datetime | ValueError, snapshot unchanged | Yes | No | Copilot | Accept, each case separate |
| test_old_slot_can_be_booked_after_move | old slot freed | new booking at old time | Yes | No | Copilot | Accept |

Comparison with original common tests / any proposed weakening: existing tests unchanged, common suite 37 passed
Independent human checks and corrections: renamed parameters to new_date_time, reran focused tests 20 passed. Total Test Suite ran 57 test cases passed.

## G Actual verification

| Requirement / acceptance scenario | Test or demonstration | Meaningful expected result | Actual result | Evidence / version |
|---|---|---|---|---|
| RES-01 / AC-RES-01 successful move | test_valid_move_preserves_appointment_and_participant_identities | time becomes NEW_TIME, status stays SCHEDULED | PASSED | tests/test_rescheduling.py |
| RES-02 same object and participant identities | test_service_returns_same_stored_object_after_move | is same appointment, patient and practitioner | PASSED | tests/test_rescheduling.py |
| RES-03 / AC-RES-02 unknown and invalid IDs | test_valid_unknown_appointment_id_raises_lookup_error, test_blank_appointment_id_raises_value_error, test_non_string_appointment_id_raises_value_error | LookupError or ValueError | PASSED | tests/test_rescheduling.py |
| RES-04 / AC-RES-03 conflicting practitioner | test_same_practitioner_scheduled_conflict_is_rejected_without_mutation | ValueError, snapshot unchanged | PASSED | tests/test_rescheduling.py |
| AC-RES-04 different practitioner allowed | test_different_practitioner_at_new_time_is_allowed | A1 moves to NEW_TIME | PASSED | tests/test_rescheduling.py |
| RES-06 / AC-RES-05 cancelled and completed | test_cancelled_target_rejects_same_time_without_mutation, test_completed_target_rejects_same_time_without_mutation | ValueError, snapshot unchanged | PASSED | tests/test_rescheduling.py |
| RES-05-R2 / AC-RES-06-R2 lookup and listing order | test_lookup_and_practitioner_listing_show_new_time_in_order | find and list show new time in date order | PASSED | tests/test_rescheduling.py |
| Self-exclusion and same-time no-op | test_same_time_scheduled_reschedule_is_no_op | same snapshot, same object | PASSED | tests/test_rescheduling.py |
| Invalid datetime and failed-state snapshots | four invalid-time tests | ValueError, snapshot unchanged | PASSED | tests/test_rescheduling.py |
| Successful old-slot reuse | test_old_slot_can_be_booked_after_move | A2 books OLD_TIME after A1 moved | PASSED | tests/test_rescheduling.py |

| Suite | Command / working directory | Code SHA | Actual count and result | Evidence |
|---|---|---|---|---|
| Focused PG | python -m pytest -q tests/test_rescheduling.py in project/ | uncommitted on 0716b11 | 20 passed | terminal run |
| Common independently | python -m pytest -q --ignore=tests/test_rescheduling.py in project/ | uncommitted on 0716b11 | 37 passed | terminal run |
| Full cumulative | python -m pytest -q in project/ | uncommitted on 0716b11 | 57 passed | terminal run |
| Integrated retest | python -m pytest -q and python -m pytest -q tests/test_rescheduling.py in project/ | 1989ed1 (main after merging PR #21) | 57 passed full, 20 passed focused (Python 3.14.3) | run by Dominic on main after the merge |

Failures / diagnosis / corrections and reruns / unresolved concerns: first agent names used date_time, renamed to new_date_time, focused tests 20 passed after that. 

## H Decisions corrections and independent review

| Significant agent action | Human review and evidence | Accept / Modify / Reject and reason | Manual correction or recovery | Recheck evidence |
|---|---|---|---|---|
| First Copilot plan, four todos no requirement map | Compared to C and the handout prompt | Modify | Asked for RES map, named test file, listed cases, no commit | Revised plan in D |
| Copilot added reschedule methods and tests | git diff, read domain.py and services.py, ran pytest | Modify | Renamed date_time to new_date_time | focused 20 passed |
| New tests/test_rescheduling.py | Read assertions, compared with G cases | Accept | none | 20 passed, common 37, full 57 |

Final proposal decision: Accepted after modification
Evidence supporting decision: Diff only in the three allowed files, methods match the handout names after rename, focused 20 passed, common 37 passed, full 57 passed
If rejected, how the required feature was subsequently completed and verified: not applicable
Saved proposal and targeted recovery details if needed: not applicable, no rollback
Human explanation of every changed method and limitations: Appointment.reschedule checks SCHEDULED, validates the time, same-time is a no-op, then sets _date_time. AppointmentService.reschedule_appointment finds the appointment, checks has_practitioner_conflict with exclude_appointment_id, then calls reschedule and returns the same object. No console command. Listing uses the existing query.
Another PG / willing UG / tutor reviewer, actual PR/diff review and feedback: Independent review by Dominic (DominicRDA-uc, UG, willing reviewer) on PR https://github.com/DominicRDA-uc/st1-assignment-3/pull/21, 9 Nov 2026. Dominic read the domain, service, README and test diffs, checked out the branch and ran python -m pytest -q in project/ (57 passed) and tests/test_rescheduling.py (20 passed) before approving. Feedback: Appointment.reschedule checks the SCHEDULED state and validates the time before changing anything, and reschedule_appointment checks practitioner conflicts excluding the target itself and returns the same object (RES-01 to RES-06). No changes were requested. No merge conflicts with main, and the common Stage 9 tests (37) still pass.
Corrections, recheck and actual approval before integration: Yes
Integrated PG SHA / common protected SHA: PG SHA 1989ed1 (merge of PR #21, merged by Dominic after approval). Common Stage 9 SHA 280884d755caacd8679ddac78b1dab4accaa05ef
Each assessed PG member's implementation, supervision and test contribution: Junaid wrote evidence file, created issue, re defined vague requirement, proposed prompt, revised the plan, approved the plan, reviewed the diff and tests, renamed the parameters, ran the three pytest commands. Copilot drafted the two methods and the test file.
Optional UG help, acknowledged separately: Dominic (UG) acted as the independent PR reviewer and ran the integrated retest. This is unassessed UG help. All implementation, supervision and agent decisions are Junaid's.

## I Four reflections

1. Which agent change had the greatest blast radius? AppointmentService.reschedule_appointment, because a wrong conflict check would let two SCHEDULED bookings share a practitioner time or would block a valid move, and that sits on the same store as booking and listing. 
2. Did the plan predict it? Yes, the revised plan put lookup and has_practitioner_conflict with exclude_appointment_id in the service before any mutation
3. What did you reject or manually correct? The first plan was modified, not rejected. After implementation I renamed date_time to new_date_time. No rollback needed.
4. What evidence justified final approval? Allowed files only, identities and failed-state snapshots in the tests, 20 then 37 then 57 passed.

## J Ten formative questions

1. What is the difference between an AI assistant and an engineering agent? An assistant suggests text for you to paste. An engineering agent can inspect the repo, edit several files and run tools, so it needs a plan, scope limits and review
2. What is the simplified agent loop used in Stage 10? Human analysis, written task, plan review, approved bounded edits, production diff review, separate test review, independent tests, Accept Modify or Reject, corrections, another-member review, then integration
3. Why should an agent plan be reviewed before repository edits begin? So out of scope work such as storage or new packages is stopped before it lands in the tree
4. What is meant by the blast radius of a software change? How far a fault can spread, which files, tests and behaviours it can break
5. Why is diff review essential for agentic changes? Passing tests do not show extra files, secrets or weakened assertions, the diff does
6. What is a human approval gate? A point where a person must inspect and decide before the next step, such as before edits or before merge. Tool permission is not that gate
7. What is test accommodation and why is it dangerous? Weakening an assertion so a bad implementation passes, for example checking is not None instead of the new time, which hides a missed requirement
8. What is rollback in the context of agentic software engineering? Keeping the rejected diff, then a targeted restore or revert to a previous head/stable commit/checkpoint, not a repo-wide reset.
9. Who remains accountable for accepted agentic changes? The PG member (me/junaid) who approved them.
10. What is the Stage 10 engineering rule? Humans specify, review/revise/approve the plan, inspect every file and test editted by the agent, and stay accountable. 

## K Completion and Stage 11 handover

- [X] Common Stage 9 checkpoint protected; UG pathway unaffected.
- [X] RES-01–06 and RES-05-R2 implemented in the same project.
- [X] Domain/service boundaries, current exceptions and coding standard preserved.
- [X] Positive/negative/boundary cases and failed-state checks verified.
- [X] Common tests remain valid and independently passing; full suite passes.
- [X] Plan reviewed before bounded actions; every file and test diff inspected.
- [X] Actual agent route, decisions, corrections and rechecks recorded honestly.
- [X] No unrelated features, persistence, dependencies or staff solutions introduced.
- [X] Another-member or tutor review and integrated retest complete.
- [X] Tutorial, four reflections, ten formative responses and PG contributions complete.
- [X] Each PG member can explain their code and supervision.
- [X] README PG note, actual integrated SHA and limitations recorded.

Unresolved issues / owner / action: None
Stage 11 handover references to extension, tests, dependencies and actual AI/review evidence: Rescheduling is in domain.py and services.py. Tests are tests/test_rescheduling.py. No new dependency. Copilot drafted the code and tests. Plan, diff and test review are in D to H of this file. Common Stage 9 SHA 280884d.
Submitted SHA / explanation if later than tested code: [response]
Stage 11 materials are supplied from the beginning. Begin Stage 11 only after Stage 10 has been integrated, verified and recorded. UG follows the protected common code from Stage 9 to Stage 12.