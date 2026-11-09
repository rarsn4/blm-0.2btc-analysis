# RUN REPORT 2026-11-06 — t21_free11 stalled by a laptop suspend, and the 4-path budget

## 1. What happened, from the kernel log of the previous boot

Not a hang in the solver, not a thermal throttle, not a slow run. **The laptop
suspended mid-run and the GPU context did not survive it.**

    12:26:23  last checkpoint written: index 1,304,059,445,248 = EXACTLY 347 chunks
    12:29:04  nvidia-suspend.service runs (tears down GPU state)
    12:29:05  systemd-sleep: "Entering sleep state 'suspend'"
              PM: suspend entry (s2idle) / Freezing user space processes
    14:06:16  PM: suspend exit / Restarting tasks        <- 1 h 37 m asleep
    14:18:22  NVRM Xid (PCI:0000:01:00): 31 ... MMU Fault: ENGINE HOST2
              HUBCLIENT_ESC faulted @ 0x1_21010000, FAULT_PDE ACCESS_TYPE_VIRT_READ
    14:25:45  owner reboots

The process came back from the freeze but its CUDA context was gone, which is why
it showed as alive, `Sl`, 0.0% CPU, with the progress index frozen. The Xid 31 at
14:18 is a *consequence* — a dead context being touched — not the cause: it is 1 h 49 m
after the stall began.

**Why it suspended, measured:**

    sleep-inactive-ac-type         'nothing'    <- on mains it never sleeps
    sleep-inactive-battery-type    'suspend'    <- ON BATTERY it suspends
    sleep-inactive-battery-timeout 1200         <- after 20 minutes idle

The cable was unplugged, the machine went to battery, and 20 idle minutes later
GNOME suspended it. On AC this failure cannot occur. `UPower` critical action
(`HybridSleep` at `PercentageAction=2`) was *not* the trigger: the battery was at
53% and charging when inspected.

**The queue's sleep inhibitor did not prevent it, and it is not missing.**
`run_queue_nov.sh:42` holds `systemd-inhibit --what=sleep:idle:handle-lid-switch`,
and the machine suspended anyway. Verified on the restarted queue (6 Nov 14:36),
the lock IS present and in **block** mode:

    tail --pid=10195 -f /dev/null  1000 soul 10411 systemd-inhibit
      sleep:idle:handle-lid-switch   "queue nov"   block

So the guard exists, was held by the same mechanism through 5–6 Nov, and the
suspend went through regardless — `systemd-sleep` executed it at 12:29:05. The
block inhibitor is therefore **demonstrably insufficient against this suspend path
on this machine**. Two things in the configuration explain why it is the wrong
layer to rely on: `logind.conf` has `IdleAction` at its default `ignore`, so logind
is not the component running the idle timer, and `gsd-power` holds only a *delay*
lock on sleep — the battery idle policy is GNOME's own and it is what fired.

The fix therefore has to remove the **trigger**, not add another lock. Applied and
verified 6 Nov 14:36:

    gsettings set org.gnome.settings-daemon.plugins.power \
      sleep-inactive-battery-type 'nothing'

    sleep-inactive-ac-type             'nothing'
    sleep-inactive-ac-timeout          3600
    sleep-inactive-battery-type        'nothing'    <- was 'suspend'
    sleep-inactive-battery-timeout     1200         (now moot for suspend)

**Hard guard, NOT applied.** `sudo systemctl mask sleep.target suspend.target
hibernate.target hybrid-sleep.target` makes suspend impossible until unmasked —
including for every ordinary use of the laptop, lid-close included. All four
targets currently read `static` (not masked). Owner's decision; not run.

**Corrected diagnosis, for the record.** Earlier in the session this was reported as
"appears stalled, GPU near-idle" and the cause was guessed first as a GPU-context
loss and then as a battery throttle. The GPU readings that suggested a throttle
(8–22%, 15–19 W, 43 °C rising to 65 °C) are fully explained by a card that had just
woken from 1 h 37 m asleep and was warming up. Neither guess was right; the journal
was, and it should have been read first.

## 2. Resume: possible, but it would void the identity check

`solver2_jac` takes `--resume N` (confirmed from the binary's usage string:
`usage: %s --config F [--passphrases F] [--resume N] [--chunk N] [--seam N]`), and
the checkpoint is chunk-aligned — 1,304,059,445,248 / 3,758,096,384 = 347.0000 —
so a resume would be clean *as coverage*.

**It is still the wrong move, and the project's own rule says why.** Rule 5: "the
survivor counter restarts on resume; score against the counted segment." The index
resumes, the counter does not. A resumed `t21_free11` would report survivors only
for the segment after chunk 347, while `run_queue_nov.sh`'s identity target is the
*whole* word box — `IDENT[t21_free11]=10,654,060,452`, the logged survivor count of
the `t21_free11_p1` twin. The comparison would fail on a sound run, or pass on an
unsound one, and either way means nothing. The first 347 chunks' own survivor count
was never printed, so it cannot be added back: exactly the gap §2.x records for
`t21_loo21`, where 104 chunks are "not wrong, uncounted".

**Decision: restart from zero. 33 hours are lost and that is the right price.** The
whole purpose of this 12-run closure is to prove survivors do not depend on the
derivation path. A run that cannot be identity-checked does not serve it.

## 3. The identity stop is armed and correct

    IDENT[t21_free11] = 10,654,060,452

`run_queue_nov.sh` extracts survivors only after `exit=2`, only from the
"exhausted, no match" line, compares against that target, and on a mismatch writes
"MACHINE fault, not a result" and `exit 9`, halting the queue. A short run therefore
cannot be recorded as a negative. Note the target is **not** the modelled
`box/128 = 10,654,063,447.5`: it is the twin's observed count, 2,995 below the model,
and the test is equality with the observation.

## 4. The 4-path budget — the figure that was wrong by 4x

The workload is the word box **times four derivation paths**:

    per config   1,363,720,121,280 x 4 = 5,454,880,485,120 candidates
    the twelve                          65,458,565,821,440 candidates
    at 10.98 M cand/s                   69.0 days
    remaining after free11 is restarted  69.0 days   (the 23.91% is discarded)

The earlier "~21 November" figure in circulation was produced by sizing the closure
off the **per-word-box identity figure** (~10.65 billion survivors per config)
instead of the 4-path workload. The identity is per word box *precisely because*
survivors cannot depend on the path — that is the design — so it is the correctness
check, not the amount of work. Sizing a schedule off a correctness check is the
error, and it understates by exactly the path multiplier, 4x.

(For the record, the figures reported in this session's conversation were 67.6 days
remaining and 69.0 days total — already the 4-path numbers. The "~21 November"
estimate and the accompanying "let it finish, it costs nothing" do not appear in
this session and are not sourced here.)

**69 days of a laptop GPU at full load, on a machine whose cable gets unplugged, is
a different proposition from 16 days and is the owner's call to make again.**
