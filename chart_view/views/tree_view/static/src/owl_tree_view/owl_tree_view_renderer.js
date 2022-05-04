/** @odoo-module **/
import AbstractRendererOwl from "web.AbstractRendererOwl";
import TreeViewItem from "@tree_view/components/tree_view_item/TreeViewItem";
import TreeViewTable from "@tree_view/components/tree_view_table/TreeViewTable";
import { useService, useEffect } from "@web/core/utils/hooks";

const { useState } = owl;

export default class OWLTreeViewRenderer extends AbstractRendererOwl {
    setup() {
        super.setup(...arguments)
        this.state = useState({treeViewItems: [] });
        this.filter = []
        this.tableRecords = useState([]);
        this.orm = useService("orm");
        this.clickCount = 0;
        this.timeout = 300;
        useEffect(
            () => {
                const response = this.props.model.getDataTable(this.filter)
                console.log(response)
                return () => console.log('clean effect')
            },
            () => [this.filter],
        )

        //bind function
        this.handleClickNode = this.handleClickNode.bind(this)
        this.handleActionWithNode = this.handleActionWithNode.bind(this)
    };


    async willStart() {
      this.state.treeViewItems = this.props.model.data
      const tableRecords = await this.props.model.getDataTable()
      this.tableRecords = tableRecords
    };

    async handleActionWithNode(arr_index, child_id, child) {
          this.clickCount++;
          if (this.clickCount == 1) {
            setTimeout(() => {
              if(this.clickCount == 1) {
                this.handleClickNode(arr_index, child_id, child);
              } else {
                this.handleDblClickNode(arr_index, child_id, child);
              }
              this.clickCount = 0;
            }, this.timeout || 300);
          }
    }

    async handleClickNode(arr_index, child_id, child) {
        if(child_id.length > 0) {
            let positionClickedNode = "this.state.treeViewItems[arr_index[0]]"
            for(let i = 1; i <= arr_index.length - 1; i++ ) {
                positionClickedNode += `.child[${arr_index[i]}]`
            }
            const pathNode = eval(positionClickedNode)
            if(child_id.length !== child.length) {
                const child_data = await this.props.model.getChildNodeData(child_id, arr_index)
                pathNode.child = child_data
            }
            pathNode.isOpen = !pathNode.isOpen
        }
    }

    handleDblClickNode(arr_index, child_id, child) {
        let positionClickedNode = "this.state.treeViewItems[arr_index[0]]"
        for(let i = 1; i <= arr_index.length - 1; i++ ) {
            positionClickedNode += `.child[${arr_index[i]}]`
        }
        const pathNode = eval(positionClickedNode)
        pathNode.isSelect = !pathNode.isSelect
        if(pathNode.isSelect) {
            this.filter = [...this.filter, pathNode.id]
        } else {
            const index = this.filter.findIndex(i => i == pathNode.id)
            if (index > -1) {
              const cloned = [...this.filter]
              this.filter = [cloned.splice(index, 1)]
            }
        }
    }
}


OWLTreeViewRenderer.components = { TreeViewItem, TreeViewTable };
OWLTreeViewRenderer.defaultProps = {};
OWLTreeViewRenderer.props = {
    archOptions: Object,
    model: Object,
    tableOptions: Object,
    tableFields: Array,
};
OWLTreeViewRenderer.template = "tree_view.OWLTreeViewRenderer";