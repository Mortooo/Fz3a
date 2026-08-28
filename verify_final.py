import os, io
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User

staff, _ = User.objects.get_or_create(username='s1')
staff.is_staff = True
staff.set_password('x12345')
staff.save()

out = []
c = Client()
r = c.get('/dashboard/settings/')
out.append('anon redirect: %s %s' % (r.status_code, r.get('Location')))

r = c.get('/dashboard/login/')
body = r.content.decode('utf-8')
out.append('login page has form title %r: %s' % ('تسجيل الدخول', 'تسجيل الدخول' in body))

r = c.post('/dashboard/login/', {'username': 's1', 'password': 'wrong'})
body = r.content.decode('utf-8')
out.append('error message present %r: %s' % ('بيانات الدخول غير صحيحة', 'بيانات الدخول غير صحيحة' in body))
out.append('error part2 %r: %s' % ('غير مخوّل للوحة التحكم', 'غير مخوّل للوحة التحكم' in body))

r = c.post('/dashboard/login/', {'username': 's1', 'password': 'x12345'})
out.append('valid login redirect: %s %s' % (r.status_code, r.get('Location')))

with io.open('verify_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))
print('written')
