from sqladmin import ModelView
from ..models import Cat


class CatAdmin(ModelView, model=Cat):
    column_list = [Cat.id, Cat.name, Cat.litter_code, Cat.gender, Cat.date_of_birth,
                   Cat.is_available, Cat.created_at]  # What to show in the list
    column_details_list = [Cat.id, Cat.name, Cat.litter_code, Cat.gender, Cat.date_of_birth, Cat.description,
                           # What to show when viewing one kitten
                           Cat.photo_base64, Cat.is_available, Cat.created_at, Cat.updated_at]
    can_create = True  # Can add new kittens
    can_edit = True    # Can change kitten info
    can_delete = True  # Can remove kittens
    name = "Kitten"       # What to call one kitten
    name_plural = "Kittens"  # What to call many kittens
