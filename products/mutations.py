# product/mutations.py
import graphene
from graphene_django.types import DjangoObjectType
from .models import Product
from channels.layers import get_channel_layer

# Définir le type GraphQL pour le modèle Product
class ProductType(DjangoObjectType):
    class Meta:
        model = Product

# Mutation pour ajouter un produit
class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        image = graphene.String(required=True)

    product = graphene.Field(ProductType)
    success_message = graphene.String()

    def mutate(self, info, name, price, image):
        # Créer un nouveau produit
        product = Product.objects.create(name=name, price=price, image=image)
        success_message = "Produit ajouté avec succès!"
        
        # Envoyer une notification en temps réel via Soketi
        channel_layer = get_channel_layer()
        channel_layer.group_send(
            "product_notifications",
            {
                "type": "product_notification",
                "message": f"Un nouveau produit '{name}' a été ajouté!"
            }
        )

        return CreateProduct(product=product, success_message=success_message)
