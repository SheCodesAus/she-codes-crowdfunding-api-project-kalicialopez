# from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Project, Pledge, Comment
from users.models import CustomUser
from users.serializers import CustomUserSerializer

User = get_user_model()


''' Pledge Serializer '''


class PledgeSerializer(serializers.ModelSerializer):
    
    # For serializer method field
    supporter = serializers.SerializerMethodField()
    supporter_profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Pledge
        fields = ['id', 'pledge_amount', 'comment',
                  'anonymous', 'project', 'supporter', 'supporter_profile_picture']
        read_only_fields = ['id', 'supporter']

    def get_supporter(self, obj):
        if obj.anonymous:  # i.e. if anonymous = true
            return None
        else:
            return obj.supporter.username

    def get_supporter_profile_picture(self, obj):
        return obj.supporter.profile_picture
    
    def create(self, validated_data):
        return Pledge.objects.create(**validated_data)


class PledgeDetailSerializer(PledgeSerializer):
# is pledgedetailserializer(pledgeserializer) the same as declaring a serializer class field?

    class Meta:
        model = Pledge
        fields = [
            "id",
            "pledge_amount",
            "comment",
            "anonymous",
            "project",
            "supporter",
            "supporter_profile_picture",
            "pledge_date"
            ]
        read_only_fields = [
            "id", 
             "supporter", 
             "pledge_amount", 
             "project"
             ]


''' Project Serializer '''


class ProjectSerializer(serializers.ModelSerializer):
    
    owner = serializers.ReadOnlyField(source="owner_id")
    owner = serializers.SerializerMethodField()
    total = serializers.ReadOnlyField()
    goal_balance = serializers.ReadOnlyField()
    funding_status = serializers.ReadOnlyField()
    owner_profile_picture = serializers.SerializerMethodField()

    # This is not working, no likes are displayed. 
    liked_by = serializers.ReadOnlyField(source="liked_projects")
    
    class Meta:

        # total = serializers.DecimalField(decimal_places = 2, max_digits = 9)

        model = Project
        fields = [
            'id', 
            'title', 
            'description', 
            'goal', 
            'image', 
            'course_name', 
            'educational_institution', 
            'current_occupation_or_industry',
            'desired_occupation_or_industry', 
            'is_open', 
            'date_created', 
            'campaign_deadline', 
            'owner', 
            'total',
            'goal_balance',
            'funding_status', 
            'liked_by', 
            'pledges',
            'total',
            'goal_balance',
            'funding_status',
            'owner_profile_picture'
            ]
        read_only_fields = [
            'id', 
            'owner', 
            'date_created',
            'total',
            'goal_balance'
            'funding_status', 
            'liked_by', 
            'pledges'
            ]
    
    def get_owner(self, obj):
        return obj.owner.username

    def get_owner_profile_picture(self, obj):
        return obj.owner.profile_picture

# Unsure if this should be here
    def create(self, validated_data):
        return Project.objects.create(**validated_data)


''' Comment Serializer '''


class CommentSerializer(serializers.ModelSerializer):
    commentator = serializers.ReadOnlyField(source='commentator.username')
    commentator_profile_picture = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 
            'project',
            'created',
            'content', 
            'commentator',
            'commentator_profile_picture',
            ]
        read_only_fields = [
            'id',
            'project',
            'commentator'
            ]

    def get_commentator_profile_picture(self, obj):
        return obj.commentator.profile_picture


# Not sure if this should be here?
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.save()
        return instance


# ''' Comment Detail Serializer ''' 

#  Update - don't need a whole other comment detail serializer, just need to refer to these objects before setting out Meta class in the project detail serializer, as that is where they will appear.
#  Unsure if this is required - currently unable to edit comments?
# class CommentDetailSerializer(CommentSerializer):
#     Comment = CommentSerializer(many=True, read_only=True)
#     liked_by = CustomUserSerializer(many=True, read_only=True)


''' Project Detail Serializer '''

# Need to put ProjectDetailSerializer below the CommentSerializer because we make reference the CommentSerializer below
class ProjectDetailSerializer(ProjectSerializer):
    pledges = PledgeSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    liked_by = CustomUserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "goal",
            "image",
            "is_open",
            "date_created",
            "campaign_deadline",
            "owner",
            "owner_profile_picture",
            "total",
            "goal_balance",
            "funding_status",
            "pledges",
            "comments",
        ]
        read_only_fields = [
            "id", 
            "owner",
            'date_created', 
            "total", 
            "goal_balance", 
            "funding_status",
            "liked_by",
            "pledges"
            ]


''' Global Search Serializer '''

# Ben's solution for Global Serializer using generic relations object related fields.
# https://stackoverflow.com/questions/38721923/serializing-a-generic-relation-in-django-rest-framework/39125641#39125641


class MultiObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        if isinstance(value, Project):
            serializer = ProjectSerializer(value)
        elif isinstance(value, User):
            serializer = CustomUserSerializer(value)
        else:
            raise TypeError("Unexpected type of tagged object")
        return serializer.data


class MultiObjectHyperlinkedField(serializers.HyperlinkedRelatedField):
    view_name = ""

    def to_representation(self, value):
        """convert the model item into a hyperlink related field"""
        # This stuff is here to replicate the process that happens in the parent class
        request = self.context["request"]
        format = self.context.get("format")
        if format and self.format and self.format != format:
            format = self.format
        # this is where the actual work happens.
        if isinstance(value, Project):
            field = self.get_url(value, "project-detail",
                                 request=request, format=format)
        elif isinstance(value, User):
            field = self.get_url(value, "customuser-detail",
                                 request=request, format=format)
        else:
            raise TypeError("Unexpected type of tagged object")
        return field


class GlobalSearchSerializer(serializers.Serializer):
    type = serializers.CharField(read_only=True)
    link = MultiObjectHyperlinkedField(read_only=True, source="item")
    item = MultiObjectRelatedField(read_only=True)

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError


# # Original code modified from https://www.yeti.co/blog/global-search-in-django-rest-framework which did not work
# class GlobalSearchSerializer(serializers.ModelSerializer):
#     class Meta:

#         model = CustomUser
#         fields = ['first_name', 'last_name', 'bio', 'country_of_residence', 'highest_level_of_education']

#     def to_internal_value(self, obj):
#         if isinstance(obj, Project):
#             serializer = ProjectSerializer(obj)
#         elif isinstance(obj, CustomUser):
#             serializer = CustomUserSerializer(obj)
#         else:
#             raise Exception("Neither a project nor user instance!")
#         return serializer.data
