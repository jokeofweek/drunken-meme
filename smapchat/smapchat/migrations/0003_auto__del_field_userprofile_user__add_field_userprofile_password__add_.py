# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'UserProfile.user'
        db.delete_column(u'smapchat_userprofile', 'user_id')

        # Adding field 'UserProfile.password'
        db.add_column(u'smapchat_userprofile', 'password',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=128),
                      keep_default=False)

        # Adding field 'UserProfile.last_login'
        db.add_column(u'smapchat_userprofile', 'last_login',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'UserProfile.is_superuser'
        db.add_column(u'smapchat_userprofile', 'is_superuser',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'UserProfile.email'
        db.add_column(u'smapchat_userprofile', 'email',
                      self.gf('django.db.models.fields.EmailField')(default=None, unique=True, max_length=75),
                      keep_default=False)

        # Adding field 'UserProfile.full_name'
        db.add_column(u'smapchat_userprofile', 'full_name',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255),
                      keep_default=False)

        # Adding field 'UserProfile.is_active'
        db.add_column(u'smapchat_userprofile', 'is_active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'UserProfile.is_admin'
        db.add_column(u'smapchat_userprofile', 'is_admin',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding M2M table for field groups on 'UserProfile'
        m2m_table_name = db.shorten_name(u'smapchat_userprofile_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'smapchat.userprofile'], null=False)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'group_id'])

        # Adding M2M table for field user_permissions on 'UserProfile'
        m2m_table_name = db.shorten_name(u'smapchat_userprofile_user_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'smapchat.userprofile'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'permission_id'])


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'UserProfile.user'
        raise RuntimeError("Cannot reverse this migration. 'UserProfile.user' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'UserProfile.user'
        db.add_column(u'smapchat_userprofile', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True),
                      keep_default=False)

        # Deleting field 'UserProfile.password'
        db.delete_column(u'smapchat_userprofile', 'password')

        # Deleting field 'UserProfile.last_login'
        db.delete_column(u'smapchat_userprofile', 'last_login')

        # Deleting field 'UserProfile.is_superuser'
        db.delete_column(u'smapchat_userprofile', 'is_superuser')

        # Deleting field 'UserProfile.email'
        db.delete_column(u'smapchat_userprofile', 'email')

        # Deleting field 'UserProfile.full_name'
        db.delete_column(u'smapchat_userprofile', 'full_name')

        # Deleting field 'UserProfile.is_active'
        db.delete_column(u'smapchat_userprofile', 'is_active')

        # Deleting field 'UserProfile.is_admin'
        db.delete_column(u'smapchat_userprofile', 'is_admin')

        # Removing M2M table for field groups on 'UserProfile'
        db.delete_table(db.shorten_name(u'smapchat_userprofile_groups'))

        # Removing M2M table for field user_permissions on 'UserProfile'
        db.delete_table(db.shorten_name(u'smapchat_userprofile_user_permissions'))


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'smapchat.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'full_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        }
    }

    complete_apps = ['smapchat']