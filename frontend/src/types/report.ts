export interface VehicleDetails {
  registration: string;
  make?: string;
  model?: string;
  colour?: string;
  fuel_type?: string;
  engine_capacity?: number;
  year_of_manufacture?: number;
  tax_status?: string;
  mot_status?: string;
  co2_emissions?: number;
  date_of_last_v5c_issued?: string;
}

export interface MotDefect {
  text: string;
  type: "FAIL" | "MAJOR" | "MINOR" | "ADVISORY" | "USER ENTERED";
  dangerous: boolean;
}

export interface MotTest {
  completed_date: string;
  test_result: "PASSED" | "FAILED";
  expiry_date?: string;
  odometer_value?: number;
  odometer_unit?: string;
  mot_test_number?: string;
  defects: MotDefect[];
}

export interface RiskFlag {
  date: string;
  type: string;
  text: string;
  dangerous: boolean;
}

export interface RiskFlags {
  tyres: RiskFlag[];
  brakes: RiskFlag[];
  rust_corrosion: RiskFlag[];
  suspension: RiskFlag[];
  lights: RiskFlag[];
  emissions: RiskFlag[];
  structural: RiskFlag[];
  other: RiskFlag[];
}

export interface RiskAnalysis {
  overall_risk: "low" | "medium" | "high";
  flags: RiskFlags;
  recurring_issues: string[];
  fail_count: number;
  advisory_count: number;
}

export interface MileagePoint {
  date: string;
  value: number;
  unit: string;
}

export interface MileageConsistency {
  consistent: boolean;
  anomalies: string[];
  values: MileagePoint[];
}

export interface Valuation {
  webuyanycar?: number;
  parkers_retail?: number;
  parkers_private?: number;
  source_note?: string;
}

export interface Recall {
  make?: string;
  concern?: string;
  remedy?: string;
  launch_date?: string;
}

export interface VehicleReport {
  registration: string;
  vehicle?: VehicleDetails;
  mot_history: MotTest[];
  risk_analysis?: RiskAnalysis;
  mileage_consistency?: MileageConsistency;
  valuation?: Valuation;
  recalls: Recall[];
  errors: Record<string, string>;
}
