Ext.require([
    'Ext.form.field.File',
    'Ext.form.Panel',
    'Ext.window.MessageBox'
]);

Ext.onReady(function(){

    var msg = function(title, msg) {
        Ext.Msg.show({
            title: title,
            msg: msg,
            minWidth: 100,
            modal: true,
            icon: Ext.Msg.INFO,
            buttons: Ext.Msg.OK
        });
    };

    Ext.create('Ext.form.Panel', {
        standardSubmit: true,
        renderTo: 'transformsViewPort',
        width: 320,
        bodyPadding: '10 10 0',
        defaults: {
            anchor: '100%',
            allowBlank: false,
            msgTarget: 'side',
            labelWidth: 100
        },
        items: [{
                xtype: 'label',
                html: '<label class="x-form-item-label x-form-item-label-top"' +
                ' style="margin-bottom:5px;font-size: 13px; color: #5a5a5a" for="ext-gen1129">Transforms</label>'
            }, {
                xtype: 'tbspacer',
                width: 10
            }],
        buttons: [{
                xtype: 'button',
                text: _t('Reset to CorePlus Defaults'),
                handler: function() {
                    router.transformsResetDefaults({}, function(response) {
                        if (response.success) {
                            Zenoss.message.success(_t('Succesfully reset.'));
                        } else {
                            Zenoss.message.error(_t('Failed. Contact SteelHouse Labs support.'));
                        }
                    });
                }
            }, {
                xtype: 'button',
                text: _t('Backup and download'),
                handler: function() {
                    router.transformsBackupNdownload({}, function(response) {
                        if (response.success) {
                            Zenoss.message.success(_t('Success!'));
                        } else {
                            Zenoss.message.error(_t('Failed. Contact SteelHouse Labs support.'));
                        }
                    });
                }
            }
        ]
    });

    Ext.create('Ext.form.Panel', {
        standardSubmit: true,
        renderTo: 'eventClassViewPort',
        width: 320,
        bodyPadding: '10 10 0',
        defaults: {
            anchor: '100%',
            allowBlank: false,
            msgTarget: 'side',
            labelWidth: 100
        },
        items: [{
                xtype: 'label',
                html: '<label class="x-form-item-label x-form-item-label-top"' +
                ' style="margin-bottom:5px;font-size: 13px; color: #5a5a5a" for="ext-gen1129">EventClass Mappings and Configuration</label>'
            }, {
                xtype: 'tbspacer',
                width: 10
            }],
        buttons: [{
                xtype: 'button',
                text: _t('Reset to CorePlus Defaults'),
                handler: function() {
                    router.eventClassResetDefaults({}, function(response) {
                        if (response.success) {
                            Zenoss.message.success(_t('Succesfully reset.'));
                        } else {
                            Zenoss.message.error(_t('Failed. Contact SteelHouse Labs support.'));
                        }
                    });
                }
            }, {
                xtype: 'button',
                text: _t('Backup and download'),
                handler: function() {
                    router.eventClassBackupNdownload({}, function(response) {
                        if (response.success) {
                            Zenoss.message.success(_t('Success!'));
                        } else {
                            Zenoss.message.error(_t('Failed. Contact SteelHouse Labs support.'));
                        }
                    });
                }
           }
        ],

    });

    Ext.create('Ext.form.Panel', {
        standardSubmit: true,
        renderTo: 'eventClassViewPortB',
        width: '100%',
        height: '100%',
        minWidth: 500,
        maxWidth: 800,
        bodyPadding: '10 10 0',
        defaults: {
            anchor: '100%',
            allowBlank: false,
            msgTarget: 'side',
            labelWidth: 150
        },
        items: [{
                xtype: 'filefield',
                id: 'form-file',
                emptyText: 'Select a backup file...',
                fieldLabel: 'EventClass/Mapping backup File',
                name: 'fileData',
                buttonText:  'Select File',
                buttonConfig: {
                    iconCls: 'upload-icon'
                }
            }],
        buttons: [{
                xtype: 'button',
                text: 'Restore',
                handler: function(){
                    var form = this.up('form').getForm();
                    if(form.isValid()){
                        form.submit({
                            url: 'uploadEventClassBackup',
                            waitMsg: 'Uploading...',
                            success: function(fp, action) {
                                msg('Woopie!', 'Successfully saved your changes.');
                            },
                            failure: function(form, action) {
                                msg('Yikes!', 'Something is wrong.');
                            }
                        });
                    } else { // display error alert if the data is invalid
                            msg('Yikes!', 'Something is wrong. Check the form and try again.');
                    }
                  }
           }

        ],

    });

    Ext.create('Ext.form.Panel', {
        standardSubmit: true,
        renderTo: 'transformsViewPortB',
        width: '100%',
        height: '100%',
        minWidth: 500,
        maxWidth: 800,
        bodyPadding: '10 10 0',
        defaults: {
            anchor: '100%',
            allowBlank: false,
            msgTarget: 'side',
            labelWidth: 150
        },
        items: [{
                xtype: 'filefield',
                id: 'form-fileB',
                emptyText: 'Select a backup file...',
                fieldLabel: 'Transform backup file',
                name: 'fileData',
                buttonText:  'Select File',
                buttonConfig: {
                    iconCls: 'upload-icon'
                }
            }],
        buttons: [{
                xtype: 'button',
                text: 'Restore',
                handler: function(){
                    var form = this.up('form').getForm();
                    if(form.isValid()){
                        form.submit({
                            url: 'uploadTransformBackup',
                            waitMsg: 'Uploading...',
                            success: function(fp, action) {
                                msg('Woopie!', 'Successfully saved your changes.');
                            },
                            failure: function(form, action) {
                                msg('Yikes!', 'Something is wrong.');
                            }
                        });
                    } else { // display error alert if the data is invalid
                            msg('Yikes!', 'Something is wrong. Check the form and try again.');
                    }
                  }
           }

        ],

    });

    Ext.ns('Zenoss.settings');
    var router = Zenoss.remote.CorePlusSettingsRouter;

    function saveConfigValues(results, callback) {
        var values = results.values;

        router.setCorePlusSettings(values, callback);
    }

    function buildPropertyGrid(response) {
        var propsGrid,
            data;
        data = response.data;
        propsGrid = new Zenoss.form.SettingsGrid({
            renderTo: 'propList',
            width: '100%',
            height: '100%',
            minWidth: 500,
            maxWidth: 800,
            bodyPadding: '10 10 0',
            saveFn: saveConfigValues
        }, data);

        Ext.each(data, function(row){
            Zenoss.registerTooltipFor(row.id);
        });
    }

    function loadProperties() {
        router.getCorePlusSettings({}, buildPropertyGrid);
    }

    loadProperties();

});