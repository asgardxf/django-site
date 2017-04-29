from django.db import migrations, models

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    TP = apps.get_model("stats", "TradePoint")
    db_alias = schema_editor.connection.alias
    TP.objects.using(db_alias).bulk_create([
        TP(
            name = "Тестовая",
            region = "63",
            city = "Самара",
            address = "улица никакая, дом 0",
        )
    ])
    
    Target = apps.get_model("stats", "Target")




class Migration(migrations.Migration):
    dependencies = [
        ('stats', '0002_auto_20170429_0948'),
    ]

    operations = [
        migrations.RunPython(forwards_func)
    ]