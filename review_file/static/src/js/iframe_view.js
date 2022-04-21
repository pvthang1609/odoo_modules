/** @odoo-module alias=web.IframeView **/

//import BasicView from 'web.BasicView';
import BasicView from 'web.BasicView';
import IframeModel from 'web.IframeModel'
import IframeRenderer from 'web.IframeRenderer'
import IframeController from 'web.IframeController'
import viewRegistry from 'web.view_registry'


var IframeView = BasicView.extend({
    config: _.extend({}, BasicView.prototype.config, {
            Model: IframeModel,
            Renderer: IframeRenderer,
            Controller: IframeController,
        }),
    viewType: 'iframe',
})

viewRegistry.add("iframe", IframeView);

export default IframeView;


