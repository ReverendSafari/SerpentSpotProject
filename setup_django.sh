#!/bin/bash
# Exit on any error
set -e


# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Create superuser
echo "Creating superuser..."
cat <<EOF | python manage.py shell
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='safari').exists():
    User.objects.create_superuser('safari', 'safari@example.com', 'saf')
EOF

echo "Setup complete."
