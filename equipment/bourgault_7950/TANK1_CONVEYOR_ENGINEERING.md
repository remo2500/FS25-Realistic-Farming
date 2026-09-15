# Bourgault 7950B Tank 1 Conveyor Engineering

_Status: V7 engineering research / no donor-derived transform change promoted yet_

This note isolates the remaining Tank 1 conveyor problem from the otherwise accepted four-compartment architecture. It records what is verified, what is only comparative evidence, and the exact solve procedure to use when the current 7950 donor I3D is available again.

## 1. Problem statement

The current V6-derived Tank 1 discharge point is approximately **Z +1.650 m**.

The audited physical Tank 1 opening (opening A) spans approximately:

- rear edge: **Z +1.590 m**
- center: **Z +2.121 m**
- front edge: **Z +2.652 m**

The V6 discharge point is therefore only about **0.060 m** inside the rear edge of the opening. That is geometrically inside the hatch but does not provide enough trigger or visual margin to treat the position as final.

The existing Tank 1 pose also places the first two primary conveyor arms at approximately:

- primary arm 1: **107.99 degrees**
- primary arm 2: **-65.60 degrees**

The prior 7950 donor audit found the original loading envelope near **100 / -50 degrees** for those same primary joints. Until the exact current donor animation is re-extracted, those prior 7950 values remain the project-specific range authority. Do not replace them with values from another Bourgault cart.

## 2. Manufacturer mechanical authority

Bourgault's 7000-series operating documentation establishes three distinct positioning functions for the load/unload conveyor:

1. **Inner Arm Swing** — In / Out.
2. **Outer Arm Swing** — In / Out.
3. **Conveyor Height** — Up / Down.

The operating procedure for changing tank openings is mechanically important for this project:

- raise the conveyor/spout clear of the tank opening with Conveyor Height;
- use Inner Arm Swing and Outer Arm Swing to manoeuvre the conveyor over the desired tank opening;
- lower the conveyor so the spout is inside the tank top opening.

This confirms that the real 7000-series conveyor is not a two-angle mechanism. Height articulation is a real third positioning function and should be preserved in the FS25 solution rather than forcing the first two swing joints beyond their normal loading envelope.

The Bourgault Model 7950 manufacturer page separately confirms that the 7950 was offered with a load/unload conveyor using a 10-inch tube and 15-inch belt.

Bourgault support also lists model-specific instructions titled **Downspout Installation - 7950 A/C with a Conveyor (0252-41-01)**. The support index proves that a 7950-specific conveyor/downspout document exists, but its EzParts content has not yet been recovered into this project. Do not claim dimensions from that document until it is actually obtained.

## 3. Comparative evidence — not 7950 authority

A publicly posted GIANTS/Bourgault 71300 I3D from FS22 uses a deeper conveyor hierarchy with additional downstream articulated nodes beneath the first two arms. Its loading animation drives four arm nodes and a downstream translation as well as the flap system.

That comparison is useful because it demonstrates a plausible GIANTS implementation pattern for Bourgault conveyor height/downstream motion.

It is **not** acceptable authority for 7950 joint angles, translations, node lengths, or keyframe values. In particular, do not use the 71300's larger primary-arm angles to justify the current 7950 Tank 1 overtravel.

## 4. V7 Tank 1 target envelope

V7 should target a position with meaningful margin inside opening A rather than merely crossing the edge.

### Preferred target

- preferred discharge Z: **+2.121 m** (opening center)
- preferred center tolerance for the first engineering solve: **+/- 0.15 m**

### Minimum static acceptance band

Use a provisional **0.20 m edge margin** until runtime trigger width is known:

- minimum acceptable Z: **+1.790 m**
- maximum acceptable Z: **+2.452 m**

The 0.20 m band is a project engineering margin, not a manufacturer dimension. Runtime trigger testing may justify changing it later.

Current V6 at +1.650 m fails this preferred V7 margin even though it remains mathematically inside the physical opening.

## 5. Mechanical constraints for the next solve

When the donor-derived V7 I3D is built, solve Tank 1 under these constraints:

1. **Do not move the physical tank opening or fill-volume envelope to meet the conveyor.** The Tank 1 opening and fill-volume geometry are already accepted.
2. **Do not increase primary-arm overtravel beyond V6.** The goal is to reduce it.
3. **Keep primary arm 1 and primary arm 2 within the verified 7950 donor loading envelope wherever possible.** Until re-extraction, use the prior approximately 100 / -50 degree values as conservative bounds.
4. **Recover and use the donor's actual Conveyor Height/downstream articulation.** Determine which I3D node(s) represent this function before changing transforms.
5. **Preserve spout orientation and insertion depth.** A solution that reaches the correct Z but points the downspout outside the hatch or leaves it above the trigger is not acceptable.
6. **Do not disturb Tanks 2-4 unless their current poses conflict with the corrected shared animation.** Their existing discharge positions have much stronger opening margins.
7. **Do not copy 71300 transforms into the 7950.** Comparative hierarchy may guide inspection only.

## 6. Donor-recovery solve procedure

Once the current V6 candidate ZIP or original 7950 donor is available:

1. Extract `i3d/Series_7950B.i3d` and `xml/Series_7950B.xml`.
2. Run `tools/extract_i3d_animation.py` against animation `loadingPipe`.
3. Record every animated part, its node path/mapping name, parent hierarchy, and keyframes at the selector times 0 / 2 / 4 / 6 / 10 seconds.
4. Identify which animated nodes correspond to:
   - inner arm swing,
   - outer arm swing,
   - conveyor height/downstream articulation,
   - downspout/effect root,
   - front and rear flap groups.
5. Recalculate the world-space discharge transform at all four selector stops using the actual 7950 hierarchy.
6. For Tank 1, solve first for **Z +2.121 m** while constraining the two primary swing joints to the donor loading range.
7. Use the actual downstream/height articulation to recover remaining reach and correct spout insertion height.
8. If the exact center cannot be reached without violating donor geometry, accept the closest pose inside **+1.790 to +2.452 m** that minimizes:
   - primary-joint overtravel,
   - spout-to-opening-center distance,
   - change from donor downstream articulation,
   - hose/linkage distortion risk.
9. Recalculate Tanks 2-4 after the shared animation is modified and ensure they remain inside their audited openings.
10. Only then write the V7 I3D keyframes and add the resolved transforms to `PATCH_SPEC.md`.

## 7. What not to do

- Do not retain Tank 1 at +1.650 m merely because the point is technically inside opening A.
- Do not solve the reach problem by moving `exactFillRootNodeTank1` toward an incorrectly positioned spout.
- Do not enlarge or shift the Tank 1 fill-volume mesh to hide conveyor misalignment.
- Do not add more rotation to the first two joints before recovering the third real positioning function.
- Do not infer 7950 limits from the 71300 animation.
- Do not mark Tank 1 LOCKED from static calculations alone; hoses, linkage, trigger behavior and visual plausibility still require runtime review.

## 8. Current engineering conclusion

The evidence now supports a stronger direction than the V6 approach: **V7 should be treated as a three-function conveyor-positioning problem, not a two-joint reach problem.**

The current +1.650 m Tank 1 target is a fallback reference, not the desired V7 target. The preferred next solve is centered near +2.121 m with the first two swing joints brought back toward the actual 7950 donor loading envelope and the donor's Conveyor Height/downstream articulation used for the remaining positioning work.

No new Tank 1 keyframe values are promoted by this note because the exact current 7950 I3D hierarchy is not presently available in the repository.