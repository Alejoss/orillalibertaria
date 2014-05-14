# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VDenunciados'
        db.create_table(u'videos_vdenunciados', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['videos.Videos'], null=True)),
            ('perfil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['perfiles.Perfiles'], null=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('eliminado', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'videos', ['VDenunciados'])

        # Adding model 'VFavoritos'
        db.create_table(u'videos_vfavoritos', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['videos.Videos'], null=True)),
            ('perfil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['perfiles.Perfiles'], null=True)),
            ('fecha', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('eliminado', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'videos', ['VFavoritos'])


    def backwards(self, orm):
        # Deleting model 'VDenunciados'
        db.delete_table(u'videos_vdenunciados')

        # Deleting model 'VFavoritos'
        db.delete_table(u'videos_vfavoritos')


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
        },
        u'temas.temas': {
            'Meta': {'object_name': 'Temas'},
            'activo': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'creador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['perfiles.Perfiles']", 'null': 'True'}),
            'fecha_creacion': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagen': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'nivel_actividad': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'nivel_popularidad': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True'})
        },
        u'videos.vdenunciados': {
            'Meta': {'object_name': 'VDenunciados'},
            'eliminado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'perfil': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['perfiles.Perfiles']", 'null': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['videos.Videos']", 'null': 'True'})
        },
        u'videos.vfavoritos': {
            'Meta': {'object_name': 'VFavoritos'},
            'eliminado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'perfil': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['perfiles.Perfiles']", 'null': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['videos.Videos']", 'null': 'True'})
        },
        u'videos.videos': {
            'Meta': {'object_name': 'Videos'},
            'denunciado': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'eliminado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'es_youtube': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'favoritos_recibidos': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'perfil': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['perfiles.Perfiles']", 'null': 'True'}),
            'tema': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['temas.Temas']", 'null': 'True'}),
            'titulo': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'youtube_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100'})
        }
    }

    complete_apps = ['videos']