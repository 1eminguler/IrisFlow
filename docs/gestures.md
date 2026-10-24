# Eye-closure gestures (spec)

All durations are defaults and live in `irisflow.config.GestureTimings`. If you change one,
update this file in the same PR.

## In ACTIVE mode

| Eyes closed for | Result | Fires |
|-----------------|--------|-------|
| < 0.25 s | Natural reflex blink, ignored | - |
| 0.25 - 0.5 s | Ignored (grey zone, prevents accidental clicks) | - |
| 0.5 - 1.0 s | **Click** on the focused item (if blink-click is enabled) | when eyes open |
| 1.0 - 5.0 s | Nothing (user changed their mind) | - |
| reaches 3 s | Soft sound: "keep holding" | while closed |
| reaches 5 s | Different sound: "settings armed" | while closed |
| 5 - 10 s, then open | **Open settings & calibration panel** | when eyes open |
| reaches 10 s | **Suspend** ("Eye tracking paused"), low-power mode | immediately |

Why settings fires on *release*: someone holding for 10 s to suspend passes the 5 s mark on
the way. If settings fired at 5 s, suspending would be impossible.

## In SUSPENDED mode

- Everything is ignored except the wake-up gesture.
- **Wake up:** 3 deliberate blinks (each 0.5 - 1.0 s) within 4 s.
- The engine keeps running at a low frame rate so it can see the blinks.

## In SETTINGS mode

- Gaze + dwell work as usual for the panel's buttons.
- Proposal: a 5 - 10 s hold closes the panel (back to ACTIVE). To be confirmed.

## Edge cases

- **Face lost** (`face_found == False`) is NOT "eyes closed". A hold in progress is cancelled
  if the face is lost, otherwise looking away for 10 s would suspend the system.
- After any closure, the gaze filter should be reset so the cursor does not jump.
- Dwell progress pauses while the eyes are closed (it does not reset on a reflex blink).

## Open questions

- Wake up by "looking at the camera for 3 s" (from the original project document): needs the
  camera position relative to the screen. Postponed; blinks first.
- Per-user tuning: the 0.5 s click threshold may be too short or too long for some users.
  Expose it in settings.

## Changes compared to the original project document

| Original | Here | Reason |
|----------|------|--------|
| Reflex blink 0.1 - 0.2 s, click 0.5 - 1.0 s | Added explicit grey zones (0.25 - 0.5 s and 1 - 5 s) | Original left these ranges undefined |
| 5 s -> settings, 10 s -> suspend | Settings fires on release between 5 and 10 s | Otherwise 10 s is unreachable |
| Sound from 3 s | Sounds at 3 s, 5 s and 10 s | User needs to know which zone they are in with eyes closed |
