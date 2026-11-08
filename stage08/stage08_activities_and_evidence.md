# Stage 8 activities and evidence

UG and PG | One evolving group project | Complete this blank record using the Stage 8 handout.

All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage08/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. The Stage 8 preparation utility is supplied or run by teaching staff when Stage 8 begins. Follow your tutor’s controlled workflow and the handout. If temporarily supplied, keep it outside the repository in a sibling Stage_8_Assets/ folder; exclude it from Git and the final submission.

Group/tutorial: Wednesday 2.30 to 4.30, Group 2
Members and UG/PG cohorts: Junaid Sayani (junaidSayani1) PG, Dominic (DominicRDA-uc) UG, Juliann (Jules-tryingtocode) UG, Aditti UG
Record owner / contribution links for each member: Record owner Dominic (DominicRDA-uc). Contribution links in section I.

Use concise results and accessible artefact links rather than copying entire logs. Keep human-first entries before consulting GitHub Copilot. Link shared evidence once; do not repeat it across sections. No entries below are specimen answers or claimed results.

## A. Tutorial activities

### A.1 Classify all five statements
For each, choose symptom, evidence or hypothesis/opinion, and explain your reason. These are discussion statements, not confirmed diagnoses.
- Appointment disappears after cancellation.
- The data-store removal path is probably being called.
- The failing test shows store.find_appointment('A1') returns None.
- The service layer is badly designed.
- Traceback points to smartcare/services.py line 42 in the example.
The example line number is illustrative; inspect the actual line in your run. The removal hypothesis must be tested against the current project, which has no public delete operation.

Response and reason: "Appointment disappears after cancellation" is a symptom because it describes the observed behaviour without explaining why it occurs. "The data-store removal path is probably being called" is a hypothesis/opinion because it proposes a possible cause that requires investigation. "The failing test shows store.find_appointment('A1') returns None" is evidence because it is a specific observed result from a test run. "The service layer is badly designed" is a hypothesis/opinion because it is a judgment rather than an observed fact. "Traceback points to smartcare/services.py line 42 in the example" is evidence because it records information produced by the traceback, although the actual project line number must be verified.

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: For the cancelled-history scenario, FR-07 and AC-05.2 state that cancelled appointments must remain retrievable, so I expected A1 to remain stored and findable after cancellation. Observed behaviour was that A1 remained in list_appointments() with status CANCELLED, but find_appointment('A1') returned None and the service layer raised LookupError. Minimal reproduction: create a store, register a patient and practitioner, book A1, cancel A1, then compare list_appointments() with both store and service lookups. Initial hypothesis: cancellation removed the appointment from storage. This was later disproved because A1 was still in list_appointments() after cancelling, which pointed instead to the lookup logic incorrectly filtering cancelled appointments. Evidence to inspect: find_appointment() in data_store.py, appointment status values, and whether the appointment remains present in the store collection.

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: If a test expects cancelled appointments to be deleted, the test should be changed, because FR-07 requires appointment history to be retained and retrievable after cancellation. The implementation should continue to preserve cancelled records because the requirement is the authoritative source of expected behaviour. A test expecting different practitioners at the same time to conflict does not reflect AC-04.2, which explicitly permits bookings for different practitioners at the same datetime. Therefore such a test would also be a test defect rather than evidence of a product defect.

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: The hypothetical method contains several code smells: duplicate status strings (magic values), direct collection manipulation, mixed responsibilities, excessive nesting and printing inside business logic. Small refactorings include extracting helper methods, replacing duplicated status strings with AppointmentStatus, separating validation from workflow logic and reducing nested conditionals with guard clauses while preserving behaviour. Renaming appt to appointment is refactoring, extracting a repeated conflict helper is refactoring, adding rescheduling is a feature, restoring retained cancellation lookup is a repair, and replacing a magic status string with the existing enum is refactoring. The externally observable behaviour must remain unchanged for all valid and invalid inputs when performing refactoring.

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: In test_cancel_appointment_with_valid_id, the failure is LookupError: Appointment not found. The expected result is that the cancelled appointment is returned, while the observed result is that lookup fails after cancellation. The failure occurs in tests/test_services/appointment_service_test.py and follows the path test → AppointmentService.find_appointment() → SmartCareDataStore.find_appointment(). The supporting requirements are FR-07, FR-08 and AC-05.2.

Ranked causes: (1) find_appointment() excludes cancelled appointments from lookup, (2) cancellation removes the appointment from storage, (3) the service uses the wrong appointment ID or a different store instance. Distinguishing checks are: inspect the lookup condition, compare list_appointments() before and after cancellation, and verify appointment IDs and store identity. A traceback identifies where a failure appeared but does not prove the root cause because multiple defects can produce the same failure.

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: Changing code immediately after seeing a failure is risky because the real cause has not yet been established. An engineer should first gather evidence, identify expected behaviour from requirements, create and test hypotheses, and isolate the defect. Otherwise a change may hide symptoms, introduce new faults or fix the wrong problem.


Classification responses (1–5, each with reason): See A.1 above.
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: See A.2 above.
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: See A.5 above.

## B. Stage 7 baseline and safe preparation

- Stage 7 code SHA and requirement baseline: 22651192e749561fc19595a07f97df493f96b174 (main after the Stage 7 merge, PR #8 at 81c62d7, plus a README and evidence only commit). SmartCare A3 requirements baseline revision 2.
- Baseline test command / working directory / observed result / evidence: python -m pytest -q in project/ on 2265119: 17 passed (Python 3.14.3, pytest 8.3.5).
- Clean preparation SHA if a record-only commit followed Stage 7: 2265119 is a README and evidence only commit after the PR #8 merge (81c62d7). It is the baseline the preparation tool checked (Baseline Git SHA 22651192e749561fc19595a07f97df493f96b174).
- Branch and preparer / how teammates obtained this branch: debug/stage08, prepared by tutor Pranav Gupta on 6 Nov 2026 and pushed to the shared repository. Main was left unchanged. Each member runs git fetch origin, then git switch --track origin/debug/stage08, and confirms with git branch --show-current.
- Downloaded tool version, source SHA256 and --check outcome: Stage 8 preparation utility version 1.1, run by the tutor on his machine (not downloaded by students). The check output was: "Stage 8 tool 1.1; preflight PASS; baseline SHA256 b4a1993e878c59a9df5e9055320702b2d318c5b6055bb1693a3afc25cd8fd375; Baseline Git SHA 22651192e749561fc19595a07f97df493f96b174; CHECK ONLY: project unchanged; both proposed fault signatures verified in a temporary copy"
- --apply and --verify output summaries / artefact references: The apply output was: "PREPARED: F8-01 practitioner conflict; F8-02 retained-history lookup. Verified expected failures: test_f8_01_conflict; test_f8_02_history (2 failed). Backup/hash recorded in .stage8_faults". The verify output was: "VERIFIED: exactly 2 expected failures; both approved symptom signatures present". Source: tutor's email to the group, 6 Nov 2026.
- Bounded diff inspected and recovery location (not committed): Preparation commit 5258397 changes only project/smartcare/data_store.py (11 insertions, 18 deletions). The tool's recovery backup (.stage8_faults/) stayed on the tutor's machine, is excluded by .gitignore and is not in the repository.
- Prepared faulty-state commit SHA: 525839749ec64f98f3e752d69230ce0787b9834e
- Preparation or recovery issues and resolution, if any: None during preparation. On 7 Nov 2026 commit fc37537 accidentally replaced this whole record with only the two section E entries. The following commit restored the full template, header and section B with section E kept word for word, and added sections C and D.
- Initial prepared full-suite command / result / key failures: python -m pytest -q in project/ on 5258397: 3 failed, 14 passed. Failing: tests/test_starter.py::test_conflict_rule_and_different_practitioner, tests/test_services/appointment_service_test.py::test_cancel_appointment_with_valid_id and tests/test_services/appointment_service_test.py::test_invalid_transition_appointment. The tool's own check tests reported 2 failures (one per defect). Our existing suite shows 3 failing tests across the two defects.

## C. F8-01 diagnosis and repair

- Symptom / observed behaviour: A second SCHEDULED booking for the same practitioner (D1) at exactly the same datetime (2026-10-01 09:00) is accepted instead of rejected. Calling the store directly, has_practitioner_conflict('D1', datetime(2026, 10, 1, 9)) returned False while A1 was SCHEDULED for D1 at that time.
- Expected behaviour and requirement: The second booking for D1 at 09:00 must raise ValueError and leave the stored appointments unchanged (FR-05, BR-05, AC-04.1). A booking for a different practitioner (D2) at the same time must still be accepted (AC-04.2). No patient conflict or duration overlap rule applies.
- Minimal synthetic reproduction steps: 1. Create one SmartCareDataStore. 2. Register patients P1 and P2 and practitioners D1 and D2. 3. Book A1 for P1 with D1 at 2026-10-01 09:00. 4. Book A2 for P2 with D1 at the same datetime. Expected: ValueError, and list_appointments() still holds only A1. Observed: the booking is accepted. 5. Book A3 for P2 with D2 at the same datetime. Expected: accepted.
- Meaningful failing test path/name and exact relevant failure: tests/test_starter.py::test_conflict_rule_and_different_practitioner, line 127, "Failed: DID NOT RAISE <class 'ValueError'>". New regression test: see G.
- Human hypothesis and intended checks: see E, F8-01.
- Supported root cause and inspected code/runtime evidence: In has_practitioner_conflict() in smartcare/data_store.py, the condition appointment.practitioner.practitioner_id != practitioner_id is reversed. Runtime evidence for A1 (D1, 2026-10-01 09:00, scheduled) checked against D1 at 09:00: id != exclude True, practitioner != D1 False, time == True, status == scheduled True, and a.data_store is s True. Only the practitioner condition blocks the conflict. See F8-01 in section F.
- Smallest justified fix / diff / why other behaviour is preserved: One operator changed on one line of has_practitioner_conflict(): appointment.practitioner.practitioner_id != practitioner_id became appointment.practitioner.practitioner_id == practitioner_id. This restores the BR-05 rule that a conflict needs the same practitioner. The other three conditions (excluded appointment ID, exact datetime, SCHEDULED status) are unchanged, so a different practitioner at the same time is still allowed (AC-04.2), a cancelled appointment still does not block the slot, and the exclude_appointment_id behaviour is preserved. No service, domain or test code was changed.
- Repair SHA / focused verification result: 3c6dbab (https://github.com/DominicRDA-uc/st1-assignment-3/commit/3c6dbab). python -m pytest tests/test_regressions.py in project/: 1 failed, 1 passed (test_f8_01 now passes, test_f8_02 still fails as expected). Full suite: 3 failed, 16 passed, and the 3 remaining failures are all F8-02.

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: After cancel_appointment('A1') succeeds (the same object is returned with status CANCELLED), the appointment can no longer be found. The service find_appointment('A1') raises LookupError, because the store find_appointment('A1') returns None, even though list_appointments() still contains A1 with status CANCELLED.
- Expected behaviour and requirement: A cancelled appointment stays stored and retrievable in the same session. The store find_appointment('A1') must return the same CANCELLED object, and the service find_appointment('A1') must return it rather than raise LookupError (FR-06, FR-07, FR-08, BR-07, AC-05.2). Cancelling A1 a second time must raise ValueError without changing its status (AC-05.3).
- Minimal synthetic reproduction steps: 1. Create one SmartCareDataStore. 2. Register patient P1 and practitioner D1. 3. Book A1 for P1 with D1 at 2026-10-01 09:00. 4. Cancel A1. 5. Check the status of the returned object, list_appointments(), store find_appointment('A1') and service find_appointment('A1'). Observed: status CANCELLED, list [('A1', 'CANCELLED')], store find None, service find LookupError.
- Meaningful failing test path/name and exact relevant failure: tests/test_services/appointment_service_test.py::test_cancel_appointment_with_valid_id, line 35, "LookupError: Appointment not found" raised at smartcare/services.py:139. Also test_invalid_transition_appointment, line 64: the repeated cancel raises LookupError instead of the expected ValueError, because A1 cannot be found. New regression test: see G.
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: In find_appointment() in smartcare/data_store.py, the condition appointment.status.value != "cancelled" excludes cancelled appointments from lookup. Runtime evidence after booking and cancelling A1: same object kept True, id repr 'A1', status value 'cancelled', id == A1 True, status != cancelled False, a.data_store is s True, store find None. The record is retained and only the status filter blocks the lookup. See F8-02 in section F.
- Smallest justified fix / diff / why other behaviour is preserved: Removed only the extra condition appointment.status.value != "cancelled" from find_appointment(), so the loop now matches on appointment ID alone. This restores the contract "return the stored appointment or None" for every status, as FR-07 and AC-05.2 require. The blank and invalid ID check that raises ValueError is unchanged, a valid unknown ID still returns None, the same stored object is returned (no copy), and Appointment.cancel() still rejects a repeated cancel, so AC-05.3 is preserved. No service, domain or test code was changed.
- Repair SHA / focused verification result: 2cb31d1 (https://github.com/DominicRDA-uc/st1-assignment-3/commit/2cb31d1). python -m pytest tests/test_regressions.py in project/: 2 passed. Full suite: 19 passed.

## E. Human-first hypotheses

Complete both entries BEFORE Copilot. C/D supply observed/expected/reproduction/test; retain those initial facts and link them here.

### F8-01 human entry
Likely cause and why plausible: I think has_practitioner_conflict() in data_store.py contains an incorrect practitioner comparison. The method is intended to detect another SCHEDULED appointment for the same practitioner at the same time (FR-05, BR-05, AC-04.1). However, the practitioner condition appears to use != (not equal), so it only matches appointments belonging to a different practitioner. This is the opposite of the business rule and would prevent genuine conflicts from being detected.
Evidence intended to inspect / competing explanation / discriminating check: After booking A1 with D1 at 2026-10-01 09:00, calling has_practitioner_conflict('D1', datetime(2026, 10, 1, 9)) directly printed "conflict? False", even though D1 already had a SCHEDULED appointment at that time. Competing explanation: the booking service does not call has_practitioner_conflict() correctly, so the fault would be in the service layer. Discriminating check: calling the store method directly, bypassing the service. Because the method itself returned False where a conflict exists, the fault is inside has_practitioner_conflict(), not the service.
Member and saved sequence/time or commit showing this preceded consultation: Dominic (DominicRDA-uc), 7 Nov 2026; recorded in this commit before any Copilot prompt for Stage 8. Disclosure: Claude (AI assistant) suggested the discriminating checks and guiding questions and formatted this entry. The hypothesis was reached by Dominic from his own runs and reading of data_store.py. No GitHub Copilot use before commit fc37537 (7 Nov 2026, 22:15), where this entry was first recorded.

### F8-02 human entry
Likely cause and why plausible: I think find_appointment() in data_store.py incorrectly filters appointments by status as well as by appointment ID. Under FR-07 and AC-05.2, a cancelled appointment must remain retrievable in the current session. The evidence shows A1 remains stored after cancellation, but find_appointment('A1') returns None, so the method appears to exclude cancelled appointments.
Evidence intended to inspect / competing explanation / discriminating check: After booking and cancelling A1, the store printed "store list: [('A1', 'CANCELLED')]" and "store find: None". Competing explanation: cancellation deleted the appointment record. Discriminating check: comparing list_appointments() with find_appointment('A1'). Because A1 is still in the list while the lookup returns None, the record was not removed; the fault is in find_appointment().
Member and saved sequence/time or commit showing this preceded consultation: Dominic (DominicRDA-uc), 7 Nov 2026; recorded in this commit before any Copilot prompt for Stage 8. Disclosure: Claude (AI assistant) suggested the discriminating checks and guiding questions and formatted this entry. The hypothesis was reached by Dominic from his own runs and reading of data_store.py. No GitHub Copilot use before commit fc37537 (7 Nov 2026, 22:15), where this entry was first recorded.

## F. GitHub Copilot prompts, findings and human decisions

Use the full handout prompt separately for BOTH defects, after E. Keep each actual prompt or accessible reference; include observed behaviour, expected behaviour, reproduction, failing test, human hypothesis, relevant code, three ranked causes and discriminating checks, with the no-rewrite/no-invented-requirements constraints.

### F8-01 Copilot review
Actual prompt / output reference and member: Dominic (DominicRDA-uc), 7 Nov 2026, GitHub Copilot Chat in VS Code, Ask mode, new chat. Its reply showed no workspace file reads. The prompt used the exact handout section 7 structure (observed behaviour, expected behaviour, steps to reproduce, failing test, my hypothesis, relevant code, task with the three constraints), filled with the evidence from sections C and E and the current has_practitioner_conflict() and book_appointment() code. The prompt and full reply are kept in Dominic's Stage 8 notes.
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Suggestion 1: the practitioner comparison is reversed (appointment.practitioner.practitioner_id != practitioner_id excludes the matching practitioner). Evidence check suggested: print each predicate for A1 separately. Observed after running it: id != exclude True, practitioner != D1 False, time == True, status == scheduled True. Only the practitioner condition fails for a genuine same practitioner conflict. Verdict: correct. Decision: accept, because the printed predicates show this single condition is the reason the method returns False.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Suggestion 2: the stored appointment's runtime fields do not match the checked values (wrong practitioner, datetime or status). Evidence check suggested: read list_appointments() from the same store and compare the fields. Observed: "stored: A1 D1 2026-10-01 09:00:00 scheduled", which exactly matches the arguments D1 and datetime(2026, 10, 1, 9). Verdict: wrong. Decision: reject, because the stored data matches the call.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Suggestion 3: the service and the inspected store or code are different runtime instances or versions. Evidence check suggested: confirm AppointmentService.data_store is the store holding A1. Observed: "a.data_store is s: True", and the direct store call on that same store already returned False. Copilot itself rated this weaker. Verdict: wrong. Decision: reject, because the wiring is correct and wiring cannot explain the direct call result.
Final human conclusion and comparison with initial hypothesis: The root cause is the reversed practitioner condition in has_practitioner_conflict() in data_store.py. It uses != where the contract (BR-05, "another SCHEDULED appointment at this practitioner/time") needs ==, so a same practitioner booking is never seen as a conflict, and book_appointment() never raises ValueError. This is the same as my initial hypothesis in section E. Copilot's top suggestion agreed with it, and its two alternatives were tested and ruled out by the predicate printout. Copilot did not run any code. The checks were run by Dominic.

### F8-02 Copilot review
Actual prompt / output reference and member: Dominic (DominicRDA-uc), 7 Nov 2026, GitHub Copilot Chat in VS Code, Ask mode, new chat, using the same handout section 7 structure filled with the evidence from sections D and E and the current find_appointment() and Appointment.cancel() code. Limitation: although Ask mode cannot edit files or run commands, Copilot used its read-only workspace tools. Before answering, it read this Stage 8 record (including the section E hypothesis), data_store.py, services.py, domain.py and the test files, so its ranking was not independent of the human hypothesis. It made no edits. The prompt and full reply are kept in Dominic's Stage 8 notes.
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Suggestion 1: the store lookup filters out cancelled appointments (find_appointment() requires status.value != "cancelled"). Evidence check suggested: compare A1's appointment_id and status.value with the lookup conditions. Observed: id repr 'A1', status value 'cancelled', id == A1 True, status != cancelled False, store find None. Only the status condition fails. Verdict: correct. Decision: accept, because the printed conditions show the status filter alone causes the None result.
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Suggestion 2: cancellation removes the record. Evidence check suggested: compare the stored collection before and after cancellation, including object identity. Observed: same object kept True (the listed appointment after cancelling is the booked object), and list_appointments() still contains A1. Copilot itself rated this a poor fit. Verdict: wrong. Decision: reject, because the record is retained and only the lookup fails.
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: Suggestion 3: a mismatched ID or a different store. Evidence check suggested: confirm the exact ID, the lookup argument and that the service uses the same store. Observed: id repr 'A1' matches the argument exactly, and a.data_store is s True. Verdict: wrong. Decision: reject, because the ID and store both match.
Final human conclusion and comparison with initial hypothesis: The root cause is the extra condition appointment.status.value != "cancelled" in find_appointment() in data_store.py. It hides any CANCELLED appointment from lookup, which contradicts FR-07 and AC-05.2 and the contract "return the stored appointment or None". The service then turns that None into LookupError. This is the same as my initial hypothesis in section E. Copilot agreed, but because it read the record first, its agreement is weaker evidence than for F8-01. The diagnosis rests on the runtime checks Dominic ran. Copilot did not run any code.

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | 7c0455f with the new project/tests/test_regressions.py added (uncommitted when run, committed together with this record update) | python -m pytest tests/test_regressions.py -v in project/ (Python 3.14.3, pytest 8.3.5) | FAILED test_f8_01_same_practitioner_same_time_is_rejected at line 46: "Failed: DID NOT RAISE <class 'ValueError'>". Existing test_starter.py::test_conflict_rule_and_different_practitioner fails the same way at line 127. |
| F8-01 after repair | 3c6dbab | python -m pytest tests/test_regressions.py -v and python -m pytest -q in project/ (Python 3.14.3, pytest 8.3.5) | test_f8_01 PASSED, test_f8_02 still FAILED (expected, F8-02 not yet repaired). Full suite 3 failed, 16 passed. test_starter.py::test_conflict_rule_and_different_practitioner now passes. |
| F8-02 before repair | 7c0455f with the new project/tests/test_regressions.py added (uncommitted when run, committed together with this record update) | python -m pytest tests/test_regressions.py -v in project/ (Python 3.14.3, pytest 8.3.5) | FAILED test_f8_02_cancelled_appointment_stays_findable at line 86: "AssertionError: assert None is <smartcare.domain.Appointment object>" where None = data_store.find_appointment('A1'). Existing test_cancel_appointment_with_valid_id (line 35) and test_invalid_transition_appointment (line 64) fail with "LookupError: Appointment not found". |
| F8-02 after repair | 2cb31d1 | python -m pytest tests/test_regressions.py -v in project/ | 2 passed. test_cancel_appointment_with_valid_id and test_invalid_transition_appointment now pass. |
| Full suite after both repairs, before refactor | 2cb31d1 | python -m pytest -q in project/ | 19 passed (17 Stage 7 tests plus the 2 new regression tests) |

Full suite before any repair, with the regression tests added: python -m pytest -q in project/ on the same code: 5 failed, 14 passed. The 5 failures are the 2 new regression tests plus the 3 existing failing tests listed in section B.

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: test_f8_01 books A1 for D1 at 09:00, then uses pytest.raises(ValueError) on a second D1 booking at the same time, so an accepted duplicate booking fails the test. It then asserts list_appointments() == [first] and find_appointment('A2') is None, which proves a rejected booking leaves no partial state (NFR-01). Finally it books D2 at the same time and asserts it is SCHEDULED, so a repair that wrongly blocks different practitioners would also fail (AC-04.2). test_f8_02 asserts the cancelled object is the booked object and is CANCELLED, then checks the store lookup (is booked, not None) and the service lookup (is booked, not LookupError) separately, so the two layers are not confused. It also asserts the appointment is still listed, and that a second cancel raises ValueError with the status still CANCELLED (AC-05.3), which protects the guarded transition. Each test uses its own fresh store and synthetic data.
Test authorship disclosure: the test code in tests/test_regressions.py was written by Claude (AI assistant) from the requirements and reproduction steps in sections C and D. Dominic ran it, checked each assertion against the requirements and confirmed it fails for the intended reason before repair. Claude also checked that both tests pass on the pre-fault Stage 7 code (2265119, 19 passed), which shows they test the published contract and not an invented rule.
Unrelated failures investigated / resolution: Not applicable. Every failure seen on the prepared branch belonged to F8-01 or F8-02, and all of them pass after the two repairs.

## H. Refactoring decision and before/after verification

Smell and exact location: Magic status string in has_practitioner_conflict() in project/smartcare/data_store.py: appointment.status.value == "scheduled" compares against a hard coded string instead of the existing AppointmentStatus enum. A typo in the string would silently break the conflict rule, and it duplicates knowledge that already lives in AppointmentStatus.
Small proposed structural change / why justified: Replace appointment.status.value == "scheduled" with appointment.status is AppointmentStatus.SCHEDULED, which is how domain.py and the rest of the code compare statuses (for example Appointment.cancel()). AppointmentStatus is already imported in data_store.py, so no new import or dependency is needed. This is a refactoring and not a repair, because the result is the same for every status value. Process note: this plan was written in the local record before the code was edited (22:47 on 7 Nov 2026, edit at 22:48), but by mistake it was not committed until after the refactor commit 85ec285. The history therefore does not prove the order, and this note records that honestly.
External behaviour to preserve / relevant tests: has_practitioner_conflict() must still return True only for another SCHEDULED appointment with the same practitioner at the exact same datetime, return False for CANCELLED or COMPLETED appointments and for a different practitioner, respect exclude_appointment_id and never mutate records. Protected by tests/test_regressions.py::test_f8_01_same_practitioner_same_time_is_rejected, tests/test_starter.py::test_conflict_rule_and_different_practitioner and the full suite (19 passed before the change, see G).
Before result: see G, full passing suite (2cb31d1, 19 passed).
Actual change / diff / separate refactor SHA: 85ec285 (https://github.com/DominicRDA-uc/st1-assignment-3/commit/85ec285). One line in has_practitioner_conflict(): appointment.status.value == "scheduled" became appointment.status is AppointmentStatus.SCHEDULED. No other file or line changed.
Focused and full after-refactor commands / working directory / results / evidence: Before (2cb31d1): python -m pytest tests/test_regressions.py -v in project/: 2 passed. python -m pytest -q: 19 passed. After (85ec285): the same two commands gave 2 passed and 19 passed (Python 3.14.3, pytest 8.3.5). test_starter.py::test_conflict_rule_and_different_practitioner and test_f8_01 both still pass, so same practitioner conflicts are still rejected and a different practitioner is still allowed.
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: Accepted. The check now uses the enum like the rest of the codebase, removing a magic string that a typo could silently break. The same tests pass before and after with identical results, and the conflict rule (same practitioner, exact time, SCHEDULED only, exclusion respected, no mutation) behaves the same. Behaviour is preserved.

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: https://github.com/DominicRDA-uc/st1-assignment-3/issues/9 (F8-01), https://github.com/DominicRDA-uc/st1-assignment-3/issues/10 (F8-02), https://github.com/DominicRDA-uc/st1-assignment-3/issues/11 (refactor). Owner of all three: Dominic. Scope limited to project/smartcare/data_store.py, the new project/tests/test_regressions.py and this record. No requirement, architecture or feature changes.
Branch / prepared, repair and refactor checkpoints: debug/stage08. Prepared faulty state 5258397 (B). Human hypotheses fc37537 (E). Regression tests failing before repair 65b07c2 (G). F8-01 repair 3c6dbab (C). F8-02 repair 2cb31d1 (D). Refactor 85ec285 (H).
PR link and another member's reviewer identity: Pull request from debug/stage08 into main opened by Dominic on 7 Nov 2026 (https://github.com/DominicRDA-uc/st1-assignment-3/pulls). Requested reviewer: Junaid Sayani (junaidSayani1). Review completed, PR approved and merged.
Key human feedback, difference from Copilot findings and response/outcome: Key human feedback, difference from Copilot findings and response/outcome: Junaid Sayani (myself) reviewed pull request #12. I agreed with the F8-01 and F8-02 root causes and with the one-line repairs and also agreed that the enum change is a refactor and not a new rule. It also matches the accepted Copilot suggestions in section F. No extra Copilot review was run on the pull request. The missing docstrings were noted and left as the limitation already recorded in section L, I did not request any code change as of now.

Actual review approval / merge evidence: Junaid Sayani (junaidSayani1) (me) approved pull request #12 on 8 Nov 2026 and merged it. https://github.com/DominicRDA-uc/st1-assignment-3/pull/12 
Merge commit ed3d8f0d38087bbb38c80aa9e3fde03384d36711. No code change was requested.

Integrated code SHA and team pull/retest command / working directory / result: Integrated code SHA ed3d8f0d38087bbb38c80aa9e3fde03384d36711. python -m pytest in project/ gave us: 19 passed 0 failed. 

Evidence-only later SHA / explanation if different: 
Each member's substantive contribution and artefact: 
Dominic (DominicRDA-uc) diagnosed and repaired F8-01 and F8-02, added project/tests/test_regressions.py, and did the enum refactor. 

Junaid Sayani (junaidSayani1) reviewed the instructions files, design decisions, ran regression tests, unit tests, all the repairs and refactors, finally left a review and merged pull request #12.

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? The least-supported suggestion was that the service and store might have been different runtime instances in F8-01. It was plausible initially, but direct verification showed a.data_store is s was True, so the explanation lacked supporting evidence.
2. What evidence changed your group's view? The most important evidence was the runtime inspection of the predicates inside has_practitioner_conflict() and find_appointment(). Seeing that only a single condition evaluated incorrectly isolated the true root cause and ruled out alternative explanations.
3. How did regression tests protect the refactoring? The regression tests captured the required behaviour before the refactor and were re-run afterward. Because all tests passed before and after the change, they demonstrated that replacing the magic string with the enum did not alter externally visible behaviour.

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: Determine the expected behaviour from requirements, gather evidence, reproduce the problem, and form a testable hypothesis before making changes.

2. Where should expected behaviour come from during debugging?

Response: Expected behaviour should come from requirements, acceptance criteria, business rules and agreed specifications rather than assumptions.

3. What is a debugging hypothesis?

Response: A debugging hypothesis is a proposed explanation for a failure that can be tested with evidence and investigation.

4. What is a regression test and why is it retained?

Response: A regression test captures behaviour that previously failed and is retained to ensure the same defect does not reappear in future changes.

5. What is meant by root cause?

Response: The root cause is the underlying defect that directly produces the observed failure or incorrect behaviour.

6. What is refactoring?

Response: Refactoring is changing the internal structure of code to improve maintainability without changing externally observable behaviour.

7. What is a swallowed exception?

Response: A swallowed exception is an exception that is caught and suppressed without being properly handled, reported or re-raised.

8. What is a code smell?

Response: A code smell is a structure or pattern in code that suggests potential design or maintainability problems even if the code still functions correctly.

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: They should be treated as hypotheses that require verification with requirements, code inspection and runtime evidence before acceptance.

10. What is the Stage 8 engineering rule?

Response: Diagnose using evidence first, identify the supported root cause, apply the smallest justified repair, and verify the result with regression and full-suite testing.

## L. Completion and handover

- [X] Existing project, earlier tests and stage records preserved.
- [X] Passing Stage 7 SHA and safe preparation details recorded.
- [X] Both defects reproduced with meaningful failing tests.
- [X] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [X] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [X] One genuine refactor verified under passing before/after tests.
- [X] Human PR review, feedback resolution and integrated retest recorded.
- [X] Tutorial, three reflections and ten formative responses complete.
- [X] Local recovery metadata excluded from submitted source.
- [X] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: ed3d8f0d38087bbb38c80aa9e3fde03384d36711. python -m pytest -q in project/: 19 passed.

Submitted SHA and evidence-only difference if any: ed3d8f0d38087bbb38c80aa9e3fde03384d36711

Unresolved issues or incomplete checks / owner / next action: Docstrings on find_appointment() and has_practitioner_conflict() are still missing. I (Junaid) have approved without requiring that change, only due to time limitations with other members, and have also mentioned in review too that Docstring serve as important documentation.

Handover note: Stage 8 code is on main at ed3d8f0. Stage 9 can use that code.