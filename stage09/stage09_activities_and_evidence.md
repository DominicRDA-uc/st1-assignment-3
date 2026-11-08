# Stage 9 activities and evidence

Common UG and PG record. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied record in stage09/ in your EXISTING repository. Preserve project/, all earlier tests, records and responses. Do not download another starter or copy staff solutions. Use the Stage 9 handout and Overview/revision 2 baseline. Keep responses concise and link accessible artefacts; do not paste entire logs or private peer ratings.

Group: Wednesday 2.30 to 4.30, Group 2, repository https://github.com/DominicRDA-uc/st1-assignment-3
Members and responsibilities: Junaid Sayani (junaidSayani1, PG), Dominic (DominicRDA-uc, UG), Juliann (Jules-tryingtocode, UG), Aditti (UG). The Stage 9 work was split into three tasks, the pure queries (branch stage9/Task/Pure_query_implementation), the service listing (branch stage9/Task/practitioner_appointments_listing) and the console menu (branch stage9/Feature/Console_based_menu). 
Stage 8 integrated SHA, command, working directory and actual result: ed3d8f0d38087bbb38c80aa9e3fde03384d36711 (merge of PR #12), python -m pytest -q in project/, 19 passed. The Stage 9 branches were started after the Stage 8 evidence update c0fabde, and the first Stage 9 run on that code gave 19 passed before any new tests were added.

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
| QRY-01, test_only_requested_practitioner_is_selected | queries.py select_appointments | D2 is a control, every returned appointment has practitioner D1 | PASSED | project/tests/test_queries.py |
| QRY-01, test_practitioner_id_is_case_sensitive | queries.py select_appointments | 'd1' selects nothing and returns an empty list | PASSED | project/tests/test_queries.py |
| QRY-02, test_default_includes_all_status | queries.py select_appointments | no status given, the result holds every AppointmentStatus value | PASSED | project/tests/test_queries.py |
| QRY-02, test_explicit_status_filters | queries.py select_appointments | each enum status returns only appointments with that status | PASSED | project/tests/test_queries.py |
| QRY-02, test_no_match_returns_new_empty_list | queries.py select_appointments | no match gives [] and the result is not the source list | PASSED | project/tests/test_queries.py |
| QRY-03, test_orders_by_date_time_then_appointment_id | queries.py select_appointments | equal time appointments come out ordered by appointment ID | PASSED | project/tests/test_queries.py |
| QRY-03, test_order_and_fields_are_unchanged | queries.py select_appointments | order and fields of the source snapshot are equal before and after two queries | PASSED | project/tests/test_queries.py |
| FP-01, test_repeated_calls_give_same_result_in_new_list | queries.py select_appointments | two calls give equal results in two different lists | PASSED | project/tests/test_queries.py |
| FP-02, test_distinct_list_for_each_input | queries.py select_appointments | empty, sorted and unsorted inputs each give a new list and the source snapshot is unchanged | PASSED | project/tests/test_queries.py |
| FP-03, test_named_key_returns_date_time_then_id | queries.py appointment_sort_key | the key returns date_time then appointment_id | PASSED | project/tests/test_queries.py |
| FP-03, test_sorting_using_named_key | queries.py select_appointments | the result order matches sorted with appointment_sort_key | PASSED | project/tests/test_queries.py |
| QRY-04, test_empty_list_for_no_appointments | services.py list_practitioner_appointments | known practitioner with no appointments or no matching status gives an empty list | PASSED | project/tests/test_services/appointment_service_test.py |
| QRY-04, test_list_practitioner_appointments_invalid_requests | services.py list_practitioner_appointments | unknown ID raises LookupError, blank ID and status 'scheduled' raise ValueError, records unchanged | PASSED | project/tests/test_services/appointment_service_test.py |
| FR-09, test_list_practitioner_appointments_uses_registered_id_and_order | services.py list_practitioner_appointments | an ID with spaces still lists the registered practitioner's appointments in order | PASSED | project/tests/test_services/appointment_service_test.py |
| FR-07, test_list_practitioner_appointments_shows_cancelled | services.py list_practitioner_appointments | after cancellation the all status list and CANCELLED list keep the appointment and SCHEDULED does not | PASSED | project/tests/test_services/appointment_service_test.py |

Full suite on final branch stage9/Feature/Console_based_menu. 
Run python -m pytest -q in project/: 37 passed.

Include practitioner isolation, every enum status/default all, equal-time ID tie-break, named-key reuse, repeated calls, empty/already-sorted fresh lists, unchanged source order/fields, known-empty/unknown/invalid service cases and retained history.

Purity explanation from code inspection, including absence of hidden state and I/O: 
Both functions only use their arguments in queries.py. There is no global variable, no store or service import, no print and no input. select_appointments builds a new list and returns sorted of that list, so the source list is never sorted or changed in place (as asked by the tutor in handout). It only reads the practitioner ID and status of each appointment and never calls cancel or sets a field, so the same inputs give the same output each time.
What the tests do and do not establish: The tests show that for the cases we tried the source order and fields stay the same, the result is a new list, repeated calls match and the order is correct. They do not prove there is no hidden state or input/output for every possible input, that needs the code inspection above. Since there can be infinite amount of sample data, we typically test boundary cases. Hence test cases passing does not say that everything is correct non breaking and complete.

## D. Integrated console and workflow evidence

| Scenario / acceptance ID | Reproducible inputs / artefact | Expected result | Observed result and state check | Evidence link |
|---|---|---|---|---|
| UI-01 full menu workflow | test_UI_01_menu_workflow, scripted input to the real menu, same steps as the handout | Conflict rejected, D2 booking at same time works, A1 cancelled but still found, scheduled list empty, freed slot booked with new ID | Passed, all of these were seen in the output in the manual run and tested run | project/tests/test_workflows.py |
| UI-02 invalid-input recovery | test_UI_02_menu_recovers_from_invalid_input, same way, with wrong menu choice, blank and unknown IDs, duplicate patient, bad dates, repeated cancel and bad status | Each wrong input shows a message and goes back to menu, failed booking does not take the ID | Passed, A1 could still be booked after the failed tries, as verified through manual run and test case.| project/tests/test_workflows.py |
| Automated service workflow | test_integrated_service_workflow, services and one store, no menu | Wrong bookings change nothing, different practitioner allowed, cancelled A1 kept, filters work, freed slot booked | Passed, stored list same before and after the wrong bookings | project/tests/test_workflows.py |

Same patient with another practitioner is allowed because the conflict rule only checks the same practitioner at the same time. There is no rule about one patient having two practitioners at once in the system desc/handouts.

Include registration/find, booking, conflict rejection, different-practitioner booking, cancellation, retrieval, listing/filtering, freed slot and exit; duplicate/unknown/blank IDs, malformed/impossible date, invalid status, unknown choice and repeated cancellation. Identify before/after state and subsequent successful action.

## E. GitHub Copilot review and human decisions

Human design completed before AI: sections A and B of this file, written before the Copilot review was run. (That means complete code design was initially suggested by human)
Actual prompt/context supplied:The Section 8 reviewer prompt from the Stage 9 handout, used unchanged. Context given was the synthetic code and tests only, queries.py, AppointmentService.list_practitioner_appointments, run_menu with parse_status in console.py, tests/test_queries.py and tests/test_workflows.py, and the current contracts.

Actual response: The code keeps the query pure, the source list is not changed, the service uses the registered ID, and the menu uses one store and does not copy domain rules. No Critical findings. Important, the duplicate registration case in the menu test is only sent as input and its error message is not checked. Optional, the menu stops with an EOFError traceback if input closes before choosing 0. Optional, status text in capitals like SCHEDULED is rejected. Optional, a wrong status for an unknown practitioner reports the status error first when using the menu. Optional, the menu looks up the practitioner a second time to print the name.

| AI finding | Code/test evidence | Severity | Accept/Modify/Reject and reason | Change or no change | Actual verification |
|---|---|---|---|---|---|
| Duplicate registration in the menu test is not asserted | tests/test_workflows.py test_UI_02_menu_recovers_from_invalid_input | Important | Accept, the case is in the handout list and the test should check it | Added one assert for the duplicate patient error | Ran the menu with P1 registered twice, got the duplicate error and find still showed Alex Example. Full suite 37 passed |
| EOFError traceback when input ends without 0 | console.py run_menu, python main.py --interactive with input that ends early | Not imp | Reject, not an expected input error in the handout and catching it would hide a real stop of the program | No change | Normal exit with 0 still works |
| Capital status such as SCHEDULED is rejected | console.py parse_status | Alr happens (not imp) | Reject, the prompt and the handout use lowercase and no requirement asks for other cases | No change | - |
| Wrong status with unknown practitioner shows the status error first in the menu | console.py parse_status is called before the service | Not Important | Reject, the handout says not to make an error priority rule for several errors | No change | Ran status booked with unknown D9, got the status error and the menu continued |
| Second practitioner lookup to print the name in the listing | console.py option 8 | Not Important | Reject, it is needed to print the name when the list is empty and the lookup does not change any record | No change | Read the code, the empty list case prints the practitioner name with No appointments found |

Responsibility check: explain how domain invariants, shared-store collections, service coordination, pure queries and console effects remain separate: The domain objects in domain.py keep their own rules, such as trimmed non-blank IDs and the cancel rule. The store keeps the in memory collections and the lookup. The services coordinate registration, booking, cancellation and the validated listing. queries.py only selects and sorts the list it is given. console.py prompts, parses the date and status text, calls the services and prints messages, and it holds no domain or conflict rules. Everythingg is in its own layer, in its own files so nothing interfere with other files, takes additional responsibility there is proper modularity and separation of concern presentation layer does not know bout business logic applied in services and vice versa, etc.

## F. Required reflections

1. Which integration concern was architectural rather than a filtering/sorting detail? I think deciding where each check belongs since the pure query does not check if a practitioner is registered, the service does that through the store and also checks the status, and the console only turns text into the enum. The menu also uses one store and one set of services for the whole session, so every command sees the same records. Also, the decision where is the pure queries called from, anywhere else other than services would have disturbed our main architecture and our modularity.
2. Which Copilot suggestion did you reject as over-engineering, and why? Apart from the one I accepted, I rejected all others and almost all of em were over-engineered suggestions, well to be fair Copilot didnt know bout handout requirements in detail thats why it over extended as next steps, but we rejected knowing in full detail the system reqs.
3. How did you prove cancelled appointments remain retrievable and listable in the same session? In test_list_practitioner_appointments_shows_cancelled, after cancelling A1 the all status list and the CANCELLED list still hold it and the SCHEDULED list does not. The workflow test checks find_appointment('A1') returns the same object with status CANCELLED, and the UI-01 run shows the A1 reference line with cancelled after the cancel.

## G. Ten formative answers

1. What makes select_appointments pure, and what side effect breaks purity? It only uses its arguments and returns a new list, with no input, output or hidden state. Sorting the source list in place, printing, or changing an appointment object would break its purity. Also they are deterministic for all same input service gives to it, it will always give same output to service for it  and modify nothing outside of its local scope.
2. Which explicit inputs are needed, and why avoid a global store? 
It needs the list of appointments, the practitioner ID and the optional status. A global store would hide an input (by superceding), so the result could change without the arguments changing and it would be harder to test. Also global breaks purity, the func should work with only local scope.
3. How can a new list reuse Appointment objects safely? 
The new list holds the same objects, and that is fine as long as the query never changes them. We checked this by comparing a snapshot of order and fields before and after.
4. Why use a named key, and what breaks equal-time ties? 
A named key can be reused and tested on its own. The named key we use is date_time then appointment_id, so appointments at the same time are ordered by appointment ID (which can never be same due to uniqueness hence all ties are broken by this).
5. How do default and explicit status filters differ? No status (None) returns every status including CANCELLED and COMPLETED, an explicit enum value returns only appointments with that status.
6. How do empty, unknown practitioner and invalid filter cases differ? A known practitioner with nothing matching gives an empty list. A valid ID that is not registered raises LookupError. A blank or invalid ID or a status that is not an AppointmentStatus raises ValueError.
7. Which console errors recover, and how is unchanged state checked? Unknown menu choice, blank or unknown IDs, duplicate registration, bad date/time, unknown appointment, repeated cancellation and invalid status all print a message and return to the menu. State is checked by finding or listing the records afterwards and by booking the same ID successfully after a failed booking.
8. What is data integrity for registered participants, conflicts and history? Appointments hold the real registered patient and practitioner objects, the same practitioner cannot have two SCHEDULED appointments at the exact same time, and cancelled appointments stay in the store with status CANCELLED and are not deleted.
9. What is Copilot's review role, and who verifies findings? Copilot gives suggestions as a reviewer, it does not decide. The group checks each finding against the requirements, the code and the tests before accepting, modifying or rejecting it.
10. How do pure functions and OOP responsibilities work together? 
Domain objects keep their rules and the services coordinate the store. The pure query only selects and sorts what the service gives it, and the console only handles input and output, so interaction never controls the domain rules.

## H. Review, completion and common handover

Issues and bounded branches: branches stage9/Task/Pure_query_implementation, stage9/Task/practitioner_appointments_listing and stage9/Feature/Console_based_menu. 
Issue links: https://github.com/DominicRDA-uc/st1-assignment-3/issues/13 (pure query), https://github.com/DominicRDA-uc/st1-assignment-3/issues/14 (service listing), https://github.com/DominicRDA-uc/st1-assignment-3/issues/15 (menu and entry point)
PR/diff and another-member human reviewer: 
Review responses and Copilot comparison: [links]
Integrated common Stage 9 SHA: [complete]
Full regression command, working directory, actual count/result and evidence: python -m pytest -q in project/ on branch stage9/Feature/Console_based_menu gave 37 passed. 

README run instructions and scope/limitations: project/README.md has not been updated for Stage 9 yet.
Unresolved issues and support/action: The project README update, the human review, the GitHub Copilot review, the PR merges and the final SHA are still to be done.
UG common candidate / PG future branch plan: Dominic, Juliann and Aditti (UG) go to Stage 12 using the protected common Stage 9 candidate. Junaid (PG) starts Stage 10 later on a separate branch after the common candidate is approved.

- [X] Query contracts, purity, new lists and named-key ordering verified.
- [X] Service empty/unknown/invalid cases and cancellation history verified.
- [X] Every console command and invalid-input recovery demonstrated.
- [X] Query and workflow tests plus all previous tests pass; actual evidence linked.
- [X] Human design, Copilot critique, review and integration recorded honestly.
- [X] Reflections and ten formative responses completed.
- [ ] README updated; earlier code/tests/records preserved.
- [ ] Common SHA protected for UG Stage 12; PG Stage 10/11 work deferred until approved.

No persistence, rescheduling or assurance implementation is part of Stage 9. UG: 6→7→8→9→12. PG: 6→7→8→9→10→11→12. Mixed groups keep one repository and protect the common candidate.
