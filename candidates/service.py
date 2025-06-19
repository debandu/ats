from abc import ABC, abstractmethod

class BaseService(ABC):
    """
    Abstract base class interface for model services.
    Requires concrete subclasses to define:
    - model (as a @property)
    - serializer_class (as a @property)
    - __init__, update, delete
    """

    @property
    @abstractmethod
    def model(self):
        """Must return a Django model class."""
        pass

    @property
    @abstractmethod
    def serializer_class(self):
        """Must return a DRF serializer class."""
        pass

    @abstractmethod
    def __init__(self, id=None, data=None):
        """Initialize the service with an instance loaded from id or created from data."""
        pass

    @abstractmethod
    def update(self, data, partial=False):
        """Update the instance with new data."""
        pass

    @abstractmethod
    def delete(self):
        """Delete the instance."""
        pass


# implementation of the CandidateService using the BaseService interface

from rest_framework.exceptions import NotFound
from django.db.models import Q, F, Value, Case, When, IntegerField
from .models import Candidate
from .serializers import CandidateSerializer

class CandidateService(BaseService):
    @property
    def model(self):
        return Candidate

    @property
    def serializer_class(self):
        return CandidateSerializer

    def __init__(self, id=None, data=None):
        if id is None and data is None:
            raise ValueError("Either 'id' or 'data' must be provided.")

        if id is not None:
            self.instance = self.model.objects.filter(id=id).first()
            if not self.instance:
                raise NotFound(f"{self.model.__name__} with ID {id} not found.")
        else:
            self.instance = self._create_from_data(data)

    def _create_from_data(self, data):
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def update(self, data, partial=False):
        serializer = self.serializer_class(instance=self.instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def delete(self):
        self.instance.delete()
        return True

    @staticmethod
    def search_candidates(query, queryset, name_field="name"):
        if not query:
            return queryset.none()

        words = query.lower().split()
        filters = Q()
        for word in words:
            filters |= Q(**{f"{name_field}__icontains": word})

        annotations = {
            f"match_{word}": Case(
                When(**{f"{name_field}__icontains": word}, then=Value(1)),
                default=Value(0),
                output_field=IntegerField()
            )
            for word in words
        }

        queryset = queryset.annotate(**annotations).filter(filters)

        total_score = None
        for word in words:
            if total_score is None:
                total_score = F(f"match_{word}")
            else:
                total_score += F(f"match_{word}")

        return queryset.annotate(relevancy=total_score).order_by("-relevancy", name_field)
