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

Response and reason: [complete]

### A.2 Build a debugging record
Choose the cancelled-history scenario or a same-practitioner/time booking. Before changing code, record expected behaviour, observed behaviour, minimal reproduction, a hypothesis and evidence to inspect. Use a requirement to justify the expectation. Keep the initial hypothesis even if later evidence disproves it.

Response and reason: [complete]

### A.3 Test defect or product defect
A test expects cancelled appointments to be deleted, but FR-07 says history must be retained. What should be changed? Explain why. Also decide whether a test expecting different practitioners at the same time to conflict reflects AC-04.2. Do not assume every failing test is correct.

Response and reason: [complete]

### A.4 Refactoring smell hunt
Consider a hypothetical 70-line AppointmentService method containing duplicate status strings, direct collection manipulation, printing, validation and four nested conditionals. Identify the smells and propose small refactorings that preserve required behaviour. The direct collection work replaces the old storage-specific scenario; use the existing SmartCareDataStore boundary. Do not implement an extra architecture.
Classify these proposed changes as refactoring, repair or feature: rename appt to appointment; extract a repeated conflict helper; add rescheduling; restore retained cancellation lookup; replace a magic status string with the existing enum. Explain the behaviour that must remain unchanged.

Response and reason: [complete]

### A.5 Traceback and hypothesis ranking
Using one actual failure, identify its exception/assertion, expected and observed values, test line, application call path and supporting requirement. List three plausible causes and rank them by fit with the available evidence. For each cause, name a check that could distinguish it from the others. Explain why a traceback alone does not establish the cause.

Response and reason: [complete]

### A.6 Exit question
Why is changing code immediately after seeing a failure often a poor debugging strategy?

Response and reason: [complete]


Classification responses (1–5, each with reason): [complete]
Tutorial debugging record — expected; observed; reproduction; hypothesis; evidence to inspect: [complete]
Traceback — exception/assertion; expected/observed values; test line; call path; requirement; ranked causes and discriminating checks: [complete]

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
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

## D. F8-02 diagnosis and repair

- Symptom / observed behaviour: After cancel_appointment('A1') succeeds (the same object is returned with status CANCELLED), the appointment can no longer be found. The service find_appointment('A1') raises LookupError, because the store find_appointment('A1') returns None, even though list_appointments() still contains A1 with status CANCELLED.
- Expected behaviour and requirement: A cancelled appointment stays stored and retrievable in the same session. The store find_appointment('A1') must return the same CANCELLED object, and the service find_appointment('A1') must return it rather than raise LookupError (FR-06, FR-07, FR-08, BR-07, AC-05.2). Cancelling A1 a second time must raise ValueError without changing its status (AC-05.3).
- Minimal synthetic reproduction steps: 1. Create one SmartCareDataStore. 2. Register patient P1 and practitioner D1. 3. Book A1 for P1 with D1 at 2026-10-01 09:00. 4. Cancel A1. 5. Check the status of the returned object, list_appointments(), store find_appointment('A1') and service find_appointment('A1'). Observed: status CANCELLED, list [('A1', 'CANCELLED')], store find None, service find LookupError.
- Meaningful failing test path/name and exact relevant failure: tests/test_services/appointment_service_test.py::test_cancel_appointment_with_valid_id, line 35, "LookupError: Appointment not found" raised at smartcare/services.py:139. Also test_invalid_transition_appointment, line 64: the repeated cancel raises LookupError instead of the expected ValueError, because A1 cannot be found. New regression test: see G.
- Human hypothesis and intended checks: see E, F8-02.
- Supported root cause and inspected code/runtime evidence: [complete after diagnosis]
- Smallest justified fix / diff / why other behaviour is preserved: [complete]
- Repair SHA / focused verification result: [complete]

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
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

### F8-02 Copilot review
Actual prompt / output reference and member: [complete]
1. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
2. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
3. Ranked suggestion / evidence check / observed evidence / correct, partly correct or wrong / accept, modify or reject with reason: [complete]
Final human conclusion and comparison with initial hypothesis: [complete]

## G. Failing to passing regression evidence

| Checkpoint | Code SHA or precise diff | Command and working directory | Actual result and artefact reference |
|---|---|---|---|
| F8-01 before repair | [complete] | [complete] | [complete] |
| F8-01 after repair | [complete] | [complete] | [complete] |
| F8-02 before repair | [complete] | [complete] | [complete] |
| F8-02 after repair | [complete] | [complete] | [complete] |
| Full suite after both repairs, before refactor | [complete] | [complete] | [complete] |

Explain how the assertions detect each relevant incorrect result and protect previous behaviour: [complete]
Unrelated failures investigated / resolution: [complete or not applicable with reason]

## H. Refactoring decision and before/after verification

Smell and exact location: [complete]
Small proposed structural change / why justified: [complete before editing]
External behaviour to preserve / relevant tests: [complete]
Before result: see G, full passing suite.
Actual change / diff / separate refactor SHA: [complete]
Focused and full after-refactor commands / working directory / results / evidence: [complete]
Result — accepted, revised or rejected / reason / behaviour-preservation conclusion: [complete]

## I. Git, human review and integration

Issues for both defects / refactor scope and owners: [complete]
Branch / prepared, repair and refactor checkpoints: [link B/C/D/H]
PR link and another member's reviewer identity: [complete]
Key human feedback, difference from Copilot findings and response/outcome: [complete]
Actual review approval / merge evidence: [complete]
Integrated code SHA and team pull/retest command / working directory / result: [complete]
Evidence-only later SHA / explanation if different: [complete or not applicable]
Each member's substantive contribution and artefact: [complete]

## J. Required reflections

1. Which Copilot diagnosis appeared convincing but lacked evidence? [complete; report honestly if none and discuss the least-supported real suggestion]
2. What evidence changed your group's view? [complete]
3. How did regression tests protect the refactoring? [complete]

## K. Ten formative questions

1. What should an engineer do before changing code in response to a failure?

Response: [complete]

2. Where should expected behaviour come from during debugging?

Response: [complete]

3. What is a debugging hypothesis?

Response: [complete]

4. What is a regression test and why is it retained?

Response: [complete]

5. What is meant by root cause?

Response: [complete]

6. What is refactoring?

Response: [complete]

7. What is a swallowed exception?

Response: [complete]

8. What is a code smell?

Response: [complete]

9. How should GitHub Copilot-generated debugging diagnoses be treated?

Response: [complete]

10. What is the Stage 8 engineering rule?

Response: [complete]

## L. Completion and handover

- [ ] Existing project, earlier tests and stage records preserved.
- [ ] Passing Stage 7 SHA and safe preparation details recorded.
- [ ] Both defects reproduced with meaningful failing tests.
- [ ] Both human hypotheses recorded before Copilot; actual suggestions evaluated with evidence.
- [ ] Supported causes and minimal repairs explained; focused and full regression results recorded.
- [ ] One genuine refactor verified under passing before/after tests.
- [ ] Human PR review, feedback resolution and integrated retest recorded.
- [ ] Tutorial, three reflections and ten formative responses complete.
- [ ] Local recovery metadata excluded from submitted source.
- [ ] Same project and full suite ready for Stage 9 after Stage 8 integration, verification and recording.

Verified integrated code SHA / result: see I.
Submitted SHA and evidence-only difference if any: [complete]
Unresolved issues or incomplete checks / owner / next action: [complete]
Handover note: [complete]