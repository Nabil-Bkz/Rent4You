from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Administrateur, ProprietaireAgence, SecretaireAgence, Garagiste, Locataire, AdminAgence


class UserSerializer(serializers.ModelSerializer):
    """User serializer for read operations"""
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'phone', 
                  'date_of_birth', 'role', 'role_display', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm', 'first_name', 
                  'last_name', 'phone', 'date_of_birth', 'role']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        # Create role-specific profile
        role = validated_data.get('role')
        if role == 'ADMIN':
            Administrateur.objects.create(user=user)
        elif role == 'OWNER':
            ProprietaireAgence.objects.create(user=user)
        elif role == 'SECRETARY':
            SecretaireAgence.objects.create(user=user)
        elif role == 'MECHANIC':
            Garagiste.objects.create(user=user)
        elif role == 'RENTER':
            Locataire.objects.create(user=user)
        elif role == 'AGENCY_ADMIN':
            AdminAgence.objects.create(user=user)
        
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """User update serializer"""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'date_of_birth']
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    """Password change serializer"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "Password fields didn't match."})
        return attrs


class AdministrateurSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Administrateur
        fields = ['id', 'user']


class ProprietaireAgenceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    agence_id = serializers.IntegerField(source='agence.id', read_only=True)
    agence_nom = serializers.CharField(source='agence.nom_agence', read_only=True)
    
    class Meta:
        model = ProprietaireAgence
        fields = ['id', 'user', 'agence_id', 'agence_nom']


class SecretaireAgenceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    agence_id = serializers.IntegerField(source='agence.id', read_only=True)
    agence_nom = serializers.CharField(source='agence.nom_agence', read_only=True)
    
    class Meta:
        model = SecretaireAgence
        fields = ['id', 'user', 'agence_id', 'agence_nom']


class GaragisteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    agence_id = serializers.IntegerField(source='agence.id', read_only=True)
    agence_nom = serializers.CharField(source='agence.nom_agence', read_only=True)
    
    class Meta:
        model = Garagiste
        fields = ['id', 'user', 'agence_id', 'agence_nom']


class LocataireSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_banned = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Locataire
        fields = ['id', 'user', 'is_banned']


class AdminAgenceSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    agence_id = serializers.IntegerField(source='agence.id', read_only=True)
    agence_nom = serializers.CharField(source='agence.nom_agence', read_only=True)
    
    class Meta:
        model = AdminAgence
        fields = ['id', 'user', 'agence_id', 'agence_nom']

