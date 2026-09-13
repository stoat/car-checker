"""
MOT history analysis engine.

Classifies defects into maintenance risk categories, detects recurring issues,
and checks mileage consistency across test history.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict

from app.schemas.report import (
    MileageConsistency,
    MileagePoint,
    MotTest,
    RiskAnalysis,
    RiskFlag,
    RiskFlags,
)

# ---------------------------------------------------------------------------
# Category keyword rules — order matters (first match wins)
# ---------------------------------------------------------------------------

CATEGORY_RULES: list[tuple[str, list[str]]] = [
    ("rust_corrosion", [
        r"corrosion", r"corroded", r"rust", r"load.?bearing", r"structural member",
        r"subframe", r"sill", r"chassis",
    ]),
    ("suspension", [
        r"suspension", r"damper", r"shock.?absorber", r"spring",
        r"wishbone", r"ball.?joint", r"steering.?rack", r"track.?rod",
        r"anti.?roll", r"hub", r"bearing.*wheel", r"wheel.*bearing",
        r"CV.?joint", r"drive.?shaft",
    ]),
    ("brakes", [
        r"brake", r"braking", r"caliper", r"calliper", r"disc", r"drum",
        r"handbrake", r"parking.?brake", r"brake.?fluid", r"brake.?pipe",
        r"brake.?hose",
    ]),
    ("tyres", [
        r"tyre", r"tire", r"tread", r"sidewall", r"tread.?depth",
        r"spare.?tyre",
    ]),
    ("lights", [
        r"light", r"lamp", r"headlight", r"headlamp", r"indicator",
        r"tail.?light", r"brake.?light", r"stop.?light", r"reflector",
    ]),
    ("emissions", [
        r"emission", r"exhaust", r"catalyst", r"catalytic", r"lambda",
        r"smoke", r"diesel.?particulate", r"DPF",
    ]),
    ("structural", [
        r"body.?work", r"floor.?pan", r"inner.?wing", r"bulkhead",
        r"seat.?belt", r"seatbelt", r"airbag",
    ]),
]

_COMPILED_RULES: list[tuple[str, list[re.Pattern]]] = [
    (cat, [re.compile(kw, re.IGNORECASE) for kw in keywords])
    for cat, keywords in CATEGORY_RULES
]


def _categorise(text: str) -> str:
    for category, patterns in _COMPILED_RULES:
        for pat in patterns:
            if pat.search(text):
                return category
    return "other"


def _severity_weight(defect_type: str) -> int:
    """Higher = worse."""
    return {"FAIL": 3, "MAJOR": 3, "MINOR": 2, "ADVISORY": 1}.get(defect_type.upper(), 1)


def analyse(tests: list[MotTest]) -> RiskAnalysis:
    flags = RiskFlags()
    fail_count = 0
    advisory_count = 0

    # Track (category, normalised_text) across MOT cycles to detect recurrence
    cycle_occurrences: dict[tuple[str, str], list[str]] = defaultdict(list)

    for test in tests:
        date = test.completed_date[:10] if test.completed_date else "unknown"

        for defect in test.defects:
            dtype = defect.type.upper()
            if dtype in ("FAIL", "MAJOR"):
                fail_count += 1
            elif dtype in ("ADVISORY", "MINOR"):
                advisory_count += 1

            category = _categorise(defect.text)
            flag = RiskFlag(
                date=date,
                type=dtype,
                text=defect.text,
                dangerous=defect.dangerous,
            )

            getattr(flags, category).append(flag)

            # Normalise text for recurrence detection (lowercase, collapse whitespace)
            norm = re.sub(r"\s+", " ", defect.text.lower().strip())
            cycle_occurrences[(category, norm)].append(date)

    # Detect recurring issues: same defect in 2+ different MOT cycles
    recurring: list[str] = []
    for (category, norm_text), dates in cycle_occurrences.items():
        if len(dates) >= 2:
            recurring.append(
                f"{category.replace('_', ' ').title()}: \"{norm_text}\" "
                f"({len(dates)} occurrences: {', '.join(sorted(set(dates)))})"
            )

    # Score overall risk
    high_severity = sum(
        1
        for test in tests
        for d in test.defects
        if d.type.upper() in ("FAIL", "MAJOR")
    )
    if high_severity >= 5 or len(flags.rust_corrosion) >= 2 or len(recurring) >= 3:
        overall_risk = "high"
    elif high_severity >= 2 or len(recurring) >= 1 or len(flags.rust_corrosion) >= 1:
        overall_risk = "medium"
    else:
        overall_risk = "low"

    return RiskAnalysis(
        overall_risk=overall_risk,
        flags=flags,
        recurring_issues=recurring,
        fail_count=fail_count,
        advisory_count=advisory_count,
    )


def check_mileage(tests: list[MotTest]) -> MileageConsistency:
    """
    Check odometer readings across MOT tests for consistency.

    Sort by date ascending and flag any decrease in mileage (potential clocking)
    or suspicious jumps (>50k miles in a single year).
    """
    points: list[MileagePoint] = []
    anomalies: list[str] = []

    sorted_tests = sorted(
        [t for t in tests if t.odometer_value is not None],
        key=lambda t: t.completed_date,
    )

    for test in sorted_tests:
        points.append(MileagePoint(
            date=test.completed_date[:10],
            value=test.odometer_value,  # type: ignore[arg-type]
            unit=test.odometer_unit or "mi",
        ))

    for i in range(1, len(points)):
        prev, curr = points[i - 1], points[i]
        diff = curr.value - prev.value

        if diff < 0:
            anomalies.append(
                f"Mileage decreased from {prev.value:,} to {curr.value:,} "
                f"between {prev.date} and {curr.date} — possible clocking"
            )
        elif diff > 50_000:
            anomalies.append(
                f"Unusually large mileage jump: {diff:,} miles "
                f"between {prev.date} and {curr.date}"
            )

    return MileageConsistency(
        consistent=len(anomalies) == 0,
        anomalies=anomalies,
        values=points,
    )
