import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audit_automation.settings')
django.setup()

from user_management.models import Unit

def create_structure():
    print("Creating Org Structure...")
    
    # Root
    vertical, _ = Unit.objects.get_or_create(name='Audit Vertical', unit_type='VERTICAL')
    
    # Domains
    plant, _ = Unit.objects.get_or_create(name='Plant', parent=vertical, unit_type='DOMAIN')
    ho_ro, _ = Unit.objects.get_or_create(name='HO & RO', parent=vertical, unit_type='DOMAIN')
    
    # Sub Domains
    Unit.objects.get_or_create(name='Operations', parent=plant, unit_type='SUB_DOMAIN')
    Unit.objects.get_or_create(name='Risk & Analytics', parent=plant, unit_type='SUB_DOMAIN')
    Unit.objects.get_or_create(name='Functions', parent=ho_ro, unit_type='SUB_DOMAIN')
    
    print("Org Structure Created:")
    for unit in Unit.objects.all():
        parent = unit.parent.name if unit.parent else "None"
        print(f"- {unit.name} ({unit.unit_type}) [Parent: {parent}]")

if __name__ == '__main__':
    create_structure()
