# Stage 7 Testing and Verification Record

Group/tutorial: Wednesday 2.30-4.30\
Members/cohorts: Junaid Sayani (junaidSayani1), Dominic (DominicRDA-uc), Julianne (Jules-tryingtocode), Aditti\
Requirements baseline: SmartCare A3 Requirements Baseline 2026, revision 2.
Use the same project/. Link actual evidence; keep responses concise. Blank fields are for your group. Copy rows only as needed.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage07/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions.

## A Tutorial Activities

### Activity 1 Requirement to test

For each requirement, propose one positive test, one negative test and the key assertion.

| Requirement                         | Positive test                                                                                 | Negative test                                                                                                                          | Key assertion                                                              |
|-------------------------------------|-----------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| FR-01 Register patient              | Register a patient with a unique Patient ID and name string.                                  | Attempt to register an empty string for the Patient ID.                                                                                | assert data_store.find_patient(patient_id).name == "Valid Name"            |
| FR-05 Prevent practitioner conflict | Book a practitioner for an appointment at a available time slot.                              | Attempt to book the same practitioner for a second appointment at an overlapping time slot.                                            | with pytest.raises(Exception):                                             |
| FR-06 Cancel appointment            | Cancel an active, confirmed appointment.                                                      | Attempt to cancel an appointment that has already been fully completed or is already cancelled.                                        | assert appointment.status == AppointmentStatus.CANCELLED                   |
| FR-07 Retain cancelled history      | Cancel a valid appointment, then execute a history lookup query for that specific patient ID. | Search for active/upcoming appointments for that patient and verify that the cancelled appointment does not show up as an active slot. | assert cancelled_appointment in data_store.get_patient_history(patient_id) |

### Activity 2 Strong or weak assertion

For each, select Strong for stated behaviour or Weak/unclear and explain why. State the behaviour and limits.

`assert True`
Judgement: Weak/unclear Why: `assert True` does not verify any data or system behaviour. Furthermore, it will always pass tests as successful regardless of whether there is an error.

`assert appointment is not None`
Judgement: Weak/unclear  Why: The assertion only verifies that an appointment object exists in the memory but fails to check the object's internal properties. Hence, the assertion will pass tests even if the appointment has blank fields, corrupt timestamps, or completely incorrect patient and practitioner data.

`assert appointment.status == AppointmentStatus.CANCELLED`
Judgement: Strong for stated behaviour Why: The assertion explicitly checks the status of the appointment and verifies whether it has been changed to `CANCELLED`. Furthermore, it will catch the error if the status says anything else and ensure the test fails.

`assert len(results) > 0`
Judgement: Weak/unclear  Why: The assertion only verifies that there is at least one item in results but does not check if the contents in the list are correct. As a result, this assertion passes the test regardless of whether results contains unrelated data.

`assert data_store.find_appointment('A1') is appointment`
Judgement: Weak/unclear Why: The assertion checks for object identity using `is` instead of checking if the actual data values match using `==`. This makes the test fragile because if the data_store creates or returns a fresh object instance during a lookup, the assertion will fail and report a false error even if all the internal appointment data is correct.

### Activity 3 Boundary thinking

Design boundary or edge cases for blank identifiers, whitespace-only names, same-time practitioner bookings, cancelled appointments and invalid status transitions.
For each input/state, expected result and supporting contract:

**Blank Identifiers**
- Input/State: A completely empty string passed as the unique identifier during a Patient or Practitioner creation.
- Expected result: The system rejects the action immediately and throws a validation error (i.e.ValueError).
- Supporting contract: Constructor pre-condition contract requiring all unique system IDs to be non-empty strings.

**Whitespace-Only Names**
- Input/State: Providing a name string consisting entirely of blank spaces (e.g., "   ") for a new user record.
- Expected result: The code detects that no real characters exist, and blocks the entry with an error.
- Supporting contract: Input validation contract requiring name fields to contain at least one meaningful, non-whitespace character.

**Same-Time Practitioner Bookings**
- Input/State: Two separate patients trying to book an appointment with the exact same Practitioner at identical calendar time slots.
- Expected result: The first scheduling request succeeds, while the second overlapping request is blocked and raises a conflict exception.
- Supporting contract: System invariant scheduling contract forbidding a single practitioner resource from being double-booked.

**Cancelled Appointments**
- Input/State: Selecting an appointment that already has a status label of `CANCELLED` and invoking the cancellation service on it a second time.
- Expected result: Rejects the repeated request with an error to prevent modifying an inactive record.
- Supporting contract: State lifecycle contract establishing that an appointment cannot transition out of a terminal cancelled state.

**Invalid Status Transitions**
- Input/State: Attempting to force an appointment's status field to transition directly from `CANCELLED` straight back to `SCHEDULED` or `COMPLETED`.
- Expected result: The system blocks the illegal modification instantly and raises an invalid state transition exception.
- Supporting contract: Explicit state-machine transition matrix guard preventing the modification or resurrection of an inactive record.

### Activity 4 Critique GitHub Copilot tests

GitHub Copilot generates five tests, all of which pass. Two only assert that objects are not None, one asserts True, and two assume SMS notifications exist. Identify what is wrong and rewrite the test intentions.
(Candidates answered respectively to the stated Copilot tests).

| Candidate | What is wrong                                                                                                                     | Rewritten test intention                                                                                          |
|-----------|-----------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| 1         | It only checks if the object is not None. It will pass even if the object has completely blank or corrupted internal data fields. | Verify that registering a patient with a valid, unused ID correctly stores the data.                              |
| 2         | It checks for surface-level object existence rather than verifying that the fields are properly matched.                          | Verify that a registered practitioner's unique identifier can be looked up and returns the exact matching record. |
| 3         | `assert True` can never fail under any circumstance, completely hiding bugs even if the system fails to save appointments.        | Verify that creating a valid booking successfully stores a new appointment with an initial status of `SCHEDULED`. |
| 4         | The requirements explicitly state that only clinic staff operate the system and no alert tools exist.                             | Verify that cancelling a scheduled appointment successfully switches its internal status field to CANCELLED`.     |
| 5         | It fabricates a text alert framework and tests a fake mock object instead of checking session history data.                       | Verify that a cancelled appointment remains safely retrievable inside the current-session history log.            |

### Tutorial exit question

Why can 100% code coverage coexist with poor software verification?

Code coverage only tracks which lines of code were executed during a test but does not track the quality or depth of what those tests actually checked. If a test suite executes every line of code but relies exclusively on weak verification checks, it will falsely report a 100% successful test run while remaining completely blind to logic bugs, data corruption, or severe violations of business rules.

## B Requirement to Test Traceability Matrix

Assign TEST IDs before implementation or generation. Use canonical AC IDs with their actual meaning; quote supporting revision 2 contracts when no canonical AC is assigned. Blank-ID validation is not AC-01.2. Identify supplied versus student-authored evidence.

| Requirement   | Acceptance criterion                                                                                 | Test ID    | Test type        | Test name / location                                                                       | Expected behaviour                                                            | Result / observed status | Supplied or student-authored |
|---------------|------------------------------------------------------------------------------------------------------|------------|------------------|--------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|--------------------------|------------------------------|
| FR-01         | AC-01.1 Valid required patient data with an unused ID is stored.                                     | TS-FR01-01 | Complete Service | `tests/test_services/patient_service_test.py::test_find_patient_with_valid_id`             | Patient object is created and safely stored in the data store.                | Passed                   | Student-authored             |
| FR-01         | AC-01.2 Registration with an existing patient ID is rejected.                                        | TS-FR01-02 | Complete Service | `tests/test_services/patient_service_test.py::test_invalid_patient_id`                     | Rejects invalid inputs and leaves the original record completely untouched.   | Passed                   | Student-authored             |
| FR-02         | AC-02.1 and AC-02.2 Known patient lookup succeeds; unknown patient lookup reports absence.           | TS-FR02-01 | Complete Service | `tests/test_services/patient_service_test.py::test_unknown_patient_id`                     | Returns the target patient object if known; raises a `LookupError` if absent. | Passed                   | Supplied                     |
| FR-04         | AC-03.1 Registered participants, a unique ID and a free time produce a stored SCHEDULED appointment. | TS-FR04-01 | Complete Service | `tests/test_services/appointment_service_test.py::book_appointment`                        | Appointment is successfully stored with an initial state of `SCHEDULED`.      | Passed                   | Student-authored             |
| FR-04         | AC-03.2 Booking an unknown patient or practitioner is rejected.                                      | TS-FRO4-02 | Complete Service | `tests/test_services/appointment_service_test.py::test_unknown_appointment_id`             | Rejects the workflow and raises a LookupError for the missing participant.    | Passed                   | Student-authored             |
| FR-05         | AC-04.1 and AC-04.2 Same practitioner/exact time/SCHEDULED conflicts; another practitioner allowed.  | TS-FR05-01 | Complete Service | `tests/test_services/appointment_service_test.py`::`test_invalid_transition_appointment`   | Detects timing rules, ensuring conflicting entries block booking flow.        | Passed                   | Student-authored             |
| FR-06         | AC-05.1 Cancelling a SCHEDULED appointment changes it to CANCELLED.                                  | TS-FR06-01 | Complete Service | `tests/test_services/appointment_service_test.py`::`test_cancel_appointment_with_valid_id` | The internal state moves precisely from `SCHEDULED` to `CANCELLED`.           | Passed                   | Student-authored             |
| FR-07         | AC-05.2 Cancelled history remains retrievable in the current session.                                | TS-FR07-01 | Complete Service | `tests/test_services/appointment_service_test.py`::`test_cancel_appointment_with_valid_id` | The cancelled appointment remains retrievable from the datastore log list.    | Passed                   | Student-authored             |
| FR-06         | AC-05.3 Repeated cancellation is rejected.                                                           | TS-FR06-02 | Complete Service | `tests/test_services/appointment_service_test.py`::`test_invalid_transition_appointment`   | Raises a `ValueError` when attempting to cancel an already cancelled object.  | Passed                   | Student-authored             |
| FR-08         | AC-06.1 A known appointment ID returns that appointment.                                             | TS-FR08-01 | Complete Service | `tests/test_services/appointment_service_test.py`::`test_unknown_appointment_id`           | Querying the datastore returns the exact matching appointment reference.      | Passed                   | Student-authored             |

## C Test Design

Use descriptive test names such as test_cancel_changes_status() or test_blank_patient_id_is_rejected(). Explain what new evidence each case adds.

| Test ID     | Requirement | Acceptance criterion | Positive / Negative / Boundary | Test intention                                                                                                          | Observable result expected                                                                 | Added evidence beyond supplied tests                                                                                |
|-------------|-------------|----------------------|--------------------------------|-------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| TS-FR01-01  | FR-01       | AC-01.1              | Positive                       | Verify that a normal, valid patient profile is successfully saved and persists through the service registry.            | Stored attributes are readable, matching input data.                                       | Establishes the baseline operational success path for clean, standard patient registration.                         |
| TS-FR01-02  | FR-01       | AC-01.2              | Boundary                       | Verify that registering an existing patient ID is flatly rejected by the data store.                                    | A `ValueError` exception is raised, leaving the original data completely intact.           | Proves that the service actively intercepts identity collision risks and blocks accidental record overwriting.      |
| TS-FR02-01  | FR-02       | AC-02.1 / 02.2       | Boundary                       | Verify that lookup of non-existent patient keys safely returns error exceptions without polluting session collections.  | Raises a `LookupError` when searching for an unregistered identifier.                      | Pinpoints standard system boundary parameters for missing identity keys.                                            |
| TS-FR04-01  | FR-04       | AC-03.1              | Positive                       | Verify that an appointment is created with an initial active state under standard constraints.                          | An appointment object is successfully logged with an initial status label of `SCHEDULED`.  | Confirms structural configuration settings and default enum assignments upon direct construction.                   |
| TS-FR04-02  | FR-04       | AC-03.2              | Negative                       | Verify that booking requests involving missing or unregistered participant IDs are flatly rejected.                     | The workflow coordination layer intercepts the request and raises a `LookupError`.         | Adds critical coverage proving that the scheduling pipeline validates participant existence before reserving slots. |
| TS-FR05-01  | FR-05       | AC-04.1 / 04.2       | Negative                       | Verify that scheduling two overlapping slots for the same practitioner is blocked while allowing separate alternatives. | Second duplicate scheduling attempt triggers a conflict `ValueError` exception.            | Validates calendar asset integrity by proving the system blocks resource-allocation overlaps at minute precision.   |
| TS-FR06-01  | FR-06       | AC-05.1              | Positive                       | Verify that calling the cancel service explicitly updates a valid appointment's status attribute.                       | The appointment status moves cleanly from the active `SCHEDULED` state to `CANCELLED`.     | Confirms the programmatic correctness of state-machine transitions through public service methods.                  |
| TS-FR07-01  | FR-07       | AC-05.2              | Positive                       | Verify that a cancellation does not purge or erase records from memory history logs.                                    | The target appointment remains fully visible and searchable in historical lookup queries.  | Guarantees compliance with clinical auditing requirements by proving historic logs remain intact after state flips. |
| TS-FR06-02  | FR-06       | AC-05.3              | Negative                       | Verify that running the cancellation service on an already cancelled entry is caught and rejected.                      | A `ValueError` is raised when trying to transition out of an inactive state.               | Proves terminal states are securely locked against repeating out-of-order lifecycle operations.                     |
| TS-FR08-01  | FR-08       | AC-06.1              | Positive                       | Verify that a valid search using a known appointment ID pulls the correct reference from session storage.               | The lookup query returns the precise, matching appointment object instance.                | Establishes lookup query reliability for individual records independent of their active state status.               |

## D Arrange Act Assert Record

Arrange test data; act on one meaningful behaviour; assert the required observable outcome. Use the specific current exception with pytest.raises where needed.

| Test ID    | Arrange                                                                                | Act                                                                                              | Assert                                                                      | Why meaningful / why assertion proves criterion                                                                                                   |
|------------|----------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| TS-FR01-01 | Initialize an empty `SmartCareDataStore` and a new `PatientService`.                   | Invoke `service.register_patient('J1', 'Alex Example')`.                                         | `assert service.find_patient('J1') is patient`                              | It proves value storage through the workflow, verifying that a valid patient record is saved into the session store and accurately retrieved.     |
| TS-FR01-02 | Register an initial patient with ID `'J1'` into the active data store.                 | Attempt to call `service.register_patient('J1', 'New Name')` again.                              | `with pytest.raises(ValueError):` wrapping the second registration action.  | Catching a `ValueError` proves that the system actively blocks duplicate IDs and prevents overwriting existing records.                           |
| TS-FR02-01 | Prepare a fresh, empty data store session.                                             | Invoke `service.find_patient('J3')` for an absent record.                                        | `with pytest.raises(LookupError):` surrounding the lookup operation.        | Verifies the service boundary contract by ensuring that querying an unknown ID safely raises an explicit error instead of returning broken data.  |
| TS-FR04-01 | Setup a clean session store, registering patient `'P1'` and practitioner `'D1'`.       | Call `appointment_service.book_appointment('A1', 'P1', 'D1', datetime(2026, 10, 1, 9))`.         | `assert booked.status is AppointmentStatus.SCHEDULED`                       | Directly verifies that a newly booked appointment successfully transitions to the required default active state in memory.                        |
| TS-FR04-02 | Register practitioner `'D1'` but do *not* register the patient ID.                     | Attempt to execute the `book_appointment` service call.                                          | `with pytest.raises(LookupError):` surrounding the booking call.            | Catching a `LookupError` proves that the system protects session integrity by blocking orphaned, corrupted entries from entering the store.       |
| TS-FR05-01 | Complete a valid booking helper routine for practitioner `'D1'` at `2026-10-01 09:00`. | Attempt to book a second appointment for a different patient with `'D1'` at the exact same time. | `with pytest.raises(ValueError):` surrounding the second booking attempt.   | Catching a `ValueError` demonstrates that the scheduling workflow actively guards calendar resources against double-booking conflicts.            |
| TS-FR06-01 | Establish an active session and create a scheduled appointment `'A1'` via the helper.  | Invoke `appointment_service.cancel_appointment('A1')`.                                           | `assert appointment.status is AppointmentStatus.CANCELLED`                  | Proves that the public service operation successfully forces the entity state machine to move from active to a cancelled state.                   |
| TS-FR07-01 | Call the cancellation service on an active appointment `'A1'` in the current session.  | Run a search query using `data_store.list_appointments()`.                                       | `assert data_store.list_appointments() == [appointment]`                    | Proves that moving a slot out of active status modifies it in place without purging or deleting the record from the session tracking list.        |
| TS-FR06-02 | Fetch an appointment that has already been flipped to a `CANCELLED` status.            | Attempt to call `cancel_appointment('A1')` a second time on that inactive record.                | `with pytest.raises(ValueError):` wrapping the duplicate cancellation call. | Catching a `ValueError` proves that terminal states are locked against repeating invalid actions, leaving the data unchanged.                     |
| TS-FR08-01 | Store a valid appointment with ID `'A1'` into the active data store registry.          | Invoke the `find_appointment('A1')` service lookup function.                                     | `assert appointment_service.find_appointment('A1') is appointment`          | Confirms lookup query reliability by proving a known ID accurately returns the exact physical object reference throughout the session.            |

## E Domain Test Evidence

Cover Patient/Practitioner construction and validation; Appointment construction, initial status, cancellation and illegal/repeated transitions. Preserve the four reference intentions described in handout Part C.

| Test ID    | Behaviour                                                 | Test file/function                                                                         | Result   |
|------------|-----------------------------------------------------------|--------------------------------------------------------------------------------------------|----------|
| TS-FR01-02 | Rejects empty or space-only patient IDs                   | `tests/test_services/patient_service_test.py`::`test_invalid_patient_id`                   | Passed   |
| TS-FR03-02 | Rejects empty or space-only practitioner IDs              | `tests/test_services/practitioner_service_test.py`::`test_invalid_practitioner_id`         | Passed   |
| TS-FR06-01 | Successfully flips appointment status to CANCELLED        | `tests/test_services/appointment_service_test.py`::`test_cancel_appointment_with_valid_id` | Passed   |
| TS-FR06-02 | Rejects repeated cancellations on an inactive appointment | `tests/test_services/appointment_service_test.py`::`test_invalid_transition_appointment`   | Passed   |

## F Service Test Evidence

Use fresh shared SmartCareDataStore state, registered objects and completed Stage 6 services.

| Test ID    | Behaviour                                               | Requirement / criterion     | Test file/function                                                                         | Result |
|------------|---------------------------------------------------------|-----------------------------|--------------------------------------------------------------------------------------------|--------|
| TS-FR01-01 | Correctly saves and finds a valid patient profile       | FR-01 / AC-01.1             | `tests/test_services/patient_service_test.py`::`test_find_patient_with_valid_id`           | Passed |
| TS-FR03-01 | Correctly saves and finds a valid practitioner profile  | FR-03 / Supporting Contract | `tests/test_services/practitioner_service_test.py`::`test_find_practitioner_with_valid_id` | Passed |
| TS-FR04-01 | Freshly booked appointments start as SCHEDULED          | FR-04 / AC-03.1             | `tests/test_services/appointment_service_test.py`::`book_appointment`                      | Passed |
| TS-FR07-01 | Cancelled appointments stay searchable in logs          | FR-07 / AC-05.2             | `tests/test_services/appointment_service_test.py`::`test_cancel_appointment_with_valid_id` | Passed |
| TS-FR08-01 | Finds an appointment reference by its distinct ID token | FR-08 / AC-06.1             | `tests/test_services/appointment_service_test.py`::`test_unknown_appointment_id`           | Passed |

## G Negative and Boundary Cases

Connect cases to actual contracts and verify unchanged state after rejection.

| Behaviour                | Boundary/invalid input                       | Expected result                                                | Test ID    |
|--------------------------|----------------------------------------------|----------------------------------------------------------------|------------|
| Patient Registration     | Empty or blank space IDs (`""`, `" "`)       | Raises `ValueError` error; data store stays completely clean.  | TS-FR01-02 |
| Practitioner Lookup      | Case-insensitive mismatches (`"prac1"`)      | Raises `LookupError` error; practitioner list stays unchanged. | TS-FR03-02 |
| Appointment Booking      | Trying to cancel a non-existent ID (`"A3"`)  | Raises `LookupError` error; active bookings stay unchanged.    | TS-FR04-02 |
| Appointment Cancellation | Trying to cancel an already `CANCELLED` slot | Raises `ValueError` error; history logs stay unchanged.        | TS-FR06-02 |

## H GitHub Copilot Test Design

Select ONE real acceptance criterion. Complete human-first fields before using Copilot. Do not require an accepted generated test.

Requirement: FR-06 Cancel only a SCHEDULED appointment. 
Acceptance criterion: AC-05.1 under FR-06 Cancelling a SCHEDULED appointment changes it to CANCELLED.
Behaviour to test: Verify that invoking the cancellation workflow explicitly changes a valid, active appointment's status attribute from `SCHEDULED` to `CANCELLED` within the session store.
Human-first test idea/categories:
- Positive Case: Cancel a freshly scheduled appointment and assert its status flag is exactly `AppointmentStatus.CANCELLED`.
- Negative Case: Attempt to cancel a non-existent appointment ID and assert it safely raises a `LookupError`.
- Boundary Case: Attempt to call the cancellation service on an appointment that has already transitioned to a terminal `CANCELLED` status and assert that it correctly throws a `ValueError`.
Prompt and purpose: 
- Prompt: Part H Requirement + Part H Acceptance Criterion + "Propose pytest test candidates covering a valid case, an invalid case and meaningful boundaries. For each candidate, state exactly which required behaviour it is intended to verify. Do not invent behaviour not stated in the requirement or criterion. Use observable outcomes rather than private implementation details. Use the current SmartCare public contracts and shared SmartCareDataStore. Do not introduce SQLite, repository abstractions or unrelated features. Do not claim that a proposed test has been executed."

For each significant candidate, copy this entry as needed:

**Candidate 1**
- Copilot test idea/candidate: `test_cancel_scheduled_appointment_changes_status_to_cancelled`
- What it claims to verify: Verifies the behaviour AC-05.1 
- Requirement trace: FR-06 / AC-05.1
- Assertion quality: Weak (`assert appointment.status == "CANCELLED"` uses a loose string literal instead of system enums)
- Human critique: While the test scenario is conceptually correct, the assertion quality is weak because checking against raw text strings can hide bugs if the internal enum properties are modified.
- Decision: Modify
- Reason: The logical intent is perfect, but the code snippet must be modified to use our real `AppointmentService` setup and strict enum types (`AppointmentStatus.CANCELLED`) inside our existing test file.
- Final test reference if accepted/modified: `tests/test_services/appointment_service_test.py`::`test_cancel_appointment_with_valid_id`
- Actual verification result: Passed upon executing test.

**Candidate 2**
- Copilot test idea/candidate: `test_cannot_cancel_non_scheduled_appointment`
- What it claims to verify: Verifies FR-06
- Requirement trace: FR-06
- Assertion quality: Strong (`with pytest.raises(ValueError):`).
- Human critique: The test correctly leverages our repository rule that illegal state transitions raise a `ValueError`. It accurately locks down state-machine invariants.
- Decision: Modify
- Reason: Highly critical for negative boundary testing. Needs to be updated to our shared transition test to cover both repeated cancellation blocks and out-of-order state transitions in our codebase.
- Final test reference if accepted/modified: `tests/test_services/appointment_service_test.py`::`test_invalid_transition_appointment`
- Actual verification result: Passed upon executing test.

Before accepting: traces to a requirement/criterion; can fail for the right reason; assertion checks required behaviour; no invented business rule; no unnecessary private implementation dependence. Reject/modify weak assertions, invented requirements, excessive mocking, duplicates, wrong exceptions, obsolete architecture and unnecessary dependencies.

## I Weak Copilot Test Reflection

Which Copilot-generated test looked convincing but was weak? Candidate 1
Why was it weak? Human Critique for Candidate 1 Section H
How did you strengthen it? Reason for Candidate 1 Section H
Accepted / modified / rejected test decisions and evidence: Final test reference and Actual verification result for Candidate 1 for Section H. No test defects found.

## J Regression Run

Run python -m pytest from project/. Retain all accumulated tests. Record the tested SHA accurately.

| Command            | Working directory | Code SHA                                   | Passed | Failed | Failure summary | Product defect / test defect / unresolved | Evidence and interpretation                                                                |
|--------------------|-------------------|--------------------------------------------|--------|--------|-----------------|-------------------------------------------|--------------------------------------------------------------------------------------------|
| `python -m pytest` | `project/`        | `ae093ceb10ec97001374213aa17da6a3d7637d80` | 17     | 0      | None            | None / Clean Run                          | All 17 tests passed cleanly across the starter checks and individual service test modules. |

Individual test runs and changed-order independence evidence:
- Patient service module run: `python -m pytest tests/test_services/patient_service_test.py` --> 3 passed.
- Practitioner service module run: `python -m pytest tests/test_services/practitioner_service_test.py` --> 3 passed.
- Appointment service module run: `python -m pytest tests/test_services/appointment_service_test.py` --> 3 passed.
- Modules were run independently and in randomized sequences. Since each test sets up a locally-scoped `SmartCareDataStore()` instance, they remain perfectly isolated. Zero cross-suite state pollution, side-effects, or dependencies were observed regardless of execution order.

Optional tutor-led demonstration notes:\
A meaningful test should detect a relevant incorrect result. Students do not have to perform the demonstration or submit failure/restoration evidence for assessment. The tutor restores the example and reruns its tests. This is not a Stage 8 fault activity.\
Requirement → test → failure/observation → diagnosis → change → verification: The regression run executed successfully with a 100% pass rate (`17 passed, 0 failed`), confirming zero software regressions or broken requirements.

## K What the Suite Still Does Not Prove

What does your test suite still not prove? The current automated suite evaluates isolated current-session backend operations in memory. It does not prove long-term text file serialisation safety, data race prevention under concurrent multi-user access, or the layout accuracy of the terminal console menu presentation code.\
Coverage if used: Not used\
Which uncovered areas matter, and why does coverage percentage alone not establish correctness? Uncovered branches in the user-interactive menu handler (`console.py`) matter because they control operator workflows. High coverage percentages alone cannot prove system correctness, because a test runner can touch every single line of code successfully while weak or surface-level assertions fail to detect incorrect logic or corrupted output states.\
Optional fixtures/parametrisation used and why, if any: Not used

## L Git and Review Evidence

Use links rather than copying GitHub history. Continue the Stage 6 workflow; no commit/PR count, conflict or individual test quota is imposed.

| Issue/task | Branch     | PR         | Reviewer   | Key feedback | Outcome    |
|------------|------------|------------|------------|--------------|------------|
| [complete] | [complete] | [complete] | [complete] | [complete]   | [complete] |

## M Contribution Evidence

Record actual work in test design, implementation, review, traceability, diagnosis, necessary fixes and integration. Do not include confidential peer ratings.

| Member                        | Actual contribution        | Evidence link   |
|-------------------------------|----------------------------|-----------------|
| Julianne (Jules-tryingtocode) | Documentation of Stage 7,  | [complete]      |

## N Formative Questions

1. What question does verification answer?
Answers whether the application code accurately satisfies the technical design contracts, specifications, and business rules stated in the requirements baseline.

2. What question does validation answer?
Answers whether the implemented software functions meet the actual, real-world operational needs and workflows of the clinic staff.

3. What is a unit test?
An isolated test that verifies a single small piece of domain logic (such as an individual function or class method) entirely independent of the surrounding service layers or shared data stores.

4. What is a pytest fixture?
A reusable setup helper function that establishes a clean, predictable baseline state before a test case runs, further preventing tests from affecting each other.

5. What is parametrisation in pytest?
A testing technique that enables a single test function to automatically execute multiple separate times using a sequence of distinct input values and expected outcomes without duplicating code.

6. What is regression testing?
Rerunning the complete suite of existing automated tests after applying modifications or bug fixes to guarantee that the changes have not broken previously verified functionalities.

7. What does code coverage tell us, and what does it not prove?
It reveals exactly which lines of text were touched or executed by the test runner. It does not prove that the code logic is correct, complete, or that the assertions used actually check the required behaviour.

8. What makes an assertion weak?
An assertion is weak if it only validates superficial metrics such as checking that an object is not None or that a list is not empty instead of checking the precise data values required by a business rule.

9. What is the appropriate role of GitHub Copilot as a test assistant?
To handle typing out standard setup data quickly, while the human engineer decides the actual rules, edge cases, and safety checks to test.

10. What is the Stage 7 engineering rule?
Complete automated verification, requirement tracking, and code reviews on a dedicated task branch before integrating and recording a tested main SHA; never rely on unverified code branches or unevidenced work.

## O Stage Completion

Tested Stage 7 main SHA: ae093ceb10ec97001374213aa17da6a3d7637d80\
Full-suite result: 17 Passed, 0 failed \
Unresolved defects and effect on baseline: None\
Clean working tree and integration evidence: [complete] \
Stage 8 handover status: Stage 8 has yet to be handed over to Dominic. \
All tutorial/formative responses and traceability/Copilot decisions complete: Awaiting review response for Section L
