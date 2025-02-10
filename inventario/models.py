from django.db import models
from decimal import Decimal
from django.db.models import Sum

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
        converted_value = base_value / Decimal(target_unit.conversion_factor)

        # Redondear el resultado si se especifica
        if decimal_places is not None:
            converted_value = round(converted_value, decimal_places)

        return converted_value

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def total_stock(self):
        """
        Calcula el stock total sumando las cantidades restantes de todas las unidades.
        """
        return sum(unit.remaining_quantity for unit in self.stock_units.all())

    def add_stock(self, quantity, unit):
        """
        Agrega una nueva unidad al stock del producto.
        
        Args:
            quantity (Decimal): Cantidad a agregar.
            unit (Unit): Unidad de medida asociada a la cantidad.
        """
        if quantity <= 0:
            raise ValueError("La cantidad a agregar debe ser mayor que cero.")
        main_unit = self.units.filter(is_main=True).first()
        if main_unit:
            quantity = main_unit.unit.convert_to(unit, quantity)
        else:
            raise ValueError("No se puede agregar stock a un producto sin unidad principal.")
        
        # Crear una nueva unidad de stock
        StockUnit.objects.create(
            product=self,
            original_quantity=quantity,
            remaining_quantity=quantity,
            is_cut=False  # Por defecto, no está fraccionada
        )

        # Si es necesario, también puedes actualizar el stock total del producto
        # (aunque esto ya se maneja en la propiedad `total_stock`).

    def remove_stock(self, quantity: Decimal, stock_id: int, unit_id: int):
        """
        Resta stock del producto, priorizando unidades ya fraccionadas.
        
        Args:
            quantity (Decimal): Cantidad a restar.
            unit (Unit): Unidad de medida asociada a la cantidad.
        
        Returns:
            bool: True si se pudo restar el stock, False en caso contrario.
        """
        if quantity <= 0:
            raise ValueError("La cantidad a restar debe ser mayor que cero.")

        if stock_id is not None:
            stock_units = self.stock_units.filter(id=stock_id)
        else:
            # Obtener las unidades de stock disponibles, ordenadas por si están fraccionadas o no
            stock_units = self.stock_units.filter(remaining_quantity__gt=0).order_by('is_cut')
        
        for stock_unit in stock_units:
            
            if unit_id is not None:
                productunit = self.units.filter(unit_id=unit_id).first()
                if productunit is None:
                    raise ValueError("La unidad especificada no está asociada a este producto.")
                unit_conversion = productunit.unit.convert_to(productunit.unit, quantity)
            else:
                productunit = self.units.filter(is_main = True).first()
                unit_conversion = productunit.unit.convert_to(productunit.unit, quantity)

            if unit_conversion <= stock_unit.remaining_quantity:
                stock_unit.remaining_quantity -= unit_conversion
                stock_unit.is_cut = True
                stock_unit.save()
                return True

        # Si no se pudo restar todo el stock necesario, lanzar una excepción
        raise ValueError("No hay suficiente stock para restar la cantidad solicitada.")

    @property
    def total_stock(self):
        """
        Calcula el stock total sumando las cantidades restantes de todas las unidades.
        """
        main_unit = self.units.filter(is_main=True).first()
        if main_unit:
            main_unit = main_unit.unit.convert_to(main_unit.unit, main_unit.quantity)
            total = self.stock_units.aggregate(total=Sum('remaining_quantity'))['total']
            return float(main_unit) * float(total) if total is not None else 0
        else:
            total = self.stock_units.aggregate(total=Sum('remaining_quantity'))['total']
            return total if total is not None else 0    

class ProductUnit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="units")
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    quantity = models.FloatField()
    public_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    supplier_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_main = models.BooleanField(default=False)

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
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_units")
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