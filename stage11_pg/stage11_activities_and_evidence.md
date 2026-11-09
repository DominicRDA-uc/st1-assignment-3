# Stage 11 PG assurance activities and evidence

PG-only stage. Undergraduate students are not required to complete this record. UG-only groups retain this supplied template unchanged as intentionally not applicable; do not fabricate N/A responses. Optional UG participation is unassessed.

Blank student template. All Assignment 3 stage materials are provided from the beginning. Complete this stage only after the previous applicable stage has been integrated, verified and recorded. Use this supplied file in stage11_pg/ in your EXISTING repository. Preserve project/, earlier records/tests and the protected common Stage 9 SHA. Do not copy staff references or fabricate AI evidence.

Group/tutorial: Wednesday 2.30 to 4.30, Group 2
Assessed PG members and contributions: Junaid Sayani (junaidSayani1)
Optional UG contributors: Adithi (adi-ii07) merged PR #23.

## A Handover and human-first scope

Integrated Stage 10 code SHA / protected Stage 9 common SHA: Stage 10 merge 1989ed1 (PR #21). Protected Stage 9 SHA 280884d (PR #19). This branch HEAD is 04afa5d, which is later Stage 10 evidence commits on main.
Recoverable branch / baseline / actual commands, working directory and results: branch stage11/Task/Reassurance from current main. git status --short empty. python -m pytest -q in project/ gave 57 passed. 
Domain, store, services, queries, console, entry point, tests and rescheduling inspected: yes, those files plus tests/test_rescheduling.py and requirements-dev.txt (pytest==8.3.5 only)
Selected PG feature and common workflow / requirements / code locations: PG reschedule in domain.py Appointment.reschedule and services.py AppointmentService.reschedule_appointment. Common workflow patient find in PatientService.find_patient and store find_patient
Actual available earlier AI, issue, PR and dependency evidence: Stage 10 issue #20, PR #21, stage10_pg record (Copilot drafted reschedule plan, and code  - given detailed prompts and responses in stage 10 evidence file). Runtime imports are stdlib. Test tool pytest 8.3.5.
Missing evidence / honest limitation: None.
Assets and trust boundaries: synthetic patient and practitioner records, appointment id status and time, tests, git history, pytest. Console text goes into services. Services call domain and store. Queries take a list and return a new list. Copilot would see repo text we paste.
Scope, assumptions, exclusions and initial observations made BEFORE Copilot: Session-only appointment scheduling system. No SQL in the project. Console prints synthetic names as menu output. No requests or API key or secrets in smartcare/. Data is lost on exit
Confirmed Copilot mode / student entitlement / permissions / approval reference: Plan Mode - no permissions given pre-approved, every permission is checked on runtime.
Plan-only → human approval → bounded editing check / approved equivalent route: Given in stage 10  Evidence File.
Overview/revision 2 availability / source: used in earlier stages from the assignment package
Assigned PG owner / independent reviewer: owner Junaid.  Reviewed and merged by Adithi (adi-ii07) on PR #23.

## B Original tutorial activities


### B1 Risk classification

| Scenario | Risk | Why | Control |
|---|---|---|---|
| AI explains a public Python error | Low | Public error text, no secrets | Keep it as learning help, check the explanation against the docs |
| Student pastes an API key into AI | Extremely High | The key can leak!! It gets registered back to AI training loop for feedback. | Do not paste keys. This project has no API key in smartcare/. Should excludde all the credentials/env files from AI access |
| Agent proposes unknown package | Medium | Extra packages are out of scope always | Reject unless listed in requirements-dev.txt and reviewed |
| AI-generated code logs patient names | Medium | Extra logging is not a requirement + in case of non-synthetic data patient data is critical should not be logged in plain text. | Do not add logging. Console already prints synthetic names for find and list |
| Agent modifies deployment configuration | High | This repo has no deploy config to change. Nor the AI has permissions for it. | Do not let the agent edit files outside the approved scope, and never anything with deployment config/CI/CD. |

### B2 Green Amber Red
Choose GREEN / AMBER / RED and justify each.

| Use | Classification | Reason and policy/control |
|---|---|---|
| Ask AI to explain pytest fixture | GREEN | Learning only, still run your own tests |
| Generate 100 lines of assessed domain code | AMBER | Large assessed code needs disclosure, review and tests |
| Paste real patient record for debugging | RED | Real records are not allowed, it is private and critical data. Use synthetic names only |
| Use AI to draft test ideas then verify | GREEN | Ideas only (plan mode) if you write or check the assertions and the ideas and implementations yourself |
| Agent autonomously deletes repository files | RED | No recovery if it deletes without approval, shouldnt be allowed to delete. |

### B3 VERIFY patient search
Record one concrete question/evidence item for each letter against the current PatientService/shared-store contract.

| VERIFY element | Question or evidence |
|---|---|
| Validate | Known ID must return the stored Patient. Unknown valid ID raises LookupError. Blank ID raises ValueError |
| Examine | PatientService.find_patient calls data_store.find_patient and raises LookupError when the store returns None |
| Run meaningful tests | test_find_patient_with_valid_id, test_unknown_patient_id, test_invalid_patient_id in tests/test_services/patient_service_test.py |
| Inspect risks | A new store starts empty, use synthetic data only |
| Fit architecture/policy | Service coordinates and applies logic/business rules, store holds the dictionary/the data and returns the data to service. Domain Patient holds the fields/identity/invariants and single focused class based data. |
| You remain responsible | Yes! (junaid) |

### B4 TRUST decision
The feature passes tests but adds an unreviewed package and logs full patient records. Should it be accepted?

| TRUST element | Reason/evidence/action |
|---|---|
| Trace | Tests passing do not show where the package came from. So we need to trace back/ review what package and why was it added. |
| Review | A human must read the new dependency and the log lines, including all other code |
| Understand | Logging full records is not the same as the required find display, and typically logging real world data is not recommended, actuallly when logging we should only log at error places and only where needed with minimal data |
| Secure | Unreviewed package and extra patient logs are out of this project's policy |
| Test | Green tests do not cover privacy or licence, or completeness |

Decision and reason: Reject, until the package is removed or approved and the logs are removed.
Exit: Why is a technically correct AI-generated feature still potentially unacceptable? It can still add an unreviewed package or leak data, which this system does not allow. There are alot of ways to achieve one single thing AI can make things work with an unsecure way but thats not correct and should be rejected.

### B5 Sanitised critique only
Identify the hard-coded demo-key placeholder, unnecessary requests import, patient-ID/name logging, fabricated lookup and missing test/provenance evidence. Do not copy or run the old audit target.


| Concern | Observed example evidence | Severity | Correction and recheck |
|---|---|---|---|
| Hard-coded demo-key placeholder | A code piece assigns API_KEY a demo-key (no example in our system tho) | High | Do not add a key, not even demo keys in system code it should be in environment and excluded from git env and AI env. Recheck smartcare/ has none |
| Unnecessary requests import | The snippet imports requests (no example in our system tho) | High | Do not install requests. Recheck requirements-dev.txt is pytest only |
| Patient ID/name logging | The snippet imports logging and logs patient ID and name (no example in our system tho) | Medium | Do not add logging. Recheck no logging import in smartcare/ |
| Fabricated lookup | The snippet search_patient builds a dict from any non-empty ID and name, empty ID returns None | High | Lookup must use the store. Recheck PatientService.find_patient or whatever equivalent for teaching snippet |
| Missing tests and provenance | The snippet shows no tests (our system has PatientService tests) | Medium-High | Keep the PatientService tests in the repo, for teaching app it should include unit and integration tests it improves reliability trust worthyness and also allows to identify code breaking changes at modification. |

## C Actual risk register


| Risk | Artefact | Likelihood | Impact | Control | Status |
|---|---|---|---|---|---|
| Session data lost on exit | in-memory store | Certain | Expected, not a defect | README says session-only | Accepted |
| Agent adds a package or extra files | Copilot edits/implementation | Uncertain until a proper review/audit. | Out of scope code, should not be present | Diff review, allowed files only | Reject |
| Weak or missing tests around reschedule plus listing | tests/test_rescheduling.py and listing tests | Uncertain | Wrong history or order could pass | Add tests/test_assurance.py | Open/Accepted |
| Extra diagnostic output | console.py prints | Low | Synthetic names are the required menu display | Do not add logging | Accepted (we only use synthetic data and dont add any logging) |

## D Actual findings tests and corrective actions

For each of at least TWO new/materially strengthened tests, explain the earlier coverage gap and the incorrect behaviour its assertions detect. No duplicated unchanged tests. test_lookup_does_not_use_another_store checks a second empty store does not invent P1/or falsify the data this will keep future modularity intact. Patient tests used one store only. test_reschedule_keeps_cancelled_history_in_a_new_list checks cancel then rebook then reschedule still keeps A1 cancelled, listing is a new list, A2 has the new time. Reschedule tests did not combine those three (integration test).

| Claim / risk / requirement | Location / version | Independent check / test | Observed result / finding or no finding | Action / owner | Recheck / limitation |
|---|---|---|---|---|---|
| Lookup uses the needed store only | PatientService.find_patient | test_lookup_does_not_use_another_store | no finding, second store stays empty, error is Patient not found | no code change/ Junaid | passed |
| Cancelled history still listed after a later reschedule | AppointmentService | test_reschedule_keeps_cancelled_history_in_a_new_list | no finding, A1 cancelled, A2 moved, listed is not stored | no code change, Junaid | passed |

| Assurance test | Earlier gap | Input/setup | Meaningful assertion | Incorrect result detected | Evidence/result |
|---|---|---|---|---|---|
| Test 1 test_lookup_does_not_use_another_store | One-store patient tests (did not cater information/logic leak into other store that could includ tight coupling) | P1 in store one, find P1 on store two | LookupError, list empty, P1 not in the message | A global or fake patient record (Not detected) | PASSED |
| Test 2 test_reschedule_keeps_cancelled_history_in_a_new_list | Reschedule tests did not keep a cancelled A1 then move A2 (integration workflow reassurance test) | cancel A1, book A2 same slot, reschedule A2 | find A1 is cancelled, listed == [A1, A2], listed is not stored | Lost history or listing mutating the store list | PASSED |
| Additional if useful | none | | | | |

| Suite | Command / project working directory | Tested code SHA | Actual result | Evidence |
|---|---|---|---|---|
| Assurance focused | python -m pytest -q tests/test_assurance.py in project/ | uncommitted on 04afa5d | 2 passed | terminal |
| Previous PG independently | python -m pytest -q --ignore=tests/test_assurance.py in project/ | uncommitted on 04afa5d | 57 passed | terminal |
| Common independently | python -m pytest -q --ignore=tests/test_assurance.py --ignore=tests/test_rescheduling.py in project/ | uncommitted on 04afa5d | 37 passed | terminal |
| Full PG cumulative | python -m pytest -q in project/ | uncommitted on 04afa5d | 59 passed | terminal |
| Integrated retest | python -m pytest -q in project/ | 030a647f5ece42b317f45b9d4149a7d3a3ab40da (main after PR #23) | 59 passed (Python 3.13.12, pytest 8.3.5) | Junaid retest on main after merge |

Confirmed defect / minimal correction / before-after evidence, or justified no-change decision: no in-scope defect found, production code unchanged, the two tests kept
Preserved earlier assertions / inspected test diff: only new file tests/test_assurance.py, no edits to older tests
Unresolved failures, action and owner: none.

## E VERIFY assessment


| VERIFY element | Evidence | Finding/action |
|---|---|---|
| Validate against requirements | FR-02 find patient, RES-05-R2 listing after a move, FR-07 cancelled history | Tests in D passed. No extra feature added |
| Examine implementation | find_patient uses the store. reschedule then list_practitioner_appointments uses select_appointments | Matches the contracts already in code |
| Run meaningful tests | test suites 2, 57, 37, 59 passed | Keep the two new tests |
| Inspect risks and assumptions | Session-only store, synthetic names, no SQL | Same as record C |
| Fit architecture and policy | Domain, store, service, query, console stay separate | No new package |
| You remain responsible | Junaid | I am responsible for my audits and AI audits, including verifiability and reliability tests |

## F TRUST assessment


| TRUST element | Evidence | Status/action |
|---|---|---|
| Trace | issue #20, PR #21, SHA 1989ed1, this branch | Stage 10 path is in git |
| Review | Adithi (adi-ii07) merged PR #23 into main at 030a647 | Independent of the PG author. Recorded in I |
| Understand | Two stores do not share patients. Listing after reschedule is a new list | See test_assurance.py |
| Secure | stdlib runtime, pytest for tests, no logging module, no secrets in smartcare/ | H |
| Test | 59 passed, common 37 still pass | Green suite is not a security claim |

## G GitHub Copilot audit

Sanitised material / actual prompt, context, version and response links: Handout G prompt filled with record A facts, SHAs, issue #20, PR #21, and the two assurance tests. Copilot replied in the IDE. Review only, no file edits.

Prompt:

Act as a software assurance reviewer using GitHub Copilot.
Review this sanitised SmartCare artefact for security, privacy,
dependency/provenance, architecture, test-quality and
unsupported-requirement risks. Do not assume missing context.
Separate observed evidence from questions requiring verification.
Rank findings by severity and suggest how a human reviewer
can verify each finding.
Context: one in-memory SmartCareDataStore; domain, services,
pure queries and console; Stage 10 rescheduling; actual tests.
No SQL, restart persistence or external calendar API is required.
My scope and initial observations:
Session-only appointment scheduling. One SmartCareDataStore in memory. No SQL, no files, no restart storage. Runtime is Python stdlib. Test tool is pytest==8.3.5 in requirements-dev.txt. No requests, no logging module, no API_KEY in smartcare/. Console prints synthetic ID and name for find and list. Data is lost on exit. PatientService.find_patient uses the store and raises LookupError when absent, ValueError for a blank ID. Appointment.reschedule and AppointmentService.reschedule_appointment move a SCHEDULED appointment. Queries return a new list. Trust boundaries: console text to services, services to domain and store, lists into queries, repo text sent to Copilot.
Relevant requirements, code, tests and version:
Protected Stage 9 SHA 280884d. Stage 10 merge 1989ed1 PR #21. Branch stage11/Task/Reassurance. Files: project/smartcare/domain.py, data_store.py, services.py, queries.py, console.py, main.py, requirements-dev.txt, tests including test_rescheduling.py and test_assurance.py. Synthetic names only (P1 Alex Example, D1 Taylor Example). Two new assurance tests: lookup on a second empty store does not invent P1, cancelled A1 stays listed after A2 is rescheduled and the listed container is not the store list. python -m pytest -q in project/ gave 59 passed. Common suite without rescheduling and assurance tests gave 37 passed. No production code change in Stage 11 so far.
Actual significant AI contributions and available evidence:
Stage 10 issue https://github.com/DominicRDA-uc/st1-assignment-3/issues/20
Stage 10 PR https://github.com/DominicRDA-uc/st1-assignment-3/pull/21
stage10_pg/stage10_activities_and_evidence.md records Copilot plan then bounded edits for reschedule. Stage 6 to 9 code PRs are in the same repo. Full Copilot chat transcripts are not all in git.
Review only. Do not edit files, install packages or run tools
without separate human approval of the bounded action.
(Along with this gave permissions to read-only/review test files and stage 10 rescheduling code + architecture for our system)


Response:


## Scope and conclusion

This is a **provisional review of the facts in your prompt only**. I did not inspect repository files or run tools, as requested. I found **no confirmed exploitable vulnerability** in the supplied evidence; the items below are verification points, not claims that defects exist.

| Rank | Area / severity | Observed evidence | Question and human verification |
|---|---|---|---|
| 1 | Test quality — **LOW** | The assurance tests reportedly verify that a lookup on a second empty store does not invent `P1`, and that rescheduling `A2` does not remove cancelled `A1` from results. The list-container check establishes that the returned list is not the store’s list. | Check `test_assurance.py`, `test_rescheduling.py`, and the related service/query code. Confirm coverage for invalid appointment states, rescheduling edge cases, and whether returned mutable appointment objects can change stored state. A new list alone does not establish deep isolation. |
| 2 | Privacy — **LOW** | Console find/list output reportedly includes IDs and names; the examples are synthetic (`P1 Alex Example`, `D1 Taylor Example`). | Inspect `console.py` and the data fixtures. Verify real patient data cannot enter this artefact or its demonstrations, and that console output is appropriate for its intended audience. |
| 3 | AI provenance — **LOW** | The Stage 10 issue, PR, and activity/evidence record document Copilot planning and bounded edits; full chat transcripts are not all in git. | Compare the [Stage 10 issue](https://github.com/DominicRDA-uc/st1-assignment-3/issues/20), [PR #21](https://github.com/DominicRDA-uc/st1-assignment-3/pull/21), merge `1989ed1`, and `stage10_pg/stage10_activities_and_evidence.md`. Confirm the relevant diff and test evidence are reviewable without relying on unavailable transcripts. AI contribution alone is not a security defect. |
| 4 | Dependency/provenance — **LOW** | Runtime is reported as Python stdlib; the development requirement pins `pytest==8.3.5`. No external runtime dependency is identified in the supplied facts. | Check `requirements-dev.txt` and the repository’s dependency workflow. Confirm how packages are sourced and whether the project’s reproducibility expectations require a lockfile or hash verification; an exact version pin alone does not establish package integrity. |

## Constraints and unsupported requirements

The stated in-memory, session-only design means **no SQL, restart persistence, files, or external calendar API are expected**. Their absence is not a finding. The described store/service/domain/query/console structure and `LookupError`/blank-ID handling raise no specific architecture or input-handling concern on the evidence provided. The reported `59 passed` is useful too.

Evidence that human scope and initial observations preceded Copilot: records A B C and the two tests were in the file before this audit
Actual supported route or approved equivalent / access limitations: Copilot Plan Mode, permissions checked at runtime. It did not open the repo or run tests (granted permission to look at tests though and told what was passing before hand)
Significant earlier AI contributions reviewed / available evidence / missing provenance: Stage 10 issue #20, PR #21, stage10_pg record. Full chats are not all in git

| AI claim | Affected requirement/code/evidence | Observed vs speculative / human verification | Severity / Accept Modify Reject / reason | Outcome / correction or no change | Recheck / limit |
|---|---|---|---|---|---|
| No confirmed exploitable vulnerability | whole system as described | Observed as a conclusion, not a code scan | Accept | no production change | Copilot did not read files |
| New list does not prove deep isolation, check mutable objects | test_assurance.py, queries.py | Observed: listed is not stored, objects inside are the same stored appointments by design | Reject. Stage 9 allows shared objects if the query does not change them | no change | already asserted listed is not stored |
| Console prints IDs and names | console.py find and list | Observed, synthetic names, required menu display | Reject | no change | no logging module |
| Version pin is not package integrity | requirements-dev.txt pytest==8.3.5 | Observed pin, no lockfile or hash | Reject adding a lockfile, out of scope | keep pytest 8.3.5 only | handout names the pin |

No false/rejected suggestion, if applicable: Copilot did not invent SQL or a missing calendar API. Two LOW items (deep isolation and lockfile) were overstated as risks for this session-only system. Rejected as defects..

## H Dependency provenance and privacy review


| Dependency/artefact | Source | Purpose | Licence/provenance | Verified? | Decision | Evidence link |
|---|---|---|---|---|---|---|
| Python 3.13.12 stdlib | python --version | runtime | https://docs.python.org/3.13/license.html | version checked, not a full licence audit | keep | domain, store, services, queries, console, main |
| pytest==8.3.5 | requirements-dev.txt | tests | https://pypi.org/project/pytest/8.3.5/ MIT on that page | file lists 8.3.5, page not re-downloaded here | keep as test tool only | requirements-dev.txt |

Actual runtime imports / test-tool dependencies / versions checked: smartcare uses datetime enum argparse. Tests also use pytest subprocess pathlib, pytest 8.3.5
Secret/data/output/input/permission/minimisation checks and evidence: no API_KEY in smartcare/. Console prints synthetic names for find and list
Requirements/model/code/tests/Stage 10 provenance links: issue #20, PR #21, stage10_pg D to H, tests/test_rescheduling.py
Bias/hidden assumptions / name formats / unnecessary fields / accessibility / scheduling policy: names are required text/ no gender or contact field/ no extra availability rule added, no assumption on scheduling policy follows FIFO order.
Policy questions or unresolved provenance / responsible contact: NA

## I Independent review and final audit statement

Human reviewer / PR or diff link / feedback: Adithi (adi-ii07) merged https://github.com/DominicRDA-uc/st1-assignment-3/pull/23 on 9 Nov 2026. Merge commit 030a647. No production-code change was requested. Junaid remains the PG owner of the tests and the audit record.
Corrections and recheck / approval before integration: No code correction. Two assurance tests kept. python -m pytest -q in project/ on 030a647: 59 passed.
Overall decision: Acceptable
Unresolved risks: NA
Evidence supporting decision: PR #23 on main. 59 passed after merge. Copilot audit in G found no confirmed defect. Production code unchanged in Stage 11.
Remediation owner / action / status: Junaid. No further Stage 11 code action.
Residual limitations and conditions of acceptance: Session-only store. Synthetic names. No lockfile. Full Copilot chats are not all in git.
Accountable reviewer and PG member sign-off: Junaid (PG owner). Adithi (adi-ii07) merged PR #23.
Integrated PG SHA / protected common SHA: Stage 11 SHA 030a647f5ece42b317f45b9d4149a7d3a3ab40da (PR #23). Protected Stage 9 SHA 280884d (PR #19). Stage 10 SHA 1989ed1 (PR #21).

## J Reflections

1. Which risk would have been easy to miss if you only checked whether tests passed? A second store inventing P1, or list mutating the store list after a reschedule. Those still pass a count if you never assert identity or a second store
2. Which AI audit finding was false or overstated? If none, state honestly and explain verification. Copilot found no exploit. The lockfile and deep isolation notes were overstated for this app. Checked requirements-dev.txt, queries.py and the two assurance tests 
3. What evidence supports your final trust decision? Imports clean, requirements-dev.txt approved packages only, the two new tests, 37 common passed, 59 total pass, complet and correct requirements adhered to, no extra leakage or broken architecture.

## K Ten formative questions


1. What does least privilege mean? Give only the access needed for the task, not shell, merge or extra package permission.
2. What is provenance in AI-assisted software engineering? Being able to say where a change, package or AI output came from
3. What is data minimisation? Keep, use and show only the data the requirement needs.
4. What is dependency hallucination? An AI names a package that is not real or not authorised or too old.
5. What is software supply-chain risk? Harm from a third-party package or its source, for eg we use pytest and lets say pytest uses some inherent C++ libraries if that c++ lib is vulnerable that vulnerability creeps into our project too.
6. What does the VERIFY framework ask students to do? Check it works and fits, using validate, examine, tests, risks, architecture and named owner
7. What does the TRUST framework ask students to do? Check it should be accepted, using trace, review, understand, secure and test
8. What does an AMBER AI-use classification mean in this course? Large assessed help that is allowed only with disclosure and proper human review/checks of the diff.
9. Who remains responsible for professionally accepted AI-assisted software? The user/engineer who accepts it, here me/Junaid.
10. What is the Stage 11 engineering rule? Identify, verify, trust, remediate, recheck. A supported no finding is valid. Humans stay accountable

## L Completion and Stage 12 handover


- [X] Actual SmartCare scope and human-first observations recorded.
- [X] All tutorial activities and every VERIFY/TRUST element complete.
- [X] At least two meaningful assurance tests with added-value explanations.
- [X] Real findings/no-findings and corrective actions or no-change evidence recorded.
- [X] Earlier assertions preserved; common and PG suites independently checked.
- [X] Copilot claims independently verified and actual decisions recorded honestly.
- [X] Dependency/provenance/privacy review and residual limits complete.
- [X] Independent human review, integration and retest recorded.
- [X] All three reflections and ten formative questions answered.
- [X] Accountable PG contribution/sign-off and protected UG pathway retained.

Unresolved issues / owner / handover action: None for Stage 11. Stage 12 is a separate PR and is not on main yet. Owner Junaid for PG handover.
Tested code SHA / command / working directory / observed result: 030a647f5ece42b317f45b9d4149a7d3a3ab40da. python -m pytest -q in project/. 59 passed (Python 3.13.12, pytest 8.3.5).
Final submitted SHA / later evidence-only change explanation: 030a647f5ece42b317f45b9d4149a7d3a3ab40da. This evidence update is after that merge and does not change production code.
Stage 12 handover links to same project/tests/assurance conclusion and limitations: same repo and tests. tests/test_assurance.py kept. No production change. Copilot audit in G, no confirmed defect. PR #23 merged. Protected Stage 9 SHA 280884d. Stage 10 SHA 1989ed1. Stage 11 SHA 030a647.
Begin Stage 12 after the previous applicable stage is integrated, verified and recorded. Its handout and blank record are already supplied.
