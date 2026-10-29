# Stage 6 activities and evidence

Complete this one group record. Link actual issues, diffs, tests and reviews; avoid copying entire histories. Blank fields are intentional. Duplicate rows as needed. Use synthetic data only. Every member records their own meaningful contribution. Do not invent results, reviews or Copilot use.

- Group/tutorial: Wednesday 2.30-4.30
- Members, GitHub usernames and cohorts: Junaid Sayani (junaidSayani1), Dominic (DominicRDA-uc), Juliann (Jules-tryingtocode), Aditti
- Repository URL: https://github.com/DominicRDA-uc/st1-assignment-3
- Starting SHA: e5bdbf1d4eb482bee09fe683c42a528603667515

## A Requirement to issue activities

### FR-02 Patient Search

- Title: Patient Search (By ID) - Code Implementation (FR-02)
- Context: The PatientService.find_patient method currently raises a NotImplementedError, we need to implement the function so that it allows us retrieving patient profiles by ID, verifies correctness of ID type and if none is found return a lookupError.
- Requirement: Implement PatientService.find_patient to find by ID return patient record.
- Acceptance criteria: Replaces the explicit NotImplementedError with functional retrieval logic.
Returns the matching patient instance when valid ID found.
Handles non-existent records gracefully by raising LookUpError
Passes all new unit tests dedicated to patient lookup while ensuring existing 8 test cases continue to pass.
Invalid formatting of ID passed raises a ValueError
- Scope: PatientService.find_patient method and corresponding unit tests.
- Definition of Done: Code implemented, unit tests for find_patient written and passing, no failing of existing tests, and code reviewed + merged into main, working as intended.
- Owner: Junaid Sayani
- Actual issue link: https://github.com/DominicRDA-uc/st1-assignment-3/issues/2

### FR-06 Appointment Cancellation with FR-07 retained history

- Title: Appointment Cancellation & History Retention (AppointmentService.cancel_appointment) - Code Implementation (FR-06, FR-07)
- Context: Canceling appointments is currently disabled via a NotImplementedError in AppointmentService.cancel_appointment. Per FR-06 and FR-07, canceling an appointment must update its status without removing the record from in_memory storage.
- Requirement: Implement AppointmentService.cancel_appointment to transition appointment status to canceled while preserving the historical record for clinic audit trails.
- Acceptance criteria: Replaces NotImplementedError with cancellation logic (FR-06).
Updates the appointment's state to CANCELED.
The cancellation and state transition only works if the appointment was in SCHEDULED state.
Retains the appointment record to preserve booking history (FR-07).
Prevents cancellation of already completed or already cancelled appointments.
Passes cancellation unit tests as well as the whole test suite.
- Scope: AppointmentService.cancel_appointment method, and related unit test files, practictioner service/lookup functions if needed, repo/datastore/domain functions as needed.
- Definition of Done: Cancellation logic implemented (appointment gets cancelled but still remains a part of storage with an updated status), all unit tests passing, and PR approved + merged.
- Owner: Junaid Sayani
- Actual issue link: https://github.com/DominicRDA-uc/st1-assignment-3/issues/4

## B Commit quality

| Original example | Strong or Weak | Reason |
|---|---|---|
| changes | weak | Small, weak commit message does not tell anything what changes were committed |
| final version | Weak | Even if this is just a simple version tag, it should be labelled properly with current version patch num etc. |
| Add patient search by ID | Strong | Tells what changes were done/pushed |
| fix stuff | Weak | Again does not tell what stuff/bugs were fixed |
| Prevent cancellation of completed appointments | Strong | Tells exactly concretely what changes were pushed |

## C Over scoped PR review

A cancellation PR also renames unrelated patient fields, restructures unrelated code and adds a new dependency.

- Scope concerns: This is scope creeping, it does not have scope for those areas and should not be modifying those fields and parts of code, its scope is relevant only to appointment related code.
- Responsibility and architecture concerns: Cancellation is the appointment's responsibility, renaming patient fields changes patient's domain, which this requirement does not own. A new dependency changes the whole application's architecture for a status update that the existing domain cancel method already supports.
- Testing and review concerns: A passing test run does not show that the scope stayed inside the cancellation requirement. The reviewer has to inspect the diff, not only the test summary. Also, the review would be tougher because of large scale changes instead of focused change.
- Changes to remove or separate, with reasons: Remove the patient field renames because they are outside appointment cancellation and break existing patient code. Remove the unrelated restructure for the same reason. Remove the new dependency too to preserve architecture. Keep the cancellation behaviour, the retained appointment record, and the unit tests.

## D Challenge a weak Copilot review

GitHub Copilot says: "Looks good; tests pass."

- Missing evidence: Which requirement was checked, which assertions the tests make, the diff includes only the files for that requirement or not. "Tests pass" does not show any of that and it is not a sole acceptance criteria.
- Follow-up review question 1: Which issue and acceptance criteria does this diff satisfy?
- Follow-up review question 2: Which tests check the changed behaviour?
- Follow-up review question 3: Does the diff change any file or behaviour outside that requirement scope?
- Follow-up review question 4: What are the failing cases, and do the tests assert the correct thing/object/state/result?
- Follow-up review question 5: Are all edge cases covered through the unit tests, is the commit/PR final and single concern focused ? 
- Additional questions if useful: None

## E Team workflow agreement

| Practice | Team agreement |
|---|---|
| Branch naming | We will name it in format: Stage-Number/(Feature/Bug/Task/Chore)/Issue/Ticket its related to|
| Commit message convention | (Feature/Bug/Task/Chore): Commit Changes that are being pushed|
| PR size | Single Issue / Single concern requirement focused small PR |
| Another-member review requirement | True - for all major PR's - no review/PR required for evidence.md files|
| Merge rule | Another Member Review approves the final version and merges it into main along with all test passing|
| Significant Copilot disclosure rule | If copilot is used in coding/testing it will be disclosed - otherwise reviewing with CoPilot always disclosed.|

## F Issue and backlog index

Create at least two focused issues. Add a linked practitioner-lookup issue or an explicit supporting criterion with the tutor if needed to cover all three service targets.

| Issue link | Requirement | Owner | Acceptance criteria or precise link | Status |
|---|---|---|---|---|
| https://github.com/DominicRDA-uc/st1-assignment-3/issues/2 | FR-02 Patient Search | Junaid Sayani | https://github.com/DominicRDA-uc/st1-assignment-3/issues/2 | open |
| https://github.com/DominicRDA-uc/st1-assignment-3/issues/3 | Practitioner search by ID | Junaid Sayani | https://github.com/DominicRDA-uc/st1-assignment-3/issues/3 | open |
| https://github.com/DominicRDA-uc/st1-assignment-3/issues/4 | FR-06 Appointment Cancellation with FR-07 retained history | Junaid Sayani | https://github.com/DominicRDA-uc/st1-assignment-3/issues/4 | open |

## G Pull request evidence

Repeat this block per PR. Record actual events, not planned approvals.

- PR link and title: https://github.com/DominicRDA-uc/st1-assignment-3/pull/5 — Enhancement/Feature: Implemented Code for Patient Search by ID
- Linked issue and requirement: https://github.com/DominicRDA-uc/st1-assignment-3/issues/2 — FR-02 Patient Search
- Feature branch: stage6/feature/issue-2_patient_search
- Changed behaviour: PatientService.find_patient returns the stored patient for a valid ID, raises LookupError when no patient is stored for that ID, and raises ValueError for a blank or invalid ID, does not add a patient. Tests are in project/tests/services_test/patient_service_test.py.

- Meaningful commits: https://github.com/DominicRDA-uc/st1-assignment-3/commit/6733d4678cb97c6043e66cceafc543e87a58f753
- Test command, directory and observed result: python -m pytest, directory project/ on commit 6733d4678cb97c6043e66cceafc543e87a58f753, 11 passed (Python 3.13.12, pytest 8.3.5).
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

- PR link and title: https://github.com/DominicRDA-uc/st1-assignment-3/pull/6 — Feature: Implemented Find practitioner by ID Lookup
- Linked issue and requirement: https://github.com/DominicRDA-uc/st1-assignment-3/issues/3 — Practitioner search by ID
- Feature branch: stage6/feature/issue-3_practitioner_search
- Changed behaviour: PractitionerService.find_practitioner returns the stored practitioner for a valid ID, raises LookupError when none is stored, and raises ValueError for a blank or invalid ID, does not add a practitioner. Tests are in project/tests/services_test/practitioner_service_test.py.
- Meaningful commits: https://github.com/DominicRDA-uc/st1-assignment-3/commit/6328f69b356e66b46f18ed19d1a255801e8d83ce
- Test command, directory and observed result: python -m pytest, directory project/ on commit 6328f69b356e66b46f18ed19d1a255801e8d83ce, 11 passed (Python 3.13.12, pytest 8.3.5).
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

- PR link and title: https://github.com/DominicRDA-uc/st1-assignment-3/pull/7 — Feature: Appointment Cancellation feature implemented
- Linked issue and requirement: https://github.com/DominicRDA-uc/st1-assignment-3/issues/4 — FR-06 Appointment Cancellation with FR-07 retained history
- Feature branch: stage6/feature/issue-4_appointment_cancellation
- Changed behaviour: AppointmentService.cancel_appointment loads the stored appointment, calls Appointment.cancel(), and returns that same object so the record stays in the store. Unknown IDs raise LookupError. An invalid transition raises ValueError and leaves the status unchanged. Tests are in project/tests/services_test/appointment_service_test.py.
- Meaningful commits: https://github.com/DominicRDA-uc/st1-assignment-3/commit/c35a418b406fb866e5ea9c2ea72b6cf7256d72a3
- Test command, directory and observed result: python -m pytest, directory project/ on commit c35a418b406fb866e5ea9c2ea72b6cf7256d72a3, 11 passed (Python 3.13.12, pytest 8.3.5).
- Another-member reviewer: [response]
- Human observations recorded before Copilot: [link and time]
- Requirement, responsibilities, test assertions and unrelated-scope checks: [response]
- Key feedback: [response]
- Author response/change and verification: [response]
- Reviewer recheck and approval: [link]
- Merge outcome and SHA: [response]
- Significant Copilot assistance: [summary or none]
- Linked issue closure: [response]
- Each member updated main: [member and confirmation]
- Integrated verification after merge: [command, directory, result and code SHA]

## H Copilot collaboration record

Record meaningful required use, not every trivial completion. Repeat per significant interaction.

- Member and task: [response]
- Prompt/purpose and relevant issue/diff: [response]
- Summary of output: [response]
- Human check against actual code, requirements and tests: [response]
- Decision — Accept / Modify / Reject: [select]
- Reason: [response]
- Verification/evidence: [link and result]

## I Human versus Copilot review comparison

- Human reviewer noticed before consulting Copilot: [response]
- Copilot noticed: [response]
- Overlap: [response]
- What did the human reviewer notice that Copilot did not: [response]
- What did Copilot identify that the human reviewer initially missed: [response]
- Unsupported or incorrect Copilot suggestion: [response or none identified with explanation]
- Human judgement accepted, modified or rejected, and why: [response]
- Which evidence justified merge approval: [response]

## J Contributions

Repeat per member. Include only categories that describe actual work; write not applicable where appropriate. Pairing or mentoring can be supported by a short corroborated note.

- Member: Junaid Sayani (junaidSayani1)
- Implementation: Patient search https://github.com/DominicRDA-uc/st1-assignment-3/commit/6733d4678cb97c6043e66cceafc543e87a58f753, practitioner search https://github.com/DominicRDA-uc/st1-assignment-3/commit/6328f69b356e66b46f18ed19d1a255801e8d83ce, appointment cancellation https://github.com/DominicRDA-uc/st1-assignment-3/commit/c35a418b406fb866e5ea9c2ea72b6cf7256d72a3
- Testing: Three unit tests in each of project/tests/services_test/patient_service_test.py, practitioner_service_test.py and appointment_service_test.py, on the commits above. python -m pytest from project/ reported 11 passed on each commit.
- Review: [work and evidence]
- Issue refinement: https://github.com/DominicRDA-uc/st1-assignment-3/issues/2, https://github.com/DominicRDA-uc/st1-assignment-3/issues/3, https://github.com/DominicRDA-uc/st1-assignment-3/issues/4
- Design and responsibility discussion: [work and evidence]
- Debugging or integration: [work and evidence]
- Documentation or team support: [work and evidence]

## K Exit question

Why is a high commit count not necessarily evidence of strong contribution?

A high count can be many small or unclear commits, or one change split up so it looks like more work. Infact, you can add a new line and make it as a commit hence count does not show that the changes meet acceptance criteria, that the work is concrete and complete, it does not show that there is some significant work that has been done by the person for any of the requirement. One commit that says what changed and is backed by tests and review can be a stronger contribution than many commits that do not.

## L Stage 6 formative questions

1. What is version control?

Version control records changes to the project over time. Each commit acts as a checkpoint for the code, such as a SHA, so the group can see who changed what, compare versions, and return to an earlier version if needed (rollbacks).

2. Why is a feature branch useful?

A feature branch keeps one change branched from main until it is reviewed. Main stays at the last integrated and stable version that works and runs correctly, and the pull request can show exactly focused feature's diff (easier to review then).

3. What makes a commit a good engineering commit?

Tells what changes were done/pushed. Tells exactly concretely what changes were pushed. A message such as "changes" or "fix stuff" does not tell anything about what changes were committed or what was fixed.

4. What is a pull request?

A pull request proposes merging a feature branch into main. It shows the diff and links the change to its issue (not necessary - can link to an external ticket) so another member can review it before it is merged into a stable main.

5. What is the purpose of code review?

Code review checks the actual diff against the requirement, the tests, and the scope before merge. It is there to find missing behaviour, weak assertions and unrelated changes while the work is still on the branch. It checks that code does not have any unnecessary stuff, follows best practices coding standards and does not have any breaking code.

6. What does a Git diff show?

A Git diff shows the line/each code change between two versions, such as a branch and main (or a commit 2 on a branch vs commit 1 on the same branch). It shows what was added, removed or changed.

7. What is a Definition of Done?

A Definition of Done is the agreed set of conditions that mean the work is finished/stable and ready to be part of main branch or is already part of it. In the issues above, that includes the behaviour implemented, the unit tests passing, the existing tests still passing, and the pull request reviewed and merged.

8. What is the appropriate role of GitHub Copilot in pull-request review?

Copilot can suggest review comments, does not replace a human review. The human reviewer checks the requirement, the assertions and the scope first then uses copilot to run a second review to catch if the human reviewer missed something and then records what was accepted or rejected by copilot suggestions.

9. Why should individual contribution not be judged only by commit count?


A high count can be many small or unclear commits, or one change split up so it looks like more work. Infact, you can add a new line and make it as a commit hence count does not show that the changes meet acceptance criteria, that the work is concrete and complete, it does not show that there is some significant work that has been done by the person for any of the requirement. One commit that says what changed and is backed by tests and review can be a stronger contribution than many commits that do not.

10. What is the Stage 6 engineering rule?

Trace each requirement through its issue, code, tests and pull request. Another member reviews the PR according to acceptance criteria mentioned in issues, then Copilot reviews as a fallback to catch if anything is missed, and any feedback is resolved before the final merge. 

## M Completion and handover

- Starting SHA: e5bdbf1d4eb482bee09fe683c42a528603667515
- Final Stage 6 code SHA: [response]
- Test command: python -m pytest
- Working directory: project/
- Observed result: On each feature commit separately, 11 passed (Python 3.13.12, pytest 8.3.5): 6733d4678cb97c6043e66cceafc543e87a58f753, 6328f69b356e66b46f18ed19d1a255801e8d83ce, c35a418b406fb866e5ea9c2ea72b6cf7256d72a3. 
- PR and another-member reviewer: https://github.com/DominicRDA-uc/st1-assignment-3/pull/5, https://github.com/DominicRDA-uc/st1-assignment-3/pull/6, https://github.com/DominicRDA-uc/st1-assignment-3/pull/7. Another-member reviewer: [response]
- Unresolved issue or none: Issues 2, 3 and 4 are open. Pull requests 5, 6 and 7 are open and not merged.
- Stage 7 handover status: unresolved work
- Final submitted SHA if later than tested SHA: [response and evidence-only difference]

- [X] Three Stage 6 service targets completed and checked.
- [X] Original supplied tests retained and passing.
- [X] At least two focused issues link requirements and acceptance criteria.
- [ ] Feature work reviewed by another member using the actual diff.
- [ ] Human-first review and required Copilot comparison recorded.
- [ ] Feedback resolved and approval recorded before merge.
- [ ] Everyone pulled main and integrated checks passed.
- [ ] Required activities, quiz responses and contribution notes completed.
- [ ] Only synthetic data included; confidential peer material kept out.
- [ ] Tutor can trace a requirement through issue, code, tests, PR and checkpoint.

Do not write a file's own future commit SHA into that file. Record the tested code SHA first, then commit the evidence; explain the difference when submitting.
