from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Territory, UserProfile

class Command(BaseCommand):
    help = 'Create users for each territory and an admin user'

    def handle(self, *args, **kwargs):
        created_count = updated_count = 0
        default_password = 'coralcal'
        for territory in Territory.objects.all():
            username = territory.territory.strip()
            if not username:
                continue
            user, user_created = User.objects.get_or_create(username=username)
            if user_created:
                user.set_password(default_password)
                user.save()
                created_count += 1
                self.stdout.write(f"Created user: {username}")
            else:
                updated_count += 1
            
            profile, created_profile = UserProfile.objects.update_or_create(
                user=user,
                defaults={
                    'user_type': 'territory',
                    'zone_name': territory.zone_name,
                    'region_name': territory.region_name
                }
            )
            if created_profile:
                self.stdout.write(f"Created profile for user: {username}")
            else:
                self.stdout.write(f"Updated profile for user: {username}")
            
        # Create zone users 
        for zone in Territory.objects.values_list('zone_name', flat=True).distinct():
            if not zone:
                continue
            username = zone.lower().replace(' ', '_')
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=default_password)
                UserProfile.objects.create(user=user, user_type='zone', zone_name=zone)
                self.stdout.write(self.style.SUCCESS(f'Created zone user: {username}'))
        
        # Region Users
        for region in Territory.objects.values_list('region_name', flat=True).distinct():
            username = region.lower().replace(' ', '_')
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=default_password)
                UserProfile.objects.create(user=user, user_type='region', region_name=region)
                self.stdout.write(self.style.SUCCESS(f'Created region user: {username}'))