# Bourgault 7950B Tank 1 Conveyor Engineering

_Status: V7 engineering research / V3 donor-derived hierarchy recovered / no V7 transform change promoted yet_

This note isolates the remaining Tank 1 conveyor problem from the otherwise accepted four-compartment architecture. It records what is verified, what is only comparative evidence, and the exact solve procedure to use for V7.

A user-supplied working **4-Tank V3 front-to-rear** archive was recovered on 2026-09-16. The complete archive is not stored in the public repository because no redistribution license was present, but the required animation, mapping, pivot, fill-root, effect, and hydraulic reference data are now preserved under:

`equipment/bourgault_7950/reference/`

The recovered archive is identified by SHA-256:

`30eebabb116e1932a53f25b78feb41c37fdda66260933d05c560302db5f9d69a`

This V3 evidence is donor-derived reference material. It is **not** the later V6 Engineering archive and is not V7 authority by itself.

## 1. Problem statement

The current V6-derived Tank 1 discharge point is approximately **Z +1.650 m**.

The audited physical Tank 1 opening (opening A) spans approximately:

- rear edge: **Z +1.590 m**
- center: **Z +2.121 m**
- front edge: **Z +2.652 m**

The V6 discharge point is therefore only about **0.060 m** inside the rear edge of the opening. That is geometrically inside the hatch but does not provide enough trigger or visual margin to treat the position as final.

The existing V6 Tank 1 pose places the first two primary conveyor arms at approximately:

- primary arm 1: **107.99 degrees**
- primary arm 2: **-65.60 degrees**

The recovered V3 `loadingPipe` animation independently confirms the earlier donor-envelope measurements:

- `overloadingArm01` starts at **0 100 0**;
- `overloadingArm02` starts at **0 -50 0**.

Those values are now direct project reference evidence rather than only a prior audit estimate. V7 should reduce the V6 overtravel back toward this verified 7950 loading pose instead of increasing it.

## 2. Recovered V3 conveyor hierarchy

The V3 vehicle XML and I3D mapping resolve the conveyor as a four-node nested chain:

| Node | Vehicle mapping | I3D scene path | Static pivot translation |
|---|---|---|---|
| `overloadingArm01` | `0>0|6|0` | `0|0|6|0` | `-1.47003 1.56863 -1.22386` |
| `overloadingArm02` | `0>0|6|0|0` | `0|0|6|0|0` | `-0.173656 0.727869 -3.68031` |
| `overloadingArm03` | `0>0|6|0|0|0` | `0|0|6|0|0|0` | `-0.241337 0.219075 1.66861` |
| `overloadingArm04` | `0>0|6|0|0|0|0` | `0|0|6|0|0|0|0` | `0 0.418 -0.045` |

The recovered V3 animation segments establish that the donor mechanism is substantially richer than the first two swing rotations:

- Arm 1: **100 -> 90 -> 0 degrees about Y**.
- Arm 2: **-50 -> -33 -> 0 degrees about Y**.
- Arm 3: **-135 -> -64 -> 0 degrees about Y**.
- Arm 4: **21 -> 0 degrees about X**.
- Arm 4 also performs a downstream translation late in the sequence:
  - `0 0.28 -0.074` -> `0 0.611 -0.005`;
  - then -> `0 0.418 -0.045` for the final transport position.

Relevant outlet/effect references are also preserved:

- `conveyorEffect`: local translation `0.00383 -0.226519 7.13227`, rotation `2.84426 0 0`.
- `pipeEffect`: local translation `-0.00384 -0.258395 -4.10928`, rotation `-38.4184 65.9399 -129.594`.
- `conveyorBelts`: local translation `1.88502 -0.783007 3.28103`.

The four exact fill roots are children of the downstream conveyor assembly and their V3 mappings/transforms are preserved in `reference/V3_REFERENCE_COMPACT.json`.

### Hydraulic dependency evidence

The V3 XML also confirms that the visible hydraulic mechanisms are explicitly dependent on the animated conveyor nodes:

- `overloadingArm01` drives `overloadingArm01Hydraulic`.
- `overloadingArm02` drives `overloadingArm02Hydraulic`.
- `overloadingArm04` drives `overloadingArm03Hydraulic`.

The corresponding hydraulic reference transforms are preserved in the compact reference file. This matters for V7 because an apparently valid outlet coordinate can still produce an implausible hydraulic cylinder/linkage pose.

## 3. Manufacturer mechanical authority

Bourgault's 7000-series operating documentation establishes three operator-facing positioning functions for the load/unload conveyor:

1. **Inner Arm Swing** — In / Out.
2. **Outer Arm Swing** — In / Out.
3. **Conveyor Height** — Up / Down.

The operating procedure for changing tank openings is mechanically important for this project:

- raise the conveyor/spout clear of the tank opening with Conveyor Height;
- use Inner Arm Swing and Outer Arm Swing to manoeuvre the conveyor over the desired tank opening;
- lower the conveyor so the spout is inside the tank top opening.

The recovered V3 FS25 hierarchy is consistent with this manufacturer description: Arms 3-4 provide real downstream articulation beyond Arms 1-2. V7 should exploit those donor motions rather than forcing all additional Tank 1 reach into the first two swing joints.

The Bourgault Model 7950 manufacturer page separately confirms that the 7950 was offered with a load/unload conveyor using a 10-inch tube and 15-inch belt.

Bourgault support also lists model-specific instructions titled **Downspout Installation - 7950 A/C with a Conveyor (0252-41-01)**. The support index proves that a 7950-specific conveyor/downspout document exists, but its EzParts content has not yet been recovered into this project. Do not claim dimensions from that document until it is actually obtained.

## 4. Comparative evidence — not 7950 authority

A publicly posted GIANTS/Bourgault 71300 I3D from FS22 also uses a deeper conveyor hierarchy with additional downstream articulated nodes beneath the first two arms.

That comparison is now secondary evidence only. The recovered 7950 V3 archive itself proves that the 7950 donor uses four animated arm nodes, so no 71300 transform is required to justify downstream articulation.

Do **not** use 71300 joint angles, translations, node lengths, or keyframe values as 7950 authority.

## 5. V7 Tank 1 target envelope

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

## 6. Mechanical constraints for the next solve

Solve Tank 1 under these constraints:

1. **Do not move the physical tank opening or fill-volume envelope to meet the conveyor.** The Tank 1 opening and fill-volume geometry are already accepted.
2. **Do not increase primary-arm overtravel beyond V6.** The goal is to reduce it.
3. **Use the recovered V3 Arm 1 / Arm 2 start pose of 100 / -50 degrees as the verified donor loading reference.**
4. **Use the actual Arm 3 / Arm 4 downstream articulation from the recovered 7950 hierarchy.**
5. **Preserve spout orientation and insertion depth.** A solution that reaches the correct Z but points the downspout outside the hatch or leaves it above the trigger is not acceptable.
6. **Check the dependent hydraulic geometry at every proposed Tank 1 pose.**
7. **Do not disturb Tanks 2-4 unless their current poses conflict with the corrected shared animation.** Their existing discharge positions have much stronger opening margins.
8. **Do not copy 71300 transforms into the 7950.**

## 7. V7 solve procedure

The V3 hierarchy no longer needs to be re-uploaded to recover its baseline data. It is preserved in Git. The next engineering solve should proceed as follows:

1. Use `reference/V3_REFERENCE_COMPACT.json` as the recovered 7950 V3 hierarchy/pivot baseline.
2. Use `tools/extract_i3d_animation.py` on any later V6/V7 archive to identify candidate-specific differences from the V3 baseline.
3. Recalculate the world-space outlet/discharge transform through Arms 1-4 using the real nested hierarchy.
4. For Tank 1, hold Arms 1-2 at or near the verified **100 / -50** loading pose first.
5. Solve Arm 3 / Arm 4 rotation/translation for a discharge target near **Z +2.121 m** while preserving plausible spout height and angle.
6. Evaluate dependent hydraulic reference/cylinder geometry for the candidate pose.
7. If exact center cannot be reached without violating donor geometry, accept the closest pose inside **+1.790 to +2.452 m** that minimizes:
   - primary-joint overtravel;
   - spout-to-opening-center distance;
   - deviation from donor Arm 3 / Arm 4 articulation;
   - hydraulic/hose/linkage distortion risk.
8. Recalculate Tanks 2-4 after shared animation changes and ensure they remain inside their audited openings.
9. Integrate the corrected front/rear flap timing into the same V7 animation sequence.
10. Only then write/promote V7 animation values into `PATCH_SPEC.md` and generate a V7 candidate ZIP.

## 8. What not to do

- Do not retain Tank 1 at +1.650 m merely because the point is technically inside opening A.
- Do not solve the reach problem by moving `exactFillRootNodeTank1` toward an incorrectly positioned spout.
- Do not enlarge or shift the Tank 1 fill-volume mesh to hide conveyor misalignment.
- Do not add more rotation to Arms 1-2 before using the recovered Arm 3-4 articulation.
- Do not infer 7950 limits from the 71300 animation.
- Do not mark Tank 1 LOCKED from static calculations alone; hoses, linkage, trigger behavior and visual plausibility still require runtime review.

## 9. Current engineering conclusion

The recovered V3 files materially strengthen the V7 plan. We now have direct 7950 evidence for the **four-node conveyor hierarchy, the 100 / -50 donor loading pose on the first two arms, Arm 3 articulation, Arm 4 rotation/translation, outlet/effect transforms, and hydraulic dependencies**.

Therefore the V7 Tank 1 solution should no longer be based on extrapolating the first two arms. The preferred next solve is centered near **Z +2.121 m**, keeping Arms 1-2 near their verified V3 loading pose and obtaining the remaining positioning from the donor's actual downstream Arm 3 / Arm 4 mechanism.

What is still missing is the exact later **V6** animation/XML/I3D state, if we want to reproduce or compare the V6-specific +1.650 m pose byte-for-byte. The V3 baseline itself is now preserved in Git and should not need to be re-uploaded for future geometry work.
