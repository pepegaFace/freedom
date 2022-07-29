from django.db import models


class Category(models.Model):
    """
    Модель категории
    """
    name = models.CharField('Name category', help_text='Required', max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class SubCategory(models.Model):
    """
    Модель под-категории
    """
    name = models.CharField('Name sub category', help_text='Required', max_length=150, unique=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, help_text='Required', verbose_name='Category')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Subcategories"


class Product(models.Model):
    """
    Модель товара
    """
    name = models.CharField('Name', help_text='Required', max_length=150)
    price = models.PositiveIntegerField('Price', help_text='Required', default=1)
    sub_category = models.ManyToManyField(SubCategory)

    # Напольные покрытия и плитка
    article = models.CharField('Article', help_text='Required', max_length=150, default='None', null=True)
    brand = models.CharField('Brand', help_text='Required', max_length=150, default='None', null=True)
    size = models.CharField('Size', help_text='Required', max_length=150, default='None', null=True)
    product_class = models.CharField('Class', help_text='Required', max_length=150, default='None', null=True)
    fire_class = models.CharField('Fire class', help_text='Required', max_length=150, default='None', null=True)
    purpose_of_goods = models.CharField('Purpose of goods', help_text='Required', max_length=150, default='None', null=True)

    # Двери
    series = models.CharField('Series', help_text='Required', max_length=150, default='None', null=True)
    loops = models.PositiveIntegerField('Loops', help_text='Required', default='0', null=True)
    locks = models.CharField('Locks', help_text='Required', max_length=150, default='None', null=True)
    material = models.CharField('Materials', help_text='Required', max_length=150, default='None', null=True)
    blade_thickness = models.CharField('Blade thickness', help_text='Required', max_length=150, default='None', null=True)
    color = models.CharField('Color', help_text='Required', max_length=150, default='None', null=True)

    # Освещение
    supplier = models.CharField('Supplier', help_text='Required', max_length=150, default='None', null=True)
    collection = models.CharField('Collection', help_text='Required', max_length=150, default='None', null=True)
    style = models.CharField('Style', help_text='Required', max_length=150, default='None', null=True)
    base_type = models.CharField('Base type', help_text='Required', max_length=150, default='None', null=True)
    count_lamp = models.PositiveIntegerField('Count lamp', help_text='Required', default='0', null=True)
    max_lamp_power = models.PositiveIntegerField('Max lamp power', help_text='Required', default='0', null=True)
    height = models.PositiveIntegerField('Height', help_text='Required', default='0', null=True)
    diameter = models.PositiveIntegerField('Diameter', help_text='Required', default='0', null=True)
    descriptions = models.TextField('Descriptions', help_text='Required', default='None', null=True)

    # Декор стен
    docking_method = models.CharField('Docking method', help_text='Required', max_length=150, default='None', null=True)
    drawing = models.CharField('Drawing', help_text='Required', max_length=150, default='None', null=True)

    # Сантехника
    power = models.CharField('Power', help_text='Required', max_length=150, default='None', null=True)
    package = models.CharField('Package', help_text='Required', max_length=150, default='None', null=True)

    # Садовые конструкции
    voltage = models.CharField('Voltage', help_text='Required', max_length=150, default='None', null=True)
