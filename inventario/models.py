from django.db import models
from decimal import Decimal
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework import status
# Create your models here.

class ConversionCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Ejemplo: "longitud", "peso"
    description = models.TextField(blank=True, null=True)  # Descripción opcional

    def __str__(self):
        return self.name

class Unit(models.Model):
    category = models.ForeignKey(ConversionCategory, on_delete=models.CASCADE, related_name="units")
    name = models.CharField(max_length=50, unique=True)  # Ejemplo: "metros", "kilogramos"
    symbol = models.CharField(max_length=10, unique=True)  # Ejemplo: "m", "kg"
    conversion_factor = models.FloatField()  # Factor respecto a una unidad base (como metros o kilogramos)

    def __str__(self):
        return f"{self.name} ({self.symbol})"
    

    def convert_to(self, target_unit, value, decimal_places=2):
        """
        Convierte un valor de esta unidad a otra unidad de la misma categoría.
        
        Args:
            target_unit (Unit): Unidad de destino.
            value (float): Valor a convertir.
            decimal_places (int): Número de decimales para redondear el resultado.
        
        Returns:
            float: Valor convertido.
        """
        if self.category != target_unit.category:
            raise ValueError("Las unidades deben pertenecer a la misma categoría.")

        if target_unit.conversion_factor == 0:
            raise ValueError("El factor de conversión de la unidad destino no puede ser cero.")

        base_value = Decimal(value) * Decimal(self.conversion_factor)
        #converted_value = base_value / Decimal(target_unit.conversion_factor)

        # Redondear el resultado si se especifica
        if decimal_places is not None:
            converted_value = round(base_value, decimal_places)

        return converted_value
    
    def reverse_to(self, target_unit, value, decimal_places=2):
        """
        Convierte un valor de esta unidad a otra unidad de la misma categoría.
        
        Args:
            target_unit (Unit): Unidad de destino.
            value (float): Valor a convertir.
            decimal_places (int): Número de decimales para redondear el resultado.
        
        Returns:
            float: Valor convertido.
        """
        if self.category != target_unit.category:
            raise ValueError("Las unidades deben pertenecer a la misma categoría.")

        if target_unit.conversion_factor == 0:
            raise ValueError("El factor de conversión de la unidad destino no puede ser cero.")

        base_value = Decimal(value) / Decimal(self.conversion_factor)
        #converted_value = base_value / Decimal(target_unit.conversion_factor)

        # Redondear el resultado si se especifica
        if decimal_places is not None:
            converted_value = round(base_value, decimal_places)

        return converted_value
    
class ProductVariant(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    account = models.ForeignKey('cuenta.Cliente', on_delete=models.CASCADE, related_name="products", default=None)
    brand = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    def remove_stock(self, quantity: Decimal, stock_id: int, unit_id: int):
        """
        Resta stock del producto, priorizando unidades ya fraccionadas.
        
        Args:
            quantity (Decimal): Cantidad a restar.
            unit (Unit): Unidad de medida asociada a la cantidad.
        
        Returns:
            bool: True si se pudo restar el stock, False en caso contrario.
        """
       
        productunit = self.units.filter(id=unit_id).first()
        stock_array = []
        
        unit_conversion = productunit.unit.convert_to(productunit.unit, float(quantity) * productunit.quantity)
        unit_remaining = float(unit_conversion) 
                 
        if(productunit.is_main):
            
            stocks = self.stock_units.filter(is_cut=False)
            
            for stock in stocks:

                stock_conversion = 0
                
                if stock.remaining_quantity == stock.original_quantity:
                    
                    stock_conversion = productunit.unit.convert_to(productunit.unit, stock.remaining_quantity)
                    unit_remaining -= float(stock_conversion) 
                    stock.remaining_quantity = 0
                    stock.is_cut = True
                    stock_array.append(stock)
              
                if unit_remaining is not None and unit_remaining <= 0:
                    break
                         
        else:
            if (stock_id is not None):
                stock = self.stock_units.filter(id=stock_id).first()
            else:
                return Response({"message": "No se ha especificado un stock: stock_id"}, status=status.HTTP_400_BAD_REQUEST)

            stock_conversion = stock.product.units.filter(is_main=True).first().unit.convert_to(stock.product.units.filter(is_main=True).first().unit, stock.remaining_quantity)
            unit_remaining =   float(unit_conversion) - float(stock_conversion) 
            new_quantity = float(stock_conversion) - float(unit_conversion)
            
            stock.remaining_quantity = stock.product.units.filter(is_main=True).first().unit.reverse_to(stock.product.units.filter(is_main=True).first().unit, new_quantity)
            stock.is_cut = True
            
            stock_array.append(stock)

        if unit_remaining is not None and  unit_remaining <= 0:
            for stock in stock_array:
                stock.save()
        else:
            return Response({"message": "No hay stock suficiente"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "Operación realizada con éxito."}, status=status.HTTP_200_OK)
     
    @property
    def total_stock(self):
        """
        Calcula el stock total sumando las cantidades restantes de todas las unidades.
        """
        main_unit = self.units.filter(is_main=True).first()
        if main_unit:
            # Convertir la cantidad principal a la unidad principal
            main_unit_quantity = main_unit.unit.convert_to(main_unit.unit, main_unit.quantity)
            # Sumar todas las cantidades restantes de las unidades de stock
            total_remaining_quantity = self.stock_units.aggregate(total=Sum('remaining_quantity'))['total']
            if total_remaining_quantity is not None:
                return float(main_unit_quantity) * float(total_remaining_quantity)
            else:
                return 0
        else:
            # Si no hay unidad principal, devolver la suma de las cantidades restantes
            total_remaining_quantity = self.stock_units.aggregate(total=Sum('remaining_quantity'))['total']
            return total_remaining_quantity if total_remaining_quantity is not None else 0

class ProductUnit(models.Model):
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="units")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity = models.FloatField()
    public_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    supplier_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_main = models.BooleanField(default=False)
    more_details = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.quantity} {self.unit.symbol} de {self.product.name} "

    def save(self, *args, **kwargs):
        if self.quantity < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        
        # Validar que no haya más de una unidad principal por producto
        if self.is_main:
            main_unit = self.product.units.filter(is_main=True).first()
            if main_unit and main_unit != self:
                raise ValueError("Ya hay una unidad principal para este producto.")
            
        super().save(*args, **kwargs)

class StockUnit(models.Model):
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="stock_units")
    original_quantity = models.DecimalField(max_digits=10, decimal_places=3)
    remaining_quantity = models.DecimalField(max_digits=10, decimal_places=3)
    is_cut = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.name} - {self.remaining_quantity}/{self.original_quantity}"

    def save(self, *args, **kwargs):
        """
        Valida que los campos sean coherentes antes de guardar.
        """
        if self.original_quantity < 0 or self.remaining_quantity < 0:
            raise ValueError("Las cantidades no pueden ser negativas.")

        if self.remaining_quantity > self.original_quantity:
            raise ValueError("La cantidad restante no puede ser mayor que la cantidad original.")

        super().save(*args, **kwargs)