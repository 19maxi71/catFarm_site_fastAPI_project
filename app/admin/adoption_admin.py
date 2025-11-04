from sqladmin import ModelView
from ..models import AdoptionQuestion, AdoptionRequest


class AdoptionQuestionAdmin(ModelView, model=AdoptionQuestion):
    column_list = [AdoptionQuestion.id, AdoptionQuestion.question_text, AdoptionQuestion.question_type,
                   AdoptionQuestion.is_required, AdoptionQuestion.order]
    column_details_list = [AdoptionQuestion.id, AdoptionQuestion.question_text, AdoptionQuestion.question_type,
                           AdoptionQuestion.options, AdoptionQuestion.is_required, AdoptionQuestion.order]
    can_create = True
    can_edit = True
    can_delete = True
    name = "Adoption Question"
    name_plural = "Adoption Questions"
    form_columns = [AdoptionQuestion.question_text, AdoptionQuestion.question_type,
                    AdoptionQuestion.options, AdoptionQuestion.is_required, AdoptionQuestion.order]


class AdoptionRequestAdmin(ModelView, model=AdoptionRequest):
    column_list = [AdoptionRequest.id, AdoptionRequest.customer_name, AdoptionRequest.customer_email,
                   AdoptionRequest.submitted_at, AdoptionRequest.status]
    column_details_list = [AdoptionRequest.id, AdoptionRequest.customer_name, AdoptionRequest.customer_email,
                           AdoptionRequest.phone, AdoptionRequest.custom_answers, AdoptionRequest.terms_agreed,
                           AdoptionRequest.subscription, AdoptionRequest.submitted_at, AdoptionRequest.status,
                           AdoptionRequest.notification_sent_at]
    can_create = False  # Only created via form submission
    can_edit = True     # Can update status
    can_delete = True
    name = "Adoption Request"
    name_plural = "Adoption Requests"
    form_columns = [AdoptionRequest.status, AdoptionRequest.notification_sent_at]  # Only allow status updates
