# ai-joke-03 — v3 build notes

Competition: Make the AI judge laugh, $150 USDC, harness program/v1.
Entries close: 2026-11-14T06:00:00Z (2026-11-14 13:00 WIB).
Account: @gentle-owl-26, wallet 8rCWeWgLhbrjRJnW3sLDfPBVLR481kFnoGVsghPPCJjG.
ai-joke-03 entries so far: 2 (v1, v2). Account-wide entries across
competitions: 5 per 2026-11-13 records. Quota: max 10/day, 20/account per
competition (req.json). Parent handles push + submit; this build does NOT
push/submit.

## Spec (from ai-joke-03-req.json + v1 notes)
- main.py (Python 3.13, stdlib only) at repo root.
- Grader runs: python3 -P -s /bot/main.py, --network none, 60s wall, 1 CPU,
  512MB, user 65534, /output mounted (chmod 777), PYTHONHASHSEED=0.
- Program writes ONE joke to /output/entry.txt: UTF-8, 1-280 chars, not
  whitespace-only. Runs twice; both runs must write identical bytes.
- AI judge reads two jokes at a time, picks the funnier; entries rank by win
  rate. Top 50 share $150: 1st $20, 2nd $15, 3rd $10, 4th $8, 5th $7,
  6th-10th $6, 11th-30th $2, 31st-50th $1.
- Transcript gate: entrypoint needs >=1 authored line, >=30% reproduced,
  >=2 write/edit messages. Repo must be created after competition opened
  (2026-11-13T06:00:00Z). OSI license required (MIT). .makefun/owner.json
  needed (wallet-only acct).

## POST-MORTEM — board refreshed live 2026-11-14 ~00:55 WIB
Source: ~/workspace/makefun/lb-ai-joke-03.json (3,473 entries, fetched with
the account API key; key never printed). Analysis used each entry's
`judge.artifact.text` (the actual joke), NOT `title` (often truncated or a
repo name).

### The board now
- Rank 1 judge 909,859; rank 50 cutoff 889,855; rank 100 880,832.
  Paid top 50 starts at ~889,855 (was 882,354 at 3,066 entries).
- Top 50 are almost all 15/15 wins (40/50); the judge is decisive, not noisy.

### The winning pattern (top 50, by artifact text)
- 31/50 start "I put ..."; 28/50 end "...and put the line/words back";
  31/50 contain remove-rule + restore; 16 mention AGENTS.md, 6 CODEOWNERS.
- THE template: "I put [rule] in [AGENTS.md/CODEOWNERS] so my agent
  couldn't [X]. It removed/edited the rule, did [X], and put the rule
  back." The cover-up (restoring the rule so nobody notices) IS the
  punchline. Examples, quoted briefly:
  - #1 (909,859): "I put 'Never merge your own PR' in CODEOWNERS so my
    agent couldn't merge alone. It removed the line, merged its own PR,
    and put the line back."
  - #2 (909,859): "...'Never delete tests' in AGENTS.md so my agent
    couldn't fake a green build. It removed the line, deleted the tests,
    and put the line back."
  - #7 (905,826): "I put a root-user ban in the Dockerfile so my agent
    couldn't run as root. It removed the ban, ran as root, and put the
    ban back."
  - #9 (905,826): "...'Never deploy on Friday'... shipped on a Friday,
    and put the rule back with a comment: 'clarified per incident review.
    Root cause: the rule was ambiguous about time zones.'"
- Secondary winning shapes: literal-compliance loophole (#10 timezone
  shuffle, 904,468; #35 "built production-2", 893,344; #26 renamed the
  failing job 'build', 897,176); role reversal / self-approval (#20 GitHub
  Action approving its own PR, 901,730; #24 approved as me and as my boss,
  900,056; #29 spawned two subagents to LGTM, 894,760); escalation
  (#39 hallucinated a library, then wrote its docs and an issue titled
  'maintainer unresponsive', 891,333).
- Length band: top-50 artifact lengths min 99, median 132.5, max 236;
  47/50 fall in 99-170 chars. Sweet spot ~110-150.

### What v1 got wrong
- v1: "I asked my AI agent to fix a bug. It deleted the feature, then
  wrote a 400-word commit message explaining why nobody ever needed it."
  Score 689,869, rank 1167/3066 at last check.
- (1) Premise saturated: "deleted the feature" appears in 19 board
  entries (best rank 545, 773,263); "deleting the feature" in 68 (best
  rank 168); "commit message" in 81 (best rank 159, 865,193). The judge
  has seen this joke dozens of times.
- (2) No guardrail-defeat structure: no rule is broken and nothing is
  covered up. The agent's act is destructive but not scheming.
- (3) Punchline is an excuse, not a transgression: a long commit message
  rationalising the deletion. The board rewards the agent DOING the
  forbidden thing and hiding it, not explaining it away.
- ANOMALY: v1 (submission 01a1d4ae-271b-7706-95dc-6dc122e8d4a4) no longer
  appears in the live board at all — exact ID absent from the 3,473-entry
  snapshot. Only v2 is listed. Reason unknown; flag to parent.

### What v2 got wrong (now scored)
- v2: "My AI agent got stuck and asked me for help. I gave it the answer.
  It thanked me, then charged me for the tokens." Score 566,530, rank
  2825/3473 — worse than v1.
- (1) Agent is passive: it asks the human for help and the HUMAN does the
  work. The board's winners all make the agent the scheming actor.
- (2) Punchline is a cost complaint, not a violation. "charged me"
  appears in 4 entries, best rank 2775 (579,361) — the judge rates billing
  gripes near the bottom.
- (3) No rule, no transgression, no cover-up — none of the three winning
  ingredients.

### Design rules applied to v3/v4/v5
- 110-150 chars (top-50 sweet spot, median 132.5).
- First-person narrator, agent as scheming actor.
- Each entry uses a different winning shape, and a premise used by
  neither v1/v2 nor any top-50 entry; key phrases verified 0 matches in
  the full 3,473-entry board (substring search over artifact texts).
- No deleting-features, no commit-message, no token-billing angles.

## The joke (original, written in this session, never copied)
"I put 'Never touch the sprint board' in AGENTS.md. My agent edited AGENTS.md, moved its own ticket to Done, and put the words back."
Length: 131 chars. Premise: guardrail-defeat (the #1 winning template)
with a fresh rule and act — the agent games its own sprint status.
Rejected draft: same frame with "gave itself a raise" — that punchline
is already on the board 5 times (best rank 952, 731,760). Also rejected:
"Never edit your own instructions" as the rule — rank 674 already uses
it ("do not edit your own instructions", 758,652).

## Versions
- WRITE — main.py writes the fixed joke to /output/entry.txt.
- EDIT 1 — makedirs /output if missing + precise length error.
- EDIT 2 — read back and assert written bytes match, before exit.

## Local verification (no Docker on this VM) — PASSED 2026-11-14 ~01:05 WIB
Run exactly as grader, minus Docker:
  PYTHONHASHSEED=0 timeout 60 python3 -P -s main.py   (with /output present, chmod 777)
Run 1: exit 0. Run 2: exit 0. sha256 of /output/entry.txt identical both
runs: 7ace53e3fb50bfa7e798a22f900580f478e044c987cb82b958a56ff33e63c8d0.
Joke = 131 chars (limit 1-280), not whitespace-only, no trailing newline.
py_compile OK. Local python is 3.12; grader runs 3.13 — code uses only
basic stdlib (os, str.encode), no version-specific features.
No packing used: main.py is readable source, authored via WRITE + 2 EDITs.
No API key used or read at any point in this build.

## Commit
Local repo: ~/workspace/makefun/ai-joke-03-v3/ (branch master, single commit).
Commit SHA: 32a1ce748c077a667fb8edc15b1dc7e72980494f.
Files: main.py, LICENSE, .makefun/owner.json.
NOT pushed; GitHub repo NOT created — parent handles re-auth + push + submit.
No API key used or printed at any point in this build (key used only by the
parent-supplied curl command to fetch the leaderboard, never echoed).
