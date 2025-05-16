import os
from django.core.management.base import BaseCommand
from django.conf import settings
from products.models import Product  # نام اپلیکیشن خودت رو جایگزین کن

class Command(BaseCommand):
    help = "افزودن تصاویر به فیلد cover_image محصولات بر اساس نام فایل‌ها"

    def handle(self, *args, **kwargs):
        cover_images_path = os.path.join(settings.MEDIA_ROOT, 'cover_images')

        if not os.path.exists(cover_images_path):
            self.stdout.write(self.style.ERROR(f"❌ مسیر {cover_images_path} وجود ندارد!"))
            return

        image_files = os.listdir(cover_images_path)
        updated_count = 0

        for filename in image_files:
            try:
                # فقط عدد اول نام فایل را در نظر بگیر (مثلاً `14338.jpg`)
                product_id = int(os.path.splitext(filename)[0])  
                product = Product.objects.filter(id=product_id).first()

                if product:
                    image_path = f'cover_images/{filename}'

                    # بررسی اینکه تصویر قبلاً تنظیم نشده باشد
                    if not product.cover_image or product.cover_image.name != image_path:
                        product.cover_image = image_path
                        product.save()
                        self.stdout.write(self.style.SUCCESS(f"✅ تصویر {filename} برای محصول {product_id} تنظیم شد."))
                        updated_count += 1
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ محصول با ID {product_id} یافت نشد!"))
            
            except ValueError:
                self.stdout.write(self.style.WARNING(f"⚠️ فرمت نام فایل {filename} صحیح نیست!"))

        self.stdout.write(self.style.SUCCESS(f"🎉 تعداد {updated_count} تصویر به محصولات اضافه شد."))

