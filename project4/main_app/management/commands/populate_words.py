from django.core.management.base import BaseCommand
from main_app.models import GameWord

class Command(BaseCommand):
    help = 'Populate the database with sample words'

    def handle(self, *args, **options):
        # Sample words with their corresponding letter images
        sample_words = [
    # 3-letter words
    {'word': 'بيت', 'images': ['ب.png', 'ي.png', 'ت.png']},
    {'word': 'قمر', 'images': ['ق.png', 'م.png', 'ر.png']},
    {'word': 'شمس', 'images': ['ش.png', 'م.png', 'س.png']},
    {'word': 'نور', 'images': ['ن.png', 'و.png', 'ر.png']},
    {'word': 'باب', 'images': ['ب.png', 'ا.png', 'ب.png']},
    {'word': 'ماء', 'images': ['م.png', 'ا.png', 'ء.png']},
    {'word': 'ورد', 'images': ['و.png', 'ر.png', 'د.png']},
    {'word': 'قلب', 'images': ['ق.png', 'ل.png', 'ب.png']},
    {'word': 'يد',  'images': ['ي.png', 'د.png']},
    {'word': 'عين', 'images': ['ع.png', 'ي.png', 'ن.png']},
    {'word': 'أسد', 'images': ['أ.png', 'س.png', 'د.png']},
    {'word': 'نار', 'images': ['ن.png', 'ا.png', 'ر.png']},
    {'word': 'حوت', 'images': ['ح.png', 'و.png', 'ت.png']},
    {'word': 'ثور', 'images': ['ث.png', 'و.png', 'ر.png']},
    {'word': 'جمل', 'images': ['ج.png', 'م.png', 'ل.png']},
    {'word': 'دب',  'images': ['د.png', 'ب.png']},
    {'word': 'زهر', 'images': ['ز.png', 'ه.png', 'ر.png']},
    {'word': 'فيل', 'images': ['ف.png', 'ي.png', 'ل.png']},
    {'word': 'لبن', 'images': ['ل.png', 'ب.png', 'ن.png']},
    {'word': 'موز', 'images': ['م.png', 'و.png', 'ز.png']},
    {'word': 'نجم', 'images': ['ن.png', 'ج.png', 'م.png']},
    {'word': 'ورد', 'images': ['و.png', 'ر.png', 'د.png']},
    {'word': 'بحر', 'images': ['ب.png', 'ح.png', 'ر.png']},
    {'word': 'تمر', 'images': ['ت.png', 'م.png', 'ر.png']},

    # 4-letter words
    {'word': 'كتاب', 'images': ['ك.png', 'ت.png', 'ا.png', 'ب.png']},
    {'word': 'مفتاح', 'images': ['م.png', 'ف.png', 'ت.png', 'ا.png', 'ح.png']},
    {'word': 'هلال', 'images': ['ه.png', 'ل.png', 'ا.png', 'ل.png']},
    {'word': 'لعبه', 'images': ['ل.png', 'ع.png', 'ب.png', 'ه.png']},
    {'word': 'نهر', 'images': ['ن.png', 'ه.png', 'ر.png']},
    {'word': 'هدهد', 'images': ['ه.png', 'د.png', 'ه.png', 'د.png']},
    {'word': 'ورق', 'images': ['و.png', 'ر.png', 'ق.png']},
    {'word': 'أمل', 'images': ['أ.png', 'م.png', 'ل.png']},
    {'word': 'ثوب', 'images': ['ث.png', 'و.png', 'ب.png']},
    {'word': 'جبل', 'images': ['ج.png', 'ب.png', 'ل.png']},
    {'word': 'غيم', 'images': ['غ.png', 'ي.png', 'م.png']},
    {'word': 'حليب', 'images': ['ح.png', 'ل.png', 'ي.png', 'ب.png']},
    {'word': 'سعيد', 'images': ['س.png', 'ع.png', 'ي.png', 'د.png']},
    {'word': 'ورد', 'images': ['و.png', 'ر.png', 'د.png']},
    {'word': 'سهم', 'images': ['س.png', 'ه.png', 'م.png']},
    {'word': 'نحل', 'images': ['ن.png', 'ح.png', 'ل.png']},
    {'word': 'فجر', 'images': ['ف.png', 'ج.png', 'ر.png']},
    {'word': 'حجر', 'images': ['ح.png', 'ج.png', 'ر.png']},
    {'word': 'دجاج', 'images': ['د.png', 'ج.png', 'ا.png', 'ج.png']},
    {'word': 'حمار', 'images': ['ح.png', 'م.png', 'ا.png', 'ر.png']},

    # 5-letter words
    {'word': 'مفتاح', 'images': ['م.png', 'ف.png', 'ت.png', 'ا.png', 'ح.png']},
    {'word': 'مدرسة', 'images': ['م.png', 'د.png', 'ر.png', 'س.png', 'ة.png']},
    {'word': 'سيارة', 'images': ['س.png', 'ي.png', 'ا.png', 'ر.png', 'ة.png']},
    {'word': 'تفاحة', 'images': ['ت.png', 'ف.png', 'ا.png', 'ح.png', 'ة.png']},
    {'word': 'طائرة', 'images': ['ط.png', 'ا.png', 'ئ.png', 'ر.png', 'ة.png']},
    {'word': 'جميلة', 'images': ['ج.png', 'م.png', 'ي.png', 'ل.png', 'ة.png']},
    {'word': 'زهرة', 'images': ['ز.png', 'ه.png', 'ر.png', 'ة.png']},
    {'word': 'موزة', 'images': ['م.png', 'و.png', 'ز.png', 'ة.png']},
    {'word': 'مائدة', 'images': ['م.png', 'ا.png', 'ئ.png', 'د.png', 'ة.png']},
    {'word': 'مسرح', 'images': ['م.png', 'س.png', 'ر.png', 'ح.png']},
    {'word': 'قطار', 'images': ['ق.png', 'ط.png', 'ا.png', 'ر.png']},
    {'word': 'وردة', 'images': ['و.png', 'ر.png', 'د.png', 'ة.png']},
    {'word': 'صديق', 'images': ['ص.png', 'د.png', 'ي.png', 'ق.png']},
    {'word': 'مطر', 'images': ['م.png', 'ط.png', 'ر.png']},
    {'word': 'طفل', 'images': ['ط.png', 'ف.png', 'ل.png']},
    {'word': 'حقيبة', 'images': ['ح.png', 'ق.png', 'ي.png', 'ب.png', 'ة.png']},
    {'word': 'مكتبة', 'images': ['م.png', 'ك.png', 'ت.png', 'ب.png', 'ة.png']},
    {'word': 'سفينة', 'images': ['س.png', 'ف.png', 'ي.png', 'ن.png', 'ة.png']},
    {'word': 'مدينة', 'images': ['م.png', 'د.png', 'ي.png', 'ن.png', 'ة.png']},
    {'word': 'حديقة', 'images': ['ح.png', 'د.png', 'ي.png', 'ق.png', 'ة.png']},
]


        for word_data in sample_words:
            word_obj, created = GameWord.objects.get_or_create(
                word=word_data['word'],
                defaults={'images': word_data['images']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created word: {word_data["word"]}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Word already exists: {word_data["word"]}')
                )