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

    Ext.ns('Zenoss.settings');
    var router = Zenoss.remote.supportSettingsRouter;

    function saveConfigValues(results, callback) {
        var values = results.values;

        router.setSupportSettings(values, callback);
    }

    function buildPropertyGrid(response) {
        var propsGrid,
            data;
        data = response.data;
        propsGrid = new Zenoss.form.SettingsGrid({
            renderTo: 'propList',
            width: '100%',
            height: '1200',
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
        router.getSupportSettings({}, buildPropertyGrid);
    }

    loadProperties();

});
