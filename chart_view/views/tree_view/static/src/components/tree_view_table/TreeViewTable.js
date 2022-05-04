/** @odoo-module **/
const { Component } = owl;

export default class TreeViewTable extends Component {

}

TreeViewTable.components = { }
TreeViewTable.defaultProps = { }
TreeViewTable.props = {
    tableFields: Array,
    data: Array,
}
TreeViewTable.template = "tree_view.TreeViewTable"
