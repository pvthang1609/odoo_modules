/** @odoo-module alias=web.IframeRenderer **/

import BasicRenderer from 'web.BasicRenderer';


var IframeRenderer = BasicRenderer.extend({
    on_attach_callback: function () {
          this.isInDOM = true;
    },
    async _renderView() {
          const context = this.state.getContext()
          const iframe = $(
            `<iframe src="/web/content/${context.file_id}" style="width:100%;height:70vh"></iframe>`
          );
          this.$el.append(iframe);
    },
})

export default IframeRenderer;