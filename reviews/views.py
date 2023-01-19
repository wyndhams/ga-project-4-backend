from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError
from .serializers.common import ReviewSerializer
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .models import Review


class ReviewListView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        # request.data['owner'] = request.user.id
        review_to_create = ReviewSerializer(data=request.data)
        try:
            review_to_create.is_valid()
            review_to_create.save()
            return Response(review_to_create.data, status=status.HTTP_201_CREATED)
        # below is the exception thrown when we miss a required field
        except IntegrityError as e:
            return Response({
                "detail": str(e),
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # AssertionError occurs when the incorrect type is passed as a value for an existing field
        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        # catch all exception
        except:
            return Response("Unprocessable Entity", status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class ReviewDetailView(APIView):
    permission_classes = (IsAuthenticated, )

    def get_review(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise NotFound(detail="Can't find that album!")

    def put(self, request, pk):
        review_to_edit = self.get_review(pk=pk)
        # if review_to_edit.owner != request.user:
            # raise PermissionDenied()

        updated_review = ReviewSerializer(review_to_edit, data=request.data)
        try:
            updated_review.is_valid()
            updated_review.save()
            return Response(updated_review.data, status=status.HTTP_202_ACCEPTED)

        except AssertionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        except:
            return Response({"detail": "Unprocessable Entity"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk):
        try:
            review_to_delete = self.get_review(pk=pk)
            # if review_to_delete.owner != request.user:
                # raise PermissionDenied()

            review_to_delete.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except review.DoesNotExist:
            raise NotFound(detail="Review not found")