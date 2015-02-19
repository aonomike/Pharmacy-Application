# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DrugFlowTracker'
        db.create_table('DrugFlowTracker', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('transactiontype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['commodities.StockTransactionType'], null=True, db_column='transactionType', blank=True)),
            ('transactiondate', self.gf('django.db.models.fields.DateTimeField')(null=True, db_column='transactionDate', blank=True)),
            ('tranbatch', self.gf('django.db.models.fields.CharField')(max_length=20, db_column='tranBatch')),
            ('arvdrug', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_column='arvDrugId', blank=True)),
            ('expirydate', self.gf('django.db.models.fields.DateTimeField')(null=True, db_column='expiryDate', blank=True)),
            ('remarks', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(null=True, db_column='quantity', blank=True)),
            ('operator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='myActions', to=orm['auth.User'])),
        ))
        db.send_create_signal('AuditTrail', ['DrugFlowTracker'])


    def backwards(self, orm):
        # Deleting model 'DrugFlowTracker'
        db.delete_table('DrugFlowTracker')


    models = {
        'AuditTrail.drugflowtracker': {
            'Meta': {'object_name': 'DrugFlowTracker', 'db_table': "'DrugFlowTracker'"},
            'arvdrug': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_column': "'arvDrugId'", 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expirydate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "'expiryDate'", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'myActions'", 'to': "orm['auth.User']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'db_column': "'quantity'", 'blank': 'True'}),
            'remarks': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tranbatch': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_column': "'tranBatch'"}),
            'transactiondate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_column': "'transactionDate'", 'blank': 'True'}),
            'transactiontype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['commodities.StockTransactionType']", 'null': 'True', 'db_column': "'transactionType'", 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'commodities.stocktransactiontype': {
            'Meta': {'object_name': 'StockTransactionType', 'db_table': "u'tblstocktransactiontype'"},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'reporttitle': ('django.db.models.fields.CharField', [], {'max_length': '45', 'db_column': "u'reportTitle'", 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['AuditTrail']