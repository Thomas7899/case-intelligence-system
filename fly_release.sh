#!/bin/bash
# Fly.io Release Script - Runs on every deploy before the app starts
# This ensures database migrations and demo user are always set up

set -e

echo "🚀 Running database migrations..."
python manage.py migrate --noinput

echo "👤 Setting up demo user..."
python manage.py shell << 'EOF'
from django.contrib.auth.models import User

# Create admin if not exists
admin, admin_created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@caseintelligence.dev',
        'is_staff': True,
        'is_superuser': True
    }
)
if admin_created:
    admin.set_password('admin123secure')
    admin.save()
    print("✅ Admin user created")
else:
    print("ℹ️  Admin user already exists")

# Create demo_reviewer for recruiters
demo, demo_created = User.objects.get_or_create(
    username='demo_reviewer',
    defaults={
        'email': 'demo@caseintelligence.dev',
        'first_name': 'Demo',
        'last_name': 'Reviewer',
        'is_staff': False,
        'is_superuser': False
    }
)
demo.set_password('demo2024secure')
demo.save()
if demo_created:
    print("✅ Demo user 'demo_reviewer' created")
else:
    print("ℹ️  Demo user updated")

print("🎉 User setup complete!")
EOF

echo "✅ Release complete!"
