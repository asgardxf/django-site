from django.db import migrations, models
import datetime

def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it'll be the wrong version
    Target = apps.get_model("stats", "Target")
    TP = apps.get_model("stats", "TradePoint")
    db_alias = schema_editor.connection.alias
    Target.objects.using(db_alias).bulk_create([
        Target(
            trade_point = TP.objects.get(pk=1)
        )
    ])

    Game = apps.get_model("stats", "Game")

    Game.objects.using(db_alias).bulk_create([
        Game(
            trade_point = TP.objects.get(pk=1),
            target = Target.objects.get(pk=1),
            start_time = datetime.datetime.now(),
            fallen_count = 0,
            idle_count = 0,
            prise = 1,
            interrupt = 0,
            service = 0
        ),
                Game(
            trade_point = TP.objects.get(pk=1),
            target = Target.objects.get(pk=1),
            start_time = datetime.datetime.now(),
            fallen_count = 0,
            idle_count = 0,
            prise = 1,
            interrupt = 0,
            service = 0
        ),
                        Game(
            trade_point = TP.objects.get(pk=1),
            target = Target.objects.get(pk=1),
            start_time = datetime.datetime.now(),
            fallen_count = 0,
            idle_count = 0,
            prise = 1,
            interrupt = 0,
            service = 0
        )
    ])




class Migration(migrations.Migration):
    dependencies = [
        ('stats', '0004_game_target'),
    ]

    operations = [
        migrations.RunPython(forwards_func)
    ]