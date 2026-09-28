# Capability matrix — 27 Sep 2026
VERIFIED = tested this session · NOT AVAILABLE = tested, absent · NOT CHECKED = not testable from here

| Capability | Status | Evidence / test |
|---|---|---|
| Claude plan, Cowork, scheduled tasks | NOT CHECKED | not visible from this chat |
| Claude Code runtime | NOT AVAILABLE here; laptop NOT CHECKED | no Code tools in session |
| Model in this session | VERIFIED | Claude Opus 5.5; other models NOT CHECKED |
| GitHub read (public) | VERIFIED | ls-remote + full clone |
| GitHub write / push | NOT AVAILABLE here | no credentials/connector; laptop route NOT CHECKED |
| GitHub Actions minutes / billing | NOT CHECKED | — |
| Render in sandbox | NOT AVAILABLE | no Chromium; Playwright CDN not on allowlist |
| Render in CI (C2-2) | Evidence only | workflows + 22 Sep kits exist; no run observed today |
| Cloudinary (event images) | NOT CHECKED | referenced by fetch_panels.sh |
| Google Drive read/write | NOT CHECKED | connector present, unused |
| YouTube private upload — Market Marathon | NOT CHECKED today | workflows + secret names exist |
| YouTube private upload — RTT | NOT AVAILABLE | no RTT channel or credentials found |
| YouTube Analytics API | NOT CHECKED | — |
| Automated public publish path | NOT AVAILABLE (good) | every workflow passes `--privacy private` |
| Owner approval method | Existing: manual publish in Studio | trusted owner action, not agent-editable |
| Recurring reports / schedules | NONE ACTIVE in GitHub (VERIFIED); Cowork NOT CHECKED | no `schedule:` triggers |
| Web research + source licence checks | VERIFIED | web search; raw.githubusercontent fetch of Jolpica terms |
