from peewee import *

database = PostgresqlDatabase(
    "postgres", **{"host": "localhost", "user": "postgres", "password": "password"}
)


class BaseModel(Model):
    class Meta:
        database = database


class DefaultSocleContainer(BaseModel):
    alpha_full_rank = TextField()
    container = ForeignKeyField(
        column_name="container_id", field="id", model="self", null=True
    )
    cycle = TextField()  # USER-DEFINED
    full_rank = TextField()
    rank = IntegerField()
    text = TextField()

    class Meta:
        table_name = "default_socle_container"


class DefaultSocleCompetency(BaseModel):
    alpha_full_rank = TextField()
    container = ForeignKeyField(
        column_name="container_id", field="id", model=DefaultSocleContainer
    )
    cycle = TextField()  # USER-DEFINED
    full_rank = TextField()
    rank = IntegerField()
    text = TextField()

    class Meta:
        table_name = "default_socle_competency"


class DefaultSocleSubject(BaseModel):
    title = TextField()

    class Meta:
        table_name = "default_socle_subject"


class DefaultSocleCompetencySubject(BaseModel):
    competency = ForeignKeyField(
        column_name="competency_id", field="id", model=DefaultSocleCompetency
    )
    subject = ForeignKeyField(
        column_name="subject_id", field="id", model=DefaultSocleSubject
    )

    class Meta:
        table_name = "default_socle_competency_subject"


class DefaultSocleCompetencyTemplate(BaseModel):
    competency = ForeignKeyField(
        column_name="competency_id", field="id", model=DefaultSocleCompetency
    )
    text = TextField()

    class Meta:
        table_name = "default_socle_competency_template"


class Group(BaseModel):
    id = BigAutoField()
    is_school = BooleanField()
    name = TextField(null=True)
    payment_ok = BooleanField()

    class Meta:
        table_name = "group"


class EvalPeriod(BaseModel):
    active = BooleanField(constraints=[SQL("DEFAULT true")])
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    end = DateField()
    group = ForeignKeyField(column_name="group_id", field="id", model=Group)
    name = TextField()
    start = DateField()
    updated_at = DateTimeField(constraints=[SQL("DEFAULT now()")])

    class Meta:
        table_name = "eval_period"


class Student(BaseModel):
    active = BooleanField(constraints=[SQL("DEFAULT true")])
    birthdate = DateField()
    firstname = TextField()
    group = ForeignKeyField(column_name="group_id", field="id", model=Group)
    id = BigAutoField()
    lastname = TextField()
    school_entry = DateField()
    school_exit = DateField(null=True)

    class Meta:
        table_name = "student"


class User(BaseModel):
    active = BooleanField()
    email = TextField(unique=True)
    email_confirmed = BooleanField()
    firstname = TextField(null=True)
    group = ForeignKeyField(column_name="group_id", field="id", model=Group)
    hash = TextField()
    id = BigAutoField()
    lastname = TextField(null=True)
    manager = BooleanField()

    class Meta:
        table_name = "user"


class EvalComment(BaseModel):
    active = BooleanField(constraints=[SQL("DEFAULT true")])
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    date = DateField(constraints=[SQL("DEFAULT CURRENT_DATE")])
    eval_period = ForeignKeyField(
        column_name="eval_period_id", field="id", model=EvalPeriod
    )
    id = BigAutoField()
    student = ForeignKeyField(column_name="student_id", field="id", model=Student)
    text = TextField()
    updated_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    user = ForeignKeyField(column_name="user_id", field="id", model=User)

    class Meta:
        table_name = "eval_comment"


class SocleContainer(BaseModel):
    active = BooleanField(constraints=[SQL("DEFAULT true")])
    alpha_full_rank = TextField()
    container = ForeignKeyField(
        column_name="container_id", field="id", model="self", null=True
    )
    cycle = TextField()  # USER-DEFINED
    full_rank = TextField()
    group = ForeignKeyField(column_name="group_id", field="id", model=Group)
    rank = IntegerField()
    text = TextField()

    class Meta:
        table_name = "socle_container"


class SocleCompetency(BaseModel):
    active = BooleanField(constraints=[SQL("DEFAULT true")])
    alpha_full_rank = TextField()
    container = ForeignKeyField(
        column_name="container_id", field="id", model=SocleContainer
    )
    cycle = TextField()  # USER-DEFINED
    full_rank = TextField()
    group = ForeignKeyField(column_name="group_id", field="id", model=Group)
    rank = IntegerField()
    text = TextField()

    class Meta:
        table_name = "socle_competency"


class EvalEvaluation(BaseModel):
    active = BooleanField(constraints=[SQL("DEFAULT true")])
    comment = TextField(null=True)
    competency = ForeignKeyField(
        column_name="competency_id", field="id", model=SocleCompetency
    )
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    date = DateField(constraints=[SQL("DEFAULT CURRENT_DATE")])
    eval_period = ForeignKeyField(
        column_name="eval_period_id", field="id", model=EvalPeriod
    )
    id = BigAutoField()
    status = TextField()  # USER-DEFINED
    student = ForeignKeyField(column_name="student_id", field="id", model=Student)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    user = ForeignKeyField(column_name="user_id", field="id", model=User)

    class Meta:
        table_name = "eval_evaluation"


class EvalObservation(BaseModel):
    active = BooleanField(constraints=[SQL("DEFAULT true")])
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    date = DateField(constraints=[SQL("DEFAULT CURRENT_DATE")])
    eval_period = ForeignKeyField(
        column_name="eval_period_id", field="id", model=EvalPeriod
    )
    id = BigAutoField()
    text = TextField()
    updated_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    user = ForeignKeyField(column_name="user_id", field="id", model=User)

    class Meta:
        table_name = "eval_observation"


class EvalObservationCompetency(BaseModel):
    competency = ForeignKeyField(
        column_name="competency_id", field="id", model=SocleCompetency
    )
    id = BigAutoField()
    observation = ForeignKeyField(
        column_name="observation_id", field="id", model=EvalObservation
    )

    class Meta:
        table_name = "eval_observation_competency"
        indexes = ((("observation", "competency"), True),)


class EvalObservationStudent(BaseModel):
    id = BigAutoField()
    observation = ForeignKeyField(
        column_name="observation_id", field="id", model=EvalObservation
    )
    student = ForeignKeyField(column_name="student_id", field="id", model=Student)

    class Meta:
        table_name = "eval_observation_student"
        indexes = ((("observation", "student"), True),)


class FrontendStoreError(BaseModel):
    action = TextField(null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    error = TextField(null=True)
    response = TextField(null=True)
    user = ForeignKeyField(column_name="user_id", field="id", model=User)

    class Meta:
        table_name = "frontend_store_error"


class PricingPlan(BaseModel):
    id = TextField(primary_key=True)

    class Meta:
        table_name = "pricing_plan"


class GroupPricing(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    end = DateField()
    group = ForeignKeyField(column_name="group_id", field="id", model=Group)
    plan = ForeignKeyField(column_name="plan", field="id", model=PricingPlan)
    price_cent = IntegerField()
    start = DateField()

    class Meta:
        table_name = "group_pricing"


class PricingDetail(BaseModel):
    plan = ForeignKeyField(
        column_name="plan", field="id", model=PricingPlan, unique=True
    )
    price_cent = IntegerField()

    class Meta:
        table_name = "pricing_detail"


class Report(BaseModel):
    active = BooleanField(constraints=[SQL("DEFAULT true")])
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    cycle = TextField()  # USER-DEFINED
    date = DateField(constraints=[SQL("DEFAULT now()")])
    eval_period = ForeignKeyField(
        column_name="eval_period_id", field="id", model=EvalPeriod
    )
    json_path = TextField()
    pdf_path = TextField()
    student = ForeignKeyField(column_name="student_id", field="id", model=Student)

    class Meta:
        table_name = "report"


class SocleSubject(BaseModel):
    active = BooleanField(constraints=[SQL("DEFAULT true")])
    group = ForeignKeyField(column_name="group_id", field="id", model=Group)
    title = TextField()

    class Meta:
        table_name = "socle_subject"


class SocleCompetencySubject(BaseModel):
    active = BooleanField(constraints=[SQL("DEFAULT true")])
    competency = ForeignKeyField(
        column_name="competency_id", field="id", model=SocleCompetency
    )
    subject = ForeignKeyField(column_name="subject_id", field="id", model=SocleSubject)

    class Meta:
        table_name = "socle_competency_subject"
        indexes = ((("competency", "subject"), True),)


class SocleCompetencyTemplate(BaseModel):
    active = BooleanField()
    competency = ForeignKeyField(
        column_name="competency_id", field="id", model=SocleCompetency
    )
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    group = ForeignKeyField(column_name="group_id", field="id", model=Group)
    text = TextField()
    updated_at = DateTimeField(constraints=[SQL("DEFAULT now()")])

    class Meta:
        table_name = "socle_competency_template"


class UserLogin(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    id = BigAutoField()
    user = ForeignKeyField(column_name="user_id", field="id", model=User)

    class Meta:
        table_name = "user_login"


class UserNavigation(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    id = BigAutoField()
    path = TextField()
    user = ForeignKeyField(column_name="user_id", field="id", model=User)

    class Meta:
        table_name = "user_navigation"
