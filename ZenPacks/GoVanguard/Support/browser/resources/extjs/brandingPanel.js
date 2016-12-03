Ext.require([
    'Ext.form.field.File',
    'Ext.form.Panel',
    'Ext.window.MessageBox'
]);

Ext.onReady(function(){

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
        router.getBrandingSettings({}, buildPropertyGrid);
    }

    loadProperties();

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
        renderTo: 'viewPort',
        width: '100%',
        height: '100%',
        minWidth: 500,
        maxWidth: 800,
        bodyPadding: '10 10 0',

        defaults: {
            anchor: '100%',
            allowBlank: false,
            msgTarget: 'side',
            labelWidth: 100
        },

        items: [{
            xtype: 'filefield',
            id: 'form-file',
            emptyText: 'Select a 65x65 pixel image',
            fieldLabel: 'Branding image',
            name: 'fileData',
            buttonText:  'Select File',
            buttonConfig: {
                iconCls: 'upload-icon'
            }
        } , {
            xtype:'image',
            fieldLabel: 'Current branding image',
            id: 'contImage',
            src: 'company-logo.png',
            maxWidth: 65,
            minWidth: 65,
            width: 65,
            maxHeight: 65,
            minHeight: 65,
            height: 65
        }],

        buttons: [{
            text: 'Upload',
            handler: function(){
                var form = this.up('form').getForm();
                if(form.isValid()){
                    form.submit({
                        url: 'uploadBrandingImage',
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
        }]
    });

});
