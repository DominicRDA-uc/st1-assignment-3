# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: <!-- complete -->
Members and responsibilities: <!-- complete -->
Stage 8 integrated SHA, command, working directory and actual result: <!-- complete -->

## A. Tutorial activities

### A1 Session state classification

| Information | Required session/domain or transient state? | Requirement or reason |
|---|---|---|
| Patient identity | Required session/domain state | FR-01 and FR-02, BR-01, needed to find the patient and link bookings to a real patient, core object |
| Appointment history | Required session/domain state | FR-07, BR-06 and BR-07, cancelled appointments stay in the store for the session |
| Temporary menu choice | Transient state | only needed for one pass of the menu loop, not a domain record |
| Practitioner specialty | Required session/domain state | FR-03, part of the registered practitioner record |
| Debug print output | Transient state | only for our/developer checking/debugging, no requirement needs it and it is not stored |
| Appointment status | Required session/domain state | FR-06 and BR-08, needed for cancellation rules, conflict checks and status filtering, and status transitions.|

What is intentionally lost on exit? All patients, practitioners, appointments and cancelled history are lost (for now), this is because the we are not storing anything in database (or any persisting data store), it is in memory only, so a new session always starts empty and this is expected for now. And ofcourse all the transient states like menu input etc is also lost which is ideal, and will remain like this even with DB.

### A2 Interface and domain data plan

Plan before AI. This replaces schema/key design; no database tables are required.

| Function or component | Explicit inputs and types | Outputs | Responsibility and validation | Domain source / existing constraint |
|---|---|---|---|---|
| appointment_sort_key | Input: appointment: Appointment | tuple[datetime, str]  date_time then appointment_id | pure key used as sorting named composite key to sort, no validation needed because Appointment is already validated, no side effects | Appointment.date_time is a precise date-time slot of appointment and appointment_id is non-blank valid text |
| select_appointments | appointments: list[Appointment], practitioner_id: str, status: AppointmentStatus or None | new list sorted by appointment_sort_key | pure, assumes valid objects and filter values, does not check registration, does not change the source(input list) or do input/output | practitioner comes from appointment.practitioner.practitioner_id, status from the AppointmentStatus enum, None means return every status by default|
| Service listing | practitioner_id: str, status: AppointmentStatus or None, and the shared store held by the service | new list of Appointment objects, empty list when nothing matches | finds the practitioner through the store, ValueError for blank or invalid ID, LookupError for valid unknown ID, ValueError if status is not an enum, gets list_appointments, passes the registered practitioner's ID to the query | store object, IDs are trimmed and case-sensitive, find returns None when absent so the service raises LookupError |
| Console | typed text for IDs, names, specialty, date/time and status (user end's input output) | printed messages and formatted appointments list displayed | prompts the user, parses date/time with parse_date_time, converts blank status to None and other text to the relevant matching enum, calls services, catches ValueError and LookupError, prints the message and returns to the menu, holds no domain rules and checks no invariants and processes no business logic | calls services only, with one store and one set of services for the whole session |

Relate patient ID/name, practitioner ID/name/specialty, and appointment ID/actual participants/date_time/status to the existing contracts: 
Patient ID, practitioner ID and appointment ID are trimmed non-blank text and read-only after creation. These are major domain invariants for each object instance associated with, they should not be invalid or changed/modified.

Names and specialty are trimmed non-blank text, Appointment holds the actual Patient and Practitioner objects from the shared store (dont make any copies of it), date_time is the precise date and time (to minute), status is an AppointmentStatus enum value, so the new functions only read these existing fields and add no new fields or tables or  records, or modify object field count / validity.

### A3 Responsibility violations

| Conceptual case | Violation | Correct boundary and reason |
|---|---|---|
| Appointment.cancel reads input | The domain object/invariant function interacts with user, leaks with input, so it cannot be tested without typing/inputting and it leaks its rules with the interface | Appointment.cancel only checks the SCHEDULED rule and changes status from one valid domain object to another holding the invariant|
| Service prints/reads the menu | The service does presentation work and can no longer be reused or tested without the console, changing menu or the service changes the other part too destroying modularity | The console handles the printing and reading the menu, while presentation layer calls on function from service, which then coordinates registration, booking, cancellation and listing and returns results or throws errors |
| Query sorts its source in place | appointments.sort changes the incoming list order, which is a hidden side effect and breaks purity. This actually causes memory leaks and destroys the intended test cases and functionality from caller function | Use sorted on the selected items (new list) so the source stays unchanged and a new list is returned |
| Store prints Appointment saved | The store does presentation work and fixes one message for every caller | The store's job  is to save, modify, retrieve the appointment (and other table/data record) object, it works only with data store (in-memory or persistence), the console's job is to  decide what to print and actually print it. |

### A4 Sorting comparison

For `appointments.sort(key=appointment_sort_key)` and `result = sorted(appointments, key=appointment_sort_key)`, predict source order, return value and result identity. Give a meaningful mutation check: appointments.sort(key=appointment_sort_key) changes the source order in place and returns None, so there is no result list and no new identity, result = sorted(appointments, key=appointment_sort_key) leaves the source order unchanged and returns a new list that is not the source, holding the same appointment objects, to catch accidental mutation I would snapshot (thru check_mutation func that holds the list in a tuple) the source order and each appointment's ID, practitioner, date_time and status before running the query, then after the query and a repeated call assert the snapshot is equal and result is not source.

Score-example prediction and explanation of passing the named key: the named key orders by score, then name, ordered is [('Chris', 5), ('Ali', 8), ('Mia', 8)] because the keys are (5, 'Chris'), (8, 'Ali') and (8, 'Mia'), Ali and Mia have the same score so the name breaks the tie, scores stays [('Mia', 8), ('Ali', 8), ('Chris', 5)] and ordered is not scores, key=score_key passes the function itself so sorted calls it once for every item, key=score_key() would call it straight away without a valid item and pass its result, which is not a function.

### A5 Exit question

Explain cancellation versus deletion, and checks for same-session lookup, all-status listing and SCHEDULED-only exclusion: cancellation changes the status of the appointment object to CANCELLED so the history stays (the object is retained in data store), deletion would remove the record and remove it, to check I would find the appointment by ID and see the same object with status CANCELLED, list the practitioner with no status and see the cancelled appointment included along all its appointments for the prac, then list with SCHEDULED only and see it omitted, because it is no longer scheduled.

## B. Human design and contracts

Complete before GitHub Copilot. Record any interface/integrity decision and its reasoning: The pure query only selects and sorts supplied valid objects, and the service checks the practitioner and status because it can reach the store, the service uses the registered practitioner's ID so accepted spaces around an ID do not give a misleading empty list, the service accepts only AppointmentStatus or None and the console converts text to the enum, no rule is invented for which error comes first when several inputs are wrong, and cancelled history is never deleted.

| Requirement | Input / session data | Operation and responsible component | Expected result or error | Test / evidence |
|---|---|---|---|---|
| QRY-01 | appointments for D1 and D2, practitioner_id D1 | select_appointments in queries.py | only D1 appointments, D2 is the control | test_queries.py practitioner ID based selection tests |
| QRY-02 | status AppointmentStatus | None, each enum value, and a status with no match | select_appointments | None selects every status record in the new list, an enum gives only that status, no match gives a new empty list | test_queries.py status tests |
| QRY-03 | appointments at different times and at an equal time with different IDs | select_appointments with appointment_sort_key | ascending date_time then appointment_id, source order and fields unchanged | test_queries.py order and snapshot tests |
| QRY-04 | known practitioner with no match, unknown ID, blank ID, status 'scheduled' | list_practitioner_appointments in services.py | empty list, LookupError, ValueError, ValueError | service tests, to be added in the service stage |
| FP-01 | the same inputs called twice | select_appointments | same result both times, no hidden state or input/output | test_queries.py repeat test and code inspection |
| FP-02 | empty, already sorted and unsorted lists | select_appointments | a new list each time holding the same unchanged objects | test_queries.py new list test |
| FP-03 | an appointment and a mixed list | appointment_sort_key | key returns date_time then appointment_id and sorting uses it | test_queries.py key tests |
| FR-09 | practitioner ID and optional status through the service | AppointmentService.list_practitioner_appointments | ordered list for the registered practitioner | service tests and tests/test_workflows.py |
| FR-01 to FR-08 | menu choices 1 to 7 with IDs, names, specialty and date/time | console.py calling the existing services | register, find, book, conflict rejection, cancel and find work and errors are shown | tests/test_workflows.py and the manual menu run |
| UI-01 | one session with P1, D1, D2, A1 and A2 | run_menu with one store and one set of services | the full sequence given in doc/handout works and ends with exit | console test and manual menu run |
| UI-02 | unknown choice, blank or unknown ID, duplicate, bad date/time, repeated cancel, bad status | run_menu | message shown, menu continues, no partial state | console test and manual menu run |

Cover QRY-01–04, FP-01–03, UI-01–02 and relevant FR-01–09. Explain empty versus unknown versus invalid, enum conversion, actual object identity, error handling and unchanged state on rejection: A known practitioner with nothing to show gives an empty list and no error (meaning that the practitioner is a valid object/ registered doctor but has no appointments scheduled), a valid ID that is not registered (no practitioner with that ID) raises LookupError, a blank or malformed ID or a status that is not an enum value raises ValueError and is never treated as no matches, the console turns blank status into None and the text scheduled, cancelled or completed into the enum before calling the service, results hold the same stored objects so identity can be checked with is, and after any rejected action the store is compared with its state before the action and the menu goes on to a successful command

## C. Implementation and query verification

| Requirement / test ID | Code location | Case and meaningful assertion | Actual result | Evidence link |
|---|---|---|---|---|
| | | | | |

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: <!-- response -->
What the tests do and do not establish: <!-- response -->

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | | | | |
| UI-02 invalid-input recovery | | | | |
| Automated service workflow | | | | |

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: <!-- reference -->
Actual prompt/context supplied: <!-- paste or accessible reference -->
Actual response: <!-- accessible reference -->

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| | | | | | |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: <!-- response -->

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? <!-- response -->
2. Which Copilot suggestion did you reject as over-engineering, and why? <!-- response -->
3. How did you prove cancelled appointments remain retrievable and listable in the same session? <!-- response -->

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? <!-- response -->
2. Which explicit inputs are needed, and why avoid a global store? <!-- response -->
3. How can a new list reuse Appointment objects safely? <!-- response -->
4. Why use a named key, and what breaks equal-time ties? <!-- response -->
5. How do default and explicit status filters differ? <!-- response -->
6. How do empty, unknown practitioner and invalid filter cases differ? <!-- response -->
7. Which console errors recover, and how is unchanged state checked? <!-- response -->
8. What is data integrity for registered participants, conflicts and history? <!-- response -->
9. What is Copilot's review role, and who verifies findings? <!-- response -->
10. How do pure functions and OOP responsibilities work together? <!-- response -->

## H. Review, completion and common handover

Issues and bounded branches: <!-- links -->
PR/diff and another-member human reviewer: <!-- actual links/name -->
Review responses and Copilot comparison: <!-- links -->
Integrated common Stage 9 SHA: <!-- complete -->
Full regression command, working directory, actual count/result and evidence: <!-- complete -->
README run instructions and scope/limitations: <!-- link -->
Unresolved issues and support/action: <!-- complete -->
UG common candidate / PG future branch plan: <!-- complete -->

- [ ] Query contracts, purity, new lists and named-key ordering verified.
- [ ] Service empty/unknown/invalid cases and cancellation history verified.
- [ ] Every console command and invalid-input recovery demonstrated.
- [ ] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [ ] Human design, Copilot critique, review and integration recorded honestly.
- [ ] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
