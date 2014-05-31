# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Notificaciones'
        db.delete_table(u'notificaciones_notificaciones')

        # Adding model 'Notificacion'
        db.create_table(u'notificaciones_notificacion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('actor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actor', null=True, to=orm['perfiles.Perfiles'])),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receptor', to=orm['perfiles.Perfiles'])),
            ('objeto_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('tipo_objeto', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('tipo_notificacion', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('leida', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'notificaciones', ['Notificacion'])


    def backwards(self, orm):
        # Adding model 'Notificaciones'
        db.create_table(u'notificaciones_notificaciones', (
            ('id_objeto', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(related_name='receptor', to=orm['perfiles.Perfiles'])),
            ('leida', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tipo_notificacion', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('actor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='actor', null=True, to=orm['perfiles.Perfiles'])),
            ('tipo_objeto', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
        ))
        db.send_create_signal(u'notificaciones', ['Notificaciones'])

        # Deleting model 'Notificacion'
        db.delete_table(u'notificaciones_notificacion')


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
        u'notificaciones.notificacion': {
            'Meta': {'object_name': 'Notificacion'},
            'actor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'actor'", 'null': 'True', 'to': u"orm['perfiles.Perfiles']"}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leida': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'objeto_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
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