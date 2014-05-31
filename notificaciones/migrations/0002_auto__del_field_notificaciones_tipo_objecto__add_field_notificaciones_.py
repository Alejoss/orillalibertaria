# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Notificaciones.tipo_objecto'
        db.delete_column(u'notificaciones_notificaciones', 'tipo_objecto')

        # Adding field 'Notificaciones.tipo_objeto'
        db.add_column(u'notificaciones_notificaciones', 'tipo_objeto',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True),
                      keep_default=False)


        # Changing field 'Notificaciones.tipo_notificacion'
        db.alter_column(u'notificaciones_notificaciones', 'tipo_notificacion', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Notificaciones.tipo_objecto'
        raise RuntimeError("Cannot reverse this migration. 'Notificaciones.tipo_objecto' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Notificaciones.tipo_objecto'
        db.add_column(u'notificaciones_notificaciones', 'tipo_objecto',
                      self.gf('django.db.models.fields.CharField')(max_length=20),
                      keep_default=False)

        # Deleting field 'Notificaciones.tipo_objeto'
        db.delete_column(u'notificaciones_notificaciones', 'tipo_objeto')


        # Changing field 'Notificaciones.tipo_notificacion'
        db.alter_column(u'notificaciones_notificaciones', 'tipo_notificacion', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'notificaciones.notificaciones': {
            'Meta': {'object_name': 'Notificaciones'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actor'", 'null': 'True', 'to': u"orm['perfiles.Perfiles']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notificacion'", 'to': u"orm['contenttypes.ContentType']"}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leida': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'receptor'", 'to': u"orm['perfiles.Perfiles']"}),
            'tipo_notificacion': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'tipo_objeto': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        u'perfiles.perfiles': {
            'Meta': {'object_name': 'Perfiles'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link3': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link4': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'link5': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'numero_de_posts': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'usuario': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'null': 'True'}),
            'votos_recibidos': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['notificaciones']