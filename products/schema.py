import graphene
from graphene_django.types import DjangoObjectType
from decimal import Decimal
from .models import Product
import graphene
from decimal import Decimal

import graphene
from graphene_django.types import DjangoObjectType
from decimal import Decimal
from .models import Product

# Utiliser un type Decimal pour le prix
class ProductType(DjangoObjectType):
    class Meta:
        model = Product



class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)  # Utilisation de graphene.Decimal
        image = graphene.String(required=True)

    product = graphene.Field(ProductType)
    success_message = graphene.String()

    def mutate(self, info, name, price, image):
        product = Product.objects.create(name=name, price=price, image=image)
        success_message = "Produit ajouté avec succès!"
        return CreateProduct(product=product, success_message=success_message)

class UpdateProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()
        price = graphene.Decimal()  # Utilisation de graphene.Decimal
        image = graphene.String()

    product = graphene.Field(ProductType)
    success_message = graphene.String()

    def mutate(self, info, id, name=None, price=None, image=None):
        try:
            # Récupérer le produit par ID
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return UpdateProduct(success_message="Produit non trouvé")

        # Mettre à jour les champs uniquement si une nouvelle valeur est fournie
        if name is not None:
            product.name = name
        if price is not None:
            product.price = price
        if image is not None:
            product.image = image

        # Sauvegarder les modifications
        try:
            product.save()
        except Exception as e:
            print(f"Error saving product: {e}")
            return UpdateProduct(success_message="Erreur lors de la mise à jour du produit")

        return UpdateProduct(
            product=product, 
            success_message="Produit mis à jour avec succès!"
        )


class DeleteProduct(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success_message = graphene.String()

    def mutate(self, info, id):
        product = Product.objects.get(id=id)
        product.delete()
        return DeleteProduct(success_message="Produit supprimé avec succès!")

class Query(graphene.ObjectType):
    all_products = graphene.List(ProductType)
    product = graphene.Field(ProductType, id=graphene.Int())

    def resolve_all_products(self, info):
        return Product.objects.all()

    def resolve_product(self, info, id):
        return Product.objects.get(id=id)

class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()
    update_product = UpdateProduct.Field()
    delete_product = DeleteProduct.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
