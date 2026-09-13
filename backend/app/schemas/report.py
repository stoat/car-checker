from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class VehicleDetails(BaseModel):
    registration: str
    make: str | None = None
    model: str | None = None
    colour: str | None = None
    fuel_type: str | None = None
    engine_capacity: int | None = None
    year_of_manufacture: int | None = None
    tax_status: str | None = None
    mot_status: str | None = None
    co2_emissions: int | None = None
    date_of_last_v5c_issued: str | None = None


class MotDefect(BaseModel):
    text: str
    type: str   # "FAIL" | "MAJOR" | "MINOR" | "ADVISORY" | "USER ENTERED"
    dangerous: bool = False


class MotTest(BaseModel):
    completed_date: str
    test_result: str   # "PASSED" | "FAILED"
    expiry_date: str | None = None
    odometer_value: int | None = None
    odometer_unit: str | None = None
    mot_test_number: str | None = None
    defects: list[MotDefect] = []


class RiskFlag(BaseModel):
    date: str
    type: str
    text: str
    dangerous: bool = False


class MileagePoint(BaseModel):
    date: str
    value: int
    unit: str


class MileageConsistency(BaseModel):
    consistent: bool
    anomalies: list[str] = []
    values: list[MileagePoint] = []


class RiskFlags(BaseModel):
    tyres: list[RiskFlag] = []
    brakes: list[RiskFlag] = []
    rust_corrosion: list[RiskFlag] = []
    suspension: list[RiskFlag] = []
    lights: list[RiskFlag] = []
    emissions: list[RiskFlag] = []
    structural: list[RiskFlag] = []
    other: list[RiskFlag] = []


class RiskAnalysis(BaseModel):
    overall_risk: str   # "low" | "medium" | "high"
    flags: RiskFlags
    recurring_issues: list[str] = []
    fail_count: int = 0
    advisory_count: int = 0


class Valuation(BaseModel):
    webuyanycar: float | None = None
    parkers_retail: float | None = None
    parkers_private: float | None = None
    source_note: str | None = None


class Recall(BaseModel):
    make: str | None = None
    concern: str | None = None
    remedy: str | None = None
    launch_date: str | None = None


class VehicleReport(BaseModel):
    registration: str
    vehicle: VehicleDetails | None = None
    mot_history: list[MotTest] = []
    risk_analysis: RiskAnalysis | None = None
    mileage_consistency: MileageConsistency | None = None
    valuation: Valuation | None = None
    recalls: list[Recall] = []
    errors: dict[str, str] = {}
