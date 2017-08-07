from import_export import resources
from .models import Profile



class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile
        exclude = ['user','id']
