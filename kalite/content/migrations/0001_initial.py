# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TopicTree'
        db.create_table(u'content_topictree', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('root_node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Node'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'content', ['TopicTree'])

        # Adding M2M table for field editors on 'TopicTree'
        m2m_table_name = db.shorten_name(u'content_topictree_editors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('topictree', models.ForeignKey(orm[u'content.topictree'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['topictree_id', 'user_id'])

        # Adding model 'Node'
        db.create_table(u'content_node', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sort_order', self.gf('django.db.models.fields.FloatField')(default=0, unique=True, max_length=50)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['content.Node'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'content', ['Node'])

        # Adding unique constraint on 'Node', fields ['parent', 'name']
        db.create_unique(u'content_node', ['parent_id', 'name'])

        # Adding model 'Draft'
        db.create_table(u'content_draft', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('publish_in', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['content.Node'], unique=True)),
        ))
        db.send_create_signal(u'content', ['Draft'])

        # Adding model 'ContentVideoNode'
        db.create_table(u'content_contentvideonode', (
            (u'node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['content.Node'], unique=True, primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('license_owner', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('published_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('retrieved_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.ContentLicense'])),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('video_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'content', ['ContentVideoNode'])

        # Adding model 'ContentVideoDraft'
        db.create_table(u'content_contentvideodraft', (
            (u'draft_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['content.Draft'], unique=True, primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('license_owner', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('published_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('retrieved_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.ContentLicense'])),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('video_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'content', ['ContentVideoDraft'])

        # Adding model 'ContentPDFNode'
        db.create_table(u'content_contentpdfnode', (
            (u'node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['content.Node'], unique=True, primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('license_owner', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('published_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('retrieved_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.ContentLicense'])),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('pdf_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'content', ['ContentPDFNode'])

        # Adding model 'ContentPDFDraft'
        db.create_table(u'content_contentpdfdraft', (
            (u'draft_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['content.Draft'], unique=True, primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('license_owner', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('published_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('retrieved_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.ContentLicense'])),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('pdf_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'content', ['ContentPDFDraft'])

        # Adding model 'ExerciseNode'
        db.create_table(u'content_exercisenode', (
            (u'node_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['content.Node'], unique=True, primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('license_owner', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('published_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('retrieved_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.ContentLicense'])),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'content', ['ExerciseNode'])

        # Adding model 'ExerciseDraft'
        db.create_table(u'content_exercisedraft', (
            (u'draft_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['content.Draft'], unique=True, primary_key=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('license_owner', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('published_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('retrieved_on', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.ContentLicense'])),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'content', ['ExerciseDraft'])

        # Adding model 'ContentLicense'
        db.create_table(u'content_contentlicense', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'content', ['ContentLicense'])


    def backwards(self, orm):
        # Removing unique constraint on 'Node', fields ['parent', 'name']
        db.delete_unique(u'content_node', ['parent_id', 'name'])

        # Deleting model 'TopicTree'
        db.delete_table(u'content_topictree')

        # Removing M2M table for field editors on 'TopicTree'
        db.delete_table(db.shorten_name(u'content_topictree_editors'))

        # Deleting model 'Node'
        db.delete_table(u'content_node')

        # Deleting model 'Draft'
        db.delete_table(u'content_draft')

        # Deleting model 'ContentVideoNode'
        db.delete_table(u'content_contentvideonode')

        # Deleting model 'ContentVideoDraft'
        db.delete_table(u'content_contentvideodraft')

        # Deleting model 'ContentPDFNode'
        db.delete_table(u'content_contentpdfnode')

        # Deleting model 'ContentPDFDraft'
        db.delete_table(u'content_contentpdfdraft')

        # Deleting model 'ExerciseNode'
        db.delete_table(u'content_exercisenode')

        # Deleting model 'ExerciseDraft'
        db.delete_table(u'content_exercisedraft')

        # Deleting model 'ContentLicense'
        db.delete_table(u'content_contentlicense')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'})
        },
        u'content.contentlicense': {
            'Meta': {'object_name': 'ContentLicense'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'content.contentpdfdraft': {
            'Meta': {'object_name': 'ContentPDFDraft', '_ormbases': [u'content.Draft']},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'draft_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['content.Draft']", 'unique': 'True', 'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.ContentLicense']"}),
            'license_owner': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pdf_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'published_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'retrieved_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'content.contentpdfnode': {
            'Meta': {'object_name': 'ContentPDFNode', '_ormbases': [u'content.Node']},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.ContentLicense']"}),
            'license_owner': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['content.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'pdf_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'published_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'retrieved_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'content.contentvideodraft': {
            'Meta': {'object_name': 'ContentVideoDraft', '_ormbases': [u'content.Draft']},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'draft_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['content.Draft']", 'unique': 'True', 'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.ContentLicense']"}),
            'license_owner': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'retrieved_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'video_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'content.contentvideonode': {
            'Meta': {'object_name': 'ContentVideoNode', '_ormbases': [u'content.Node']},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.ContentLicense']"}),
            'license_owner': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['content.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'published_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'retrieved_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'video_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'content.draft': {
            'Meta': {'object_name': 'Draft'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publish_in': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['content.Node']", 'unique': 'True'})
        },
        u'content.exercisedraft': {
            'Meta': {'object_name': 'ExerciseDraft', '_ormbases': [u'content.Draft']},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'draft_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['content.Draft']", 'unique': 'True', 'primary_key': 'True'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.ContentLicense']"}),
            'license_owner': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'published_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'retrieved_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'content.exercisenode': {
            'Meta': {'object_name': 'ExerciseNode', '_ormbases': [u'content.Node']},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'license': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.ContentLicense']"}),
            'license_owner': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'node_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['content.Node']", 'unique': 'True', 'primary_key': 'True'}),
            'published_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'retrieved_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'content.node': {
            'Meta': {'unique_together': "(('parent', 'name'),)", 'object_name': 'Node'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['content.Node']"}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'sort_order': ('django.db.models.fields.FloatField', [], {'default': '0', 'unique': 'True', 'max_length': '50'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'content.topictree': {
            'Meta': {'object_name': 'TopicTree'},
            'editors': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'root_node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['content.Node']"}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['content']