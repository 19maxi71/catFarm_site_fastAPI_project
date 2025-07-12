from sqladmin import ModelView
from ..models import Cat


class CatAdmin(ModelView, model=Cat):
    column_list = [Cat.id, Cat.name, Cat.role, Cat.breed, Cat.rabies_vaccinated, Cat.created_at]  # What to show in the list
    column_details_list = [Cat.id, Cat.name, Cat.role, Cat.breed, Cat.bio, Cat.photo_url, Cat.rabies_vaccinated, Cat.award, Cat.created_at, Cat.updated_at] # What to show when viewing one cat
    can_create = True  # Can add new cats
    can_edit = True    # Can change cat info
    can_delete = True  # Can remove cats
    name = "Cat"       # What to call one cat
    name_plural = "Cats"  # What to call many cats
