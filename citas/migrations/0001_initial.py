# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cita'
        db.create_table(u'citas_cita', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('texto', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('autor', self.gf('django.db.models.fields.CharField')(max_length=150, null=True)),
            ('favoritos_recibidos', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('creador', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['perfiles.Perfiles'], null=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('denunciada', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('correcta', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('eliminada', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'citas', ['Cita'])

        # Adding model 'Cfavoritas'
        db.create_table(u'citas_cfavoritas', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cita', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['citas.Cita'], null=True)),
            ('perfil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['perfiles.Perfiles'], null=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('eliminado', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'citas', ['Cfavoritas'])

        # Adding model 'Ceditadas'
        db.create_table(u'citas_ceditadas', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cita', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['citas.Cita'], null=True)),
            ('perfil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['perfiles.Perfiles'], null=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('razon', self.gf('django.db.models.fields.CharField')(max_length=250)),
        ))
        db.send_create_signal(u'citas', ['Ceditadas'])


    def backwards(self, orm):
        # Deleting model 'Cita'
        db.delete_table(u'citas_cita')

        # Deleting model 'Cfavoritas'
        db.delete_table(u'citas_cfavoritas')

        # Deleting model 'Ceditadas'
        db.delete_table(u'citas_ceditadas')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'citas.ceditadas': {
            'Meta': {'object_name': 'Ceditadas'},
            'cita': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['citas.Cita']", 'null': 'True'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'perfil': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['perfiles.Perfiles']", 'null': 'True'}),
            'razon': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'citas.cfavoritas': {
            'Meta': {'object_name': 'Cfavoritas'},
            'cita': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['citas.Cita']", 'null': 'True'}),
            'eliminado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'perfil': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['perfiles.Perfiles']", 'null': 'True'})
        },
        u'citas.cita': {
            'Meta': {'object_name': 'Cita'},
            'autor': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'correcta': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'creador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['perfiles.Perfiles']", 'null': 'True'}),
            'denunciada': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'eliminada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'favoritos_recibidos': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'texto': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'perfiles.perfiles': {
            'Meta': {'object_name': 'Perfiles'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link10': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link3': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link4': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link5': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link6': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link7': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link8': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link9': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'numero_de_posts': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'usuario': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True'}),
            'votos_recibidos': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['citas']