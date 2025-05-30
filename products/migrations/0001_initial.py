# Generated by Django 4.2 on 2024-08-07 07:06

from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40, unique=True, verbose_name='نام')),
                ('image', models.ImageField(blank=True, null=True, upload_to='category-and-brands/', verbose_name='عکس')),
            ],
        ),
        migrations.CreateModel(
            name='MainCategory',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40, verbose_name='نام')),
                ('image', models.ImageField(blank=True, null=True, upload_to='category-and-brands/', verbose_name='عکس')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.maincategory', verbose_name='زیر دسته')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='کد محصول')),
                ('cover_image', models.ImageField(blank=True, null=True, upload_to='cover_images/', verbose_name='عکس کاور')),
                ('name', models.CharField(max_length=200, verbose_name='نام محصول')),
                ('price', models.PositiveIntegerField(verbose_name='قیمت')),
                ('discount', models.PositiveSmallIntegerField(default=0, verbose_name='تخفیف (%)')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='تعداد')),
                ('description', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('active', models.BooleanField(default=True, verbose_name='فعال')),
                ('created', django_jalali.db.models.jDateField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', django_jalali.db.models.jDateField(auto_now=True, verbose_name='تاریخ آپدیت')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.maincategory', verbose_name='دسته بندی اصلی')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.base')),
            ],
            options={
                'verbose_name': 'برند',
                'verbose_name_plural': 'برند ها',
            },
            bases=('products.base',),
        ),
        migrations.CreateModel(
            name='SpecialCategory',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='products.base')),
            ],
            options={
                'verbose_name': 'دسته بندی مناسبتی',
                'verbose_name_plural': 'دسته بندی مناسبتی',
            },
            bases=('products.base',),
        ),
        migrations.CreateModel(
            name='ProductFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, verbose_name='موضوع')),
                ('value', models.CharField(max_length=100, verbose_name='مقدار')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='products.product', verbose_name='محصول')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='products.brand', verbose_name='برند'),
        ),
    ]
