from typing import Optional

from pydantic import BaseModel
from pydantic.validators import datetime
from sqlalchemy import DateTime, Float, Boolean

class MedicalRecordSchema(BaseModel):
    """
    定义pydantic模型
    """

    personal_id: Optional[str] = None
    individual_code: Optional[str] = None
    days_visiting_two_hospitals: Optional[int] = None
    months_of_visits: Optional[int] = None
    max_days_visited_per_month: Optional[int] = None
    avg_days_visited_per_month: Optional[float] = None
    max_hospitals_visited_per_month: Optional[int] = None
    avg_hospitals_visited_per_month: Optional[float] = None
    total_visits_count: Optional[int] = None
    max_visits_per_month: Optional[int] = None
    avg_visits_per_month: Optional[float] = None
    max_total_amount_per_month: Optional[float] = None
    avg_total_amount_per_month: Optional[float] = None
    max_medicine_amount_per_month: Optional[float] = None
    avg_medicine_amount_per_month: Optional[float] = None
    hospital_max_days_visited: Optional[int] = None
    hospital_avg_days_visited: Optional[float] = None
    hospital_max_coordinated_fund: Optional[float] = None
    hospital_avg_coordinated_fund: Optional[float] = None
    hospital_max_medicine: Optional[float] = None
    hospital_avg_medicine: Optional[float] = None
    hospital_code_nn: Optional[str] = None
    sequence_number_nn: Optional[str] = None
    transaction_time_dd_nn: Optional[str] = None
    transaction_time_yyyy_nn: Optional[str] = None
    transaction_time_yyyymm_nn: Optional[str] = None
    total_days_of_hospitalization_sum: Optional[int] = None
    personal_account_balance_sum: Optional[float] = None
    coordinated_payment_sum: Optional[float] = None
    all_sum: Optional[float] = None
    available_account_reimbursement_sum: Optional[float] = None
    medicine_cost_sum: Optional[float] = None
    self_paid_medicine_cost_sum: Optional[float] = None
    claimed_medicine_cost_sum: Optional[float] = None
    expensive_medicine_cost_sum: Optional[float] = None
    tcm_drug_cost_sum: Optional[float] = None
    herbal_medicine_cost_sum: Optional[float] = None
    examination_fee_sum: Optional[float] = None
    self_paid_examination_fee_sum: Optional[float] = None
    claimed_examination_fee_sum: Optional[float] = None
    expensive_examination_fee: Optional[float] = None
    treatment_fee_sum: Optional[float] = None
    self_paid_treatment_fee_sum: Optional[float] = None
    claimed_treatment_fee_sum: Optional[float] = None
    surgery_fee_sum: Optional[float] = None
    self_paid_surgery_fee_sum: Optional[float] = None
    claimed_surgery_fee_sum: Optional[float] = None
    bed_fee_sum: Optional[float] = None
    bed_fee_claimed_sum: Optional[float] = None
    medical_materials_cost_sum: Optional[float] = None
    high_cost_medical_materials_sum: Optional[float] = None
    self_paid_medical_materials_fee_sum: Optional[float] = None
    component_transfusion_claimed_sum: Optional[float] = None
    other_costs_sum: Optional[float] = None
    other_claimed_costs_sum: Optional[float] = None
    disposable_medical_materials_claimed_sum: Optional[float] = None
    deductible_standard_amount_max: Optional[float] = None
    amount_above_deductible_self_paid_sum: Optional[float] = None
    individual_proportion_burden_sum: Optional[float] = None
    amount_above_coverage_limit_sum: Optional[float] = None
    basic_coordinated_fund_payment_sum: Optional[float] = None
    civil_servant_medical_subsidy_sum: Optional[float] = None
    urban_rural_assistance_subsidy_sum: Optional[float] = None
    basic_personal_account_payment_sum: Optional[float] = None
    non_account_payment_sum: Optional[float] = None
    current_approval_amount_sum: Optional[float] = None
    subsidy_approval_amount_sum: Optional[float] = None
    hospital_medical_assistance_application_sum: Optional[float] = None
    disability_veterans_subsidy_sum: Optional[float] = None
    civil_affairs_subsidy_sum: Optional[float] = None
    urban_rural_welfare_subsidy_sum: Optional[float] = None
    discharge_diagnosis_name_nn: Optional[str] = None
    discharge_diagnosis_length_max: Optional[int] = None  # 出院诊断LENTH_MAX
    proportion_of_medicine_in_total_amount: Optional[float] = None
    individual_payment_proportion_for_medicine: Optional[float] = None
    proportion_of_checkup_costs_in_total_amount: Optional[float] = None
    individual_payment_proportion_for_checkups: Optional[float] = None
    proportion_of_treatment_costs_in_total_amount: Optional[float] = None
    individual_payment_proportion_for_treatment: Optional[float] = None
    bz_military_civilian_assistance: Optional[bool] = None
    bz_rural_and_urban_welfare: Optional[bool] = None
    whether_to_register: Optional[bool] = None
    reserved_field: Optional[bool] = None

    class Config:
        orm_mode = True

