from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# ---------------- FOR General Information ------------------
class MenuLanguage(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class GeneralInfo(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    menu_language = models.ForeignKey(MenuLanguage, on_delete=models.SET_NULL, null=True)
    dimensions = models.CharField(max_length=200, null=True, blank=True)
    weight = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    body_material = models.CharField(max_length=200, null=True, blank=True)
    body_protection = models.CharField(max_length=200, null=True, blank=True)
    simCard_amount = models.IntegerField(null=True, blank=True, default=0)
    box_description =models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self._id)


# ---------------- FOR Memory Information ------------------

class RamAmount(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    ram_amount = models.IntegerField(null=True, blank=True, default=0) #GB

    def __str__(self):
        return str(self.ram_amount)


class InternalMemory(models.Model):
     _id = models.AutoField(primary_key=True, editable=False)
     internal_memory_amount = models.IntegerField(null=True, blank=True, default=0) #GB
     def __str__(self):
         return str(self.internal_memory_amount)


class MemoryInfo(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    ram_amount = models.ForeignKey(RamAmount, on_delete=models.SET_NULL, null=True)
    internal_memory = models.ForeignKey(InternalMemory, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return str(self._id)

# ---------------- FOR Processor and OS Information ------------------

class OperationalSystem(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    version = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return (self.name + ' Version: ' + self.version)

class Cpu(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class Gpu(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class ProccessorAndOs(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    os_id = models.ForeignKey(OperationalSystem, on_delete=models.SET_NULL, null=True)
    cpu_id = models.ForeignKey(Cpu, on_delete=models.SET_NULL, null=True)
    gpu_id = models.ForeignKey(Gpu, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self._id)


# ---------------- FOR PRODUCT --------------

class Parameters(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    common_id = models.ForeignKey(GeneralInfo, on_delete=models.SET_NULL, null=True)
    memory_id = models.ForeignKey(MemoryInfo, on_delete=models.SET_NULL, null=True)
    proccessor_and_os_id =  models.ForeignKey(ProccessorAndOs, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return str(self._id)


class Category(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Brand(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    user =  models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    parameters_id =  models.ForeignKey(Parameters, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    is_promoted = models.BooleanField(default=False)
    count_in_stock = models.IntegerField(null=True, blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


