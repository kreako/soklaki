from peewee import *

database = PostgresqlDatabase('postgres', **{'host': 'localhost', 'user': 'postgres', 'password': 'password'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Group(BaseModel):
    id = BigAutoField()
    is_school = BooleanField()
    name = TextField()
    payment_ok = BooleanField()

    class Meta:
        table_name = 'group'

class Student(BaseModel):
    active = BooleanField(constraints=[SQL("DEFAULT true")])
    birthdate = DateField()
    cycle = TextField()  # USER-DEFINED
    firstname = TextField()
    group = ForeignKeyField(column_name='group_id', field='id', model=Group)
    id = BigAutoField()
    lastname = TextField()
    school_entry = DateField(null=True)

    class Meta:
        table_name = 'student'

class User(BaseModel):
    active = BooleanField()
    email = TextField(unique=True)
    email_confirmed = BooleanField()
    group = ForeignKeyField(column_name='group_id', field='id', model=Group)
    hash = TextField()
    id = BigAutoField()
    manager = BooleanField()
    name = TextField()

    class Meta:
        table_name = 'user'

class EvalComment(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    id = BigAutoField()
    student = ForeignKeyField(column_name='student_id', field='id', model=Student)
    text = TextField()
    updated_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    user = ForeignKeyField(column_name='user_id', field='id', model=User)

    class Meta:
        table_name = 'eval_comment'

class SocleDomain(BaseModel):
    rank = IntegerField()
    title = TextField()

    class Meta:
        table_name = 'socle_domain'

class SocleComponent(BaseModel):
    domain = ForeignKeyField(column_name='domain_id', field='id', model=SocleDomain)
    rank = IntegerField()
    title = TextField()

    class Meta:
        table_name = 'socle_component'

class SocleCompetency(BaseModel):
    component = ForeignKeyField(column_name='component_id', field='id', model=SocleComponent)
    cycle = TextField()  # USER-DEFINED
    rank = IntegerField()
    text = TextField()

    class Meta:
        table_name = 'socle_competency'

class EvalEvaluation(BaseModel):
    comment = TextField()
    competency = ForeignKeyField(column_name='competency_id', field='id', model=SocleCompetency)
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    id = BigAutoField()
    status = UnknownField()  # USER-DEFINED
    student = ForeignKeyField(column_name='student_id', field='id', model=Student)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    user = ForeignKeyField(column_name='user_id', field='id', model=User)

    class Meta:
        table_name = 'eval_evaluation'

class EvalObservation(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    id = BigAutoField()
    text = TextField()
    updated_at = DateTimeField(constraints=[SQL("DEFAULT now()")])

    class Meta:
        table_name = 'eval_observation'

class EvalObservationCompetency(BaseModel):
    competency = ForeignKeyField(column_name='competency_id', field='id', model=SocleCompetency)
    id = BigAutoField()
    observation = ForeignKeyField(column_name='observation_id', field='id', model=EvalObservation)

    class Meta:
        table_name = 'eval_observation_competency'

class EvalObservationStudent(BaseModel):
    id = BigAutoField()
    observation = ForeignKeyField(column_name='observation_id', field='id', model=EvalObservation)
    student = ForeignKeyField(column_name='student_id', field='id', model=Student)

    class Meta:
        table_name = 'eval_observation_student'

class EvalObservationTemplate(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    text = TextField()
    updated_at = DateTimeField(constraints=[SQL("DEFAULT now()")])

    class Meta:
        table_name = 'eval_observation_template'

class EvalObservationTemplateCompetency(BaseModel):
    competency = ForeignKeyField(column_name='competency_id', field='id', model=SocleCompetency)
    template = ForeignKeyField(column_name='template_id', field='id', model=EvalObservationTemplate)

    class Meta:
        table_name = 'eval_observation_template_competency'

class PricingPlan(BaseModel):
    id = TextField(primary_key=True)

    class Meta:
        table_name = 'pricing_plan'

class GroupPricing(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    end = DateField()
    group = ForeignKeyField(column_name='group_id', field='id', model=Group)
    plan = ForeignKeyField(column_name='plan', field='id', model=PricingPlan)
    price_cent = IntegerField()
    start = DateField()

    class Meta:
        table_name = 'group_pricing'

class PricingDetail(BaseModel):
    plan = ForeignKeyField(column_name='plan', field='id', model=PricingPlan, unique=True)
    price_cent = IntegerField()

    class Meta:
        table_name = 'pricing_detail'

class Report(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    cycle = UnknownField()  # USER-DEFINED
    end = DateField()
    json_path = TextField()
    pdf_path = TextField()
    start = DateField()
    student = ForeignKeyField(column_name='student_id', field='id', model=Student)

    class Meta:
        table_name = 'report'

class SocleSubject(BaseModel):
    title = TextField()

    class Meta:
        table_name = 'socle_subject'

class SocleCompetencySubject(BaseModel):
    competency = ForeignKeyField(column_name='competency_id', field='id', model=SocleCompetency)
    subject = ForeignKeyField(column_name='subject_id', field='id', model=SocleSubject)

    class Meta:
        table_name = 'socle_competency_subject'
        indexes = (
            (('competency', 'subject'), True),
        )

class UserLogin(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    id = BigAutoField()
    user = ForeignKeyField(column_name='user_id', field='id', model=User)

    class Meta:
        table_name = 'user_login'

class UserNavigation(BaseModel):
    created_at = DateTimeField(constraints=[SQL("DEFAULT now()")])
    id = BigAutoField()
    path = TextField()
    user = ForeignKeyField(column_name='user_id', field='id', model=User)

    class Meta:
        table_name = 'user_navigation'
