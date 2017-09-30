from rest_framework import serializers
from .models import Specialist, Domain, Speciality, Post
		
class SpecialistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialist
        fields = '__all__' 


class DomainSerializer(serializers.ModelSerializer):

    class Meta:
        model = Domain
        fields = '__all__' 


class SpecialitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Speciality
        fields = '__all__' 


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__' 
