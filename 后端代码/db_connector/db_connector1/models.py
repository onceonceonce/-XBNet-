from sqlalchemy import Time, Boolean, Date, BigInteger, ForeignKey, Index
from sqlalchemy import Column, DateTime, func
from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from sqlalchemy.orm import declarative_base  # 新版使用

Base = declarative_base()

class MedicalRecord(Base):
    """
    存储16000条数据
    """

    __tablename__ = 'medical_records1'
    personal_id = Column(String(20), primary_key=True, comment='个人ID')
    individual_code = Column(String(30),comment="个人编码")
    days_visiting_two_hospitals = Column(Integer, comment='一天去两家医院的天数')
    months_of_visits = Column(Integer, comment='就诊的月数')
    max_days_visited_per_month = Column(Integer, comment='月就诊天数_MAX')
    avg_days_visited_per_month = Column(Float, comment='月就诊天数_AVG')
    max_hospitals_visited_per_month = Column(Integer, comment='月就诊医院数_MAX')
    avg_hospitals_visited_per_month = Column(Float, comment='月就诊医院数_AVG')
    total_visits_count = Column(Integer, comment='就诊次数_SUM')
    max_visits_per_month = Column(Integer, comment='月就诊次数_MAX')
    avg_visits_per_month = Column(Float, comment='月就诊次数_AVG')
    max_total_amount_per_month = Column(Float, comment='月统筹金额_MAX')
    avg_total_amount_per_month = Column(Float, comment='月统筹金额_AVG')
    max_medicine_amount_per_month = Column(Float, comment='月药品金额_MAX')
    avg_medicine_amount_per_month = Column(Float, comment='月药品金额_AVG')
    hospital_max_days_visited = Column(Integer, comment='医院_就诊天数_MAX')
    hospital_avg_days_visited = Column(Float, comment='医院_就诊天数_AVG')
    hospital_max_coordinated_fund = Column(Float, comment='医院_统筹金_MAX')
    hospital_avg_coordinated_fund = Column(Float, comment='医院_统筹金_AVG')
    hospital_max_medicine = Column(Float, comment='医院_药品_MAX')
    hospital_avg_medicine = Column(Float, comment='医院_药品_AVG')
    hospital_code_nn = Column(String(30), comment='医院编码_NN')
    sequence_number_nn = Column(String(30), comment='顺序号_NN')
    transaction_time_dd_nn = Column(String(30), comment='交易时间DD_NN')
    transaction_time_yyyy_nn = Column(String(30), comment='交易时间YYYY_NN')
    transaction_time_yyyymm_nn = Column(String(30), comment='交易时间YYYYMM_NN')
    total_days_of_hospitalization_sum = Column(Integer, comment='住院天数_SUM')
    personal_account_balance_sum = Column(Float, comment='个人账户金额_SUM')
    coordinated_payment_sum = Column(Float, comment='统筹支付金额_SUM')
    all_sum = Column(Float, comment='ALL_SUM')
    available_account_reimbursement_sum = Column(Float, comment='可用账户报销金额_SUM')
    medicine_cost_sum = Column(Float, comment='药品费发生金额_SUM')
    self_paid_medicine_cost_sum = Column(Float, comment='药品费自费金额_SUM')
    claimed_medicine_cost_sum = Column(Float, comment='药品费申报金额_SUM')
    expensive_medicine_cost_sum = Column(Float, comment='贵重药品发生金额_SUM')
    tcm_drug_cost_sum = Column(Float, comment='中成药费发生金额_SUM')
    herbal_medicine_cost_sum = Column(Float, comment='中草药费发生金额_SUM')
    examination_fee_sum = Column(Float, comment='检查费发生金额_SUM')
    self_paid_examination_fee_sum = Column(Float, comment='检查费自费金额_SUM')
    claimed_examination_fee_sum = Column(Float, comment='检查费申报金额_SUM')
    expensive_examination_fee = Column(Float, comment='贵重检查费金额_SUM')
    treatment_fee_sum = Column(Float, comment='治疗费发生金额_SUM')
    self_paid_treatment_fee_sum = Column(Float, comment='治疗费自费金额_SUM')
    claimed_treatment_fee_sum = Column(Float, comment='治疗费申报金额_SUM')
    surgery_fee_sum = Column(Float, comment='手术费发生金额_SUM')
    self_paid_surgery_fee_sum = Column(Float, comment='手术费自费金额_SUM')
    claimed_surgery_fee_sum = Column(Float, comment='手术费申报金额_SUM')
    bed_fee_sum = Column(Float, comment='床位费发生金额_SUM')
    bed_fee_claimed_sum = Column(Float, comment='床位费申报金额_SUM')
    medical_materials_cost_sum = Column(Float, comment='医用材料发生金额_SUM')
    high_cost_medical_materials_sum = Column(Float, comment='高价材料发生金额_SUM')
    self_paid_medical_materials_fee_sum = Column(Float, comment='医用材料费自费金额_SUM')
    component_transfusion_claimed_sum = Column(Float, comment='成分输血申报金额_SUM')
    other_costs_sum = Column(Float, comment='其它发生金额_SUM')
    other_claimed_costs_sum = Column(Float, comment='其它申报金额_SUM')
    disposable_medical_materials_claimed_sum = Column(Float, comment='一次性医用材料申报金额_SUM')
    deductible_standard_amount_max = Column(Float, comment='起付线标准金额_MAX')
    amount_above_deductible_self_paid_sum = Column(Float, comment='起付标准以上自负比例金额_SUM')
    individual_proportion_burden_sum = Column(Float, comment='医疗救助个人按比例负担金额_SUM')
    amount_above_coverage_limit_sum = Column(Float, comment='最高限额以上金额_SUM')
    basic_coordinated_fund_payment_sum = Column(Float, comment='基本统筹基金支付金额_SUM')
    civil_servant_medical_subsidy_sum = Column(Float, comment='公务员医疗补助基金支付金额_SUM')
    urban_rural_assistance_subsidy_sum = Column(Float, comment='城乡救助补助金额_SUM')
    basic_personal_account_payment_sum = Column(Float, comment='基本个人账户支付_SUM')
    non_account_payment_sum = Column(Float, comment='非账户支付金额_SUM')
    current_approval_amount_sum = Column(Float, comment='本次审批金额_SUM')
    subsidy_approval_amount_sum = Column(Float, comment='补助审批金额_SUM')
    hospital_medical_assistance_application_sum = Column(Float, comment='医疗救助医院申请_SUM')
    disability_veterans_subsidy_sum = Column(Float, comment='残疾军人补助_SUM')
    civil_affairs_subsidy_sum = Column(Float, comment='民政救助补助_SUM')
    urban_rural_welfare_subsidy_sum = Column(Float, comment='城乡优抚补助_SUM')
    discharge_diagnosis_name_nn = Column(String(20), comment='出院诊断病种名称_NN')
    discharge_diagnosis_length_max = Column(Integer, comment='出院诊断LENTH_MAX')  #这个字段可能是统计每个病人出院诊断书写的详细程度，通过计算出院诊断文本的字符数或字数来得出的一个指标
    proportion_of_medicine_in_total_amount = Column(Float, comment='药品在总金额中的占比')
    individual_payment_proportion_for_medicine = Column(Float, comment='个人支付的药品占比')
    proportion_of_checkup_costs_in_total_amount = Column(Float, comment='检查总费用在总金额占比')
    individual_payment_proportion_for_checkups = Column(Float, comment='个人支付检查费用占比')
    proportion_of_treatment_costs_in_total_amount = Column(Float, comment='治疗费用在总金额占比')
    individual_payment_proportion_for_treatment = Column(Float, comment='个人支付治疗费用占比')
    bz_military_civilian_assistance = Column(Boolean, comment='BZ_民政救助')
    bz_rural_and_urban_welfare = Column(Boolean, comment='BZ_城乡优抚')
    whether_to_register = Column(Boolean, comment='是否挂号')
    reserved_field = Column(Boolean, comment='RES')

    class Config:
        orm_mode = True


class PatientInfo(Base):
    """
    每个患者具体信息
    """

    __tablename__ = 'patient_info'
    personal_id = Column(String(20),primary_key=True,comment="个人ID")
    fraud_prob = Column(Float,comment="一个人欺诈概率")
    not_fraud_prob = Column(Float,comment="一个人不欺诈概率")
    prob_res = Column(Boolean,comment="根据模型判断出来是否欺诈")
    fraud_types = Column(String(20),comment="可能的欺诈类型")

    class Config:
        orm_mode = True


