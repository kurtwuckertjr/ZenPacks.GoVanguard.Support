Ext.require([
    'Ext.form.field.File',
    'Ext.form.Panel',
    'Ext.window.MessageBox'
]);

Ext.onReady(function(){

    Ext.ns('Zenoss.settings');

    Ext.create('Ext.form.Panel', {
        renderTo: 'footerPortal',
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
            xtype:'image',
            fieldLabel: 'GoVanguard',
            id: 'contImage',
            src: 'http://www.gvit.com/wp-content/uploads/2015/12/LogoHeader.png'
        }]

    });

});
