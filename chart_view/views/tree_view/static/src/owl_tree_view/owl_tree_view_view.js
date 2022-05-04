/** @odoo-module **/
import { XMLParser } from "@web/core/utils/xml";
import { useModel } from "@web/views/helpers/model";
import { standardViewProps } from "@web/views/helpers/standard_view_props";
import { registry } from "@web/core/registry";

import OWLTreeViewModel from "@tree_view/owl_tree_view/owl_tree_view_model"
import OWLTreeViewRenderer from "@tree_view/owl_tree_view/owl_tree_view_renderer"
import { Layout } from "@web/views/layout";


const { Component } = owl

class OWLTreeViewView extends Component {
    _parseArchOptions() {
        const parser = new XMLParser();
        const arch = parser.parseXML(this.props.arch);

        const arch_options = {};
        for (const attr of arch.getAttributeNames()) {
          arch_options[attr] = arch.getAttribute(attr);
        }

        const table = arch.querySelector('treeviewtable')
        const table_options = {};
        if(table) {
            for (const attr of table.getAttributeNames()) {
              table_options[attr] = table.getAttribute(attr);
            }
        }

        const fields = table ? Array.from(arch.querySelectorAll('treeviewtable > field')) : []
        const table_fields = fields.map(i => i.getAttribute('name'))

        return {arch_options, table_options, table_fields};
    }

     setup() {
        const { arch_options, table_options, table_fields } = this._parseArchOptions();
        this.archOptions = arch_options
        this.tableOptions = table_options
        this.tableFields = table_fields

        this.model = useModel(OWLTreeViewModel, {
          resModel: this.props.resModel,
          domain: this.props.domain,
          archOptions: this.archOptions,
          tableOptions: this.tableOptions,
          tableFields: this.tableFields,
        });

     }
}

OWLTreeViewView.type = "owl_tree_view";
OWLTreeViewView.display_name = "OWLTreeViewView";
OWLTreeViewView.icon = "fa-indent";
OWLTreeViewView.multiRecord = true;
OWLTreeViewView.searchMenuTypes = ["filter", "favorite"];
OWLTreeViewView.components = { Layout, OWLTreeViewRenderer };
OWLTreeViewView.props = {
  ...standardViewProps,
};
OWLTreeViewView.template = owl.tags.xml/* xml */ `
<Layout viewType="'owl_tree_view'">
    <OWLTreeViewRenderer archOptions="archOptions" tableOptions='tableOptions' tableFields='tableFields' model="model"/>
</Layout>`;

registry.category("views").add("owl_tree_view", OWLTreeViewView);