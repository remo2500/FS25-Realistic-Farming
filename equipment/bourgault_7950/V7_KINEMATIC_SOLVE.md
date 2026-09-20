# Bourgault 7950B V7 Tank 1 Kinematic Solve

_Status: static engineering recommendation; not yet promoted to a donor-derived V7 archive_

This document records the first reproducible Tank 1 kinematic solve using the actual 7950 conveyor hierarchy recovered from the uploaded Hispano V3 reference archive.

## 1. Source authority

Reference archive:

- `FS25_Bourgault_Series_3320.zip`
- SHA-256 `30eebabb116e1932a53f25b78feb41c37fdda66260933d05c560302db5f9d69a`
- Hispano version `2.0.0.4`
- title `Bourgault 3320-76 + 7950 Air Cart [4-Tank V3 F-R]`

The donor-safe compact snapshot is stored under:

`equipment/bourgault_7950/reference/`

Forward calculations are reproducible with:

`tools/bourgault7950_forward_kinematics.py`

## 2. Recovered conveyor chain

The loading conveyor is a nested four-arm chain:

1. `overloadingArm01`
2. `overloadingArm02`
3. `overloadingArm03`
4. `overloadingArm04`

Recovered loading-state transforms:

| Item | V3 loading value |
|---|---:|
| Arm 1 rotation Y | +100 deg |
| Arm 2 rotation Y | -50 deg |
| Arm 3 rotation Y | -135 deg |
| Arm 4 rotation X | +21 deg |
| Arm 4 translation | `0 0.28 -0.074` |

The relevant arm pivot translations are:

- Arm 1: `-1.47003 1.56863 -1.22386`
- Arm 2: `-0.173656 0.727869 -3.68031`
- Arm 3: `-0.241337 0.219075 1.66861`
- Arm 4 donor loading translation: `0 0.28 -0.074`

The tank-side discharge/effect point used for the solve is the recovered `pipeEffect` local translation:

`-0.00384 -0.258395 -4.10928`

## 3. Transform-model cross-check

At the untouched V3 loading pose:

- Arm 1 = 100 deg
- Arm 2 = -50 deg
- Arm 3 = -135 deg
- Arm 4 = 21 deg

The reconstructed pipe-effect position is approximately:

`X +0.046205 / Y +4.026976 / Z +0.490969 m`

That is consistent with the old V3 cart being unable to reach the front-most physical opening correctly.

More importantly, applying the previously audited V6 Tank 1 primary-arm values:

- Arm 1 = 107.99 deg
- Arm 2 = -65.60 deg
- Arm 3 = -135 deg
- Arm 4 = 21 deg

produces:

`X +0.028876 / Y +4.026976 / Z +1.651514 m`

The earlier V6 geometry audit reported Tank 1 discharge Z approximately **+1.650 m**. The reconstructed result differs by only about **1.5 mm**. This is a strong independent validation of the hierarchy, coordinate convention, and transform model.

## 4. Important constraint discovery

Opening A spans approximately:

- rear edge: Z +1.590 m
- center: Z +2.121 m
- front edge: Z +2.652 m

Numerical search across the recovered V3 loading/stow ranges found **no donor-range-only solution** that reaches opening A.

Even allowing the full observed ranges for Arms 1-4 and the observed Arm-4 translation range, the maximum forward pipe-effect Z is only about **+1.182 m**, and that pose is badly displaced laterally.

Therefore, with the existing conveyor geometry, **some articulation outside the original V3 animation envelope is unavoidable** for the new front Tank 1. The engineering choice is not whether to exceed the V3 loading envelope; it is where to place that extra articulation with the least mechanical/visual penalty.

## 5. V6 comparison

V6 obtained approximately Z +1.650 m by keeping Arm 3 at -135 deg and pushing the first two primary joints to approximately:

- Arm 1: +107.99 deg, +7.99 deg beyond donor loading pose
- Arm 2: -65.60 deg, -15.60 deg beyond donor loading pose

Recovered hydraulic geometry shows that this increases the modeled hydraulic lengths by approximately:

- Arm 1 cylinder: **+2.626%** versus donor loading pose
- Arm 2 cylinder: **+7.457%** versus donor loading pose

This confirms the concern that V6 concentrated too much of the extra reach in the first two hydraulically represented joints.

## 6. Distributed V7 solve

A more balanced solution was calculated by keeping Arm 4 at the donor loading rotation/translation and minimizing total angle deviation across Arms 1-3 while constraining the pipe effect to the tank centerline.

### Minimum provisional acceptance boundary — Z +1.790 m

This is the existing project acceptance boundary: 0.20 m inside the rear edge of opening A.

Solved pose:

- Arm 1: **+104.483805 deg**
- Arm 2: **-58.559467 deg**
- Arm 3: **-144.472086 deg**
- Arm 4: **+21 deg**
- Arm 4 translation: `0 0.28 -0.074`

Pipe effect:

`X 0.000000 / Y +4.026976 / Z +1.790000 m`

Modeled hydraulic change versus donor:

- Arm 1: **+1.500%**
- Arm 2: **+4.048%**

### Recommended first V7 engineering target — Z +1.900 m

The exact +1.790 m boundary leaves no calculation tolerance. For the first V7 candidate, a slightly deeper target is preferable while still avoiding the larger center-target overtravel.

Recommended pose:

- Arm 1: **+105.164095 deg**
- Arm 2: **-59.356622 deg**
- Arm 3: **-145.314298 deg**
- Arm 4: **+21 deg**
- Arm 4 translation: `0 0.28 -0.074`

Pipe effect:

`X 0.000000 / Y +4.026976 / Z +1.900000 m`

Opening-A margins:

- rear-edge margin: **0.310 m**
- front-edge margin: **0.752 m**
- center offset: **-0.221 m** (rearward of center)

Modeled hydraulic change versus donor:

- Arm 1 cylinder: **+1.722%**
- Arm 2 cylinder: **+4.432%**

Compared with V6, this reduces the amount of hydraulic extension beyond the donor loading pose by approximately:

- Arm 1: **34.4% less excess extension**
- Arm 2: **40.6% less excess extension**

The total angular deviation from the original loading pose is also about **15.3% lower** than the V6 two-joint solution, even though the deviation is deliberately distributed across three joints.

### Exact opening-center solution — Z +2.121 m

Mathematically, the opening center can also be reached while keeping Arm 4 at the donor loading pose:

- Arm 1: **+106.584529 deg**
- Arm 2: **-60.997442 deg**
- Arm 3: **-146.992740 deg**
- Arm 4: **+21 deg**

Pipe effect:

`X 0.000000 / Y +4.026976 / Z +2.121000 m`

Modeled hydraulic change versus donor:

- Arm 1: **+2.180%**
- Arm 2: **+5.224%**

This is better distributed than V6 but imposes more total extra articulation than the +1.900 m candidate. It should therefore remain the second-choice position unless runtime filling proves that the +1.900 m target does not provide enough trigger/visual margin.

## 7. Arm-3-only alternative

It is mathematically possible to keep Arms 1 and 2 exactly at the donor 100 / -50 deg loading pose and obtain extra reach by rotating Arm 3 alone.

Required Arm-3 values would be approximately:

| Target Z | Arm 3 |
|---:|---:|
| +1.590 m | -150.800 deg |
| +1.790 m | -153.730 deg |
| +1.900 m | -155.356 deg |
| +2.121 m | -158.663 deg |

Although this avoids additional extension of the Arm-1/Arm-2 hydraulics, it asks Arm 3 for 15.8-23.7 degrees beyond its recovered loading pose. Without a visual collision/linkage review, that is too much concentrated overtravel to promote as the primary solution.

## 8. Tank 2 / Tank 3 baseline confirmation

The recovered hierarchy also explains why the later V6 Tank 2 and Tank 3 targets were strong:

- V3 donor loading pose `100 / -50 / -135 / 21` produces pipe Z approximately **+0.491 m**, essentially the later V6 Tank 2 target of +0.493 m.
- V3 state `90 / -33 / -135 / 21` produces pipe Z approximately **-0.775 m**, essentially the later V6 Tank 3 target of -0.769 m.

This means Tanks 2 and 3 can remain very close to genuine donor-range states while Tank 1 receives the special forward-reach treatment.

## 9. Recommended V7 action

For the first donor-derived V7 build, use **Z +1.900 m** as the Tank 1 engineering target and the distributed pose:

`Arm1 105.164095 / Arm2 -59.356622 / Arm3 -145.314298 / Arm4 21`

Do not yet mark it LOCKED.

Before promotion:

1. Insert this stop into the actual V7 `loadingPipe` sequence.
2. Recalculate the hydraulic dependent parts through the normal `cylindered` system.
3. Inspect the Arm-3 joint, hoses, nearby tank structure, and collision geometry in GIANTS Editor/in game.
4. Verify the pipe effect is visibly over opening A and that the exact-fill trigger fills only Tank 1.
5. If runtime trigger margin is inadequate, move toward the +2.121 m center solution rather than returning to the V6 two-joint overtravel strategy.

## 10. Current conclusion

The recovered 7950 donor geometry changes the Tank 1 assessment from speculation to a reproducible kinematic result.

- The V6 +1.650 m pose has been independently reproduced.
- A donor-range-only front-Tank solution is impossible with the existing geometry.
- The best current V7 strategy is **distributed controlled overtravel**, not additional Arm-1/Arm-2 overtravel and not Arm-3-only overtravel.
- **Z +1.900 m** is the recommended first V7 engineering stop because it provides substantially better physical opening margin than V6 while reducing the modeled hydraulic penalty.
