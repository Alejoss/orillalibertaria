# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Temas.imagen'
        db.add_column(u'temas_temas', 'imagen',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Temas.imagen'
        db.delete_column(u'temas_temas', 'imagen')


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
        },
        u'temas.mensajes': {
            'Meta': {'object_name': 'Mensajes'},
            'deleted_inbox': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted_sentbox': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mensaje': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True'}),
            'usuario_envia': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'envia'", 'null': 'True', 'to': u"orm['perfiles.Perfiles']"}),
            'usuario_recibe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'recibe'", 'null': 'True', 'to': u"orm['perfiles.Perfiles']"})
        },
        u'temas.notificaciones': {
            'Meta': {'object_name': 'Notificaciones'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'leido': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'tema': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['temas.Temas']", 'null': 'True'}),
            'tipo_notificacion': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'usuario_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['perfiles.Perfiles']", 'null': 'True'})
        },
        u'temas.posts': {
            'Meta': {'object_name': 'Posts'},
            'creador': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['perfiles.Perfiles']", 'null': 'True'}),
            'eliminado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'es_respuesta': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tema': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['temas.Temas']", 'null': 'True'}),
            'texto': ('django.db.models.fields.TextField', [], {'max_length': '10000', 'null': 'True'}),
            'votos_negativos': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'votos_positivos': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        u'temas.respuestas': {
            'Meta': {'object_name': 'Respuestas'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_padre': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_original'", 'null': 'True', 'to': u"orm['temas.Posts']"}),
            'post_respuesta': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'respuesta'", 'null': 'True', 'to': u"orm['temas.Posts']"})
        },
        u'temas.tema_descripcion': {
            'Meta': {'object_name': 'Tema_descripcion'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tema': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['temas.Temas']"}),
            'texto': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'usuario': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['perfiles.Perfiles']"})
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
        u'temas.votos': {
            'Meta': {'object_name': 'Votos'},
            'fecha': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_votado': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['temas.Posts']", 'null': 'True'}),
            'tema': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['temas.Temas']", 'null': 'True'}),
            'tipo': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'usuario_votado': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votado'", 'null': 'True', 'to': u"orm['perfiles.Perfiles']"}),
            'usuario_votante': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votante'", 'null': 'True', 'to': u"orm['perfiles.Perfiles']"})
        }
    }

    complete_apps = ['temas']