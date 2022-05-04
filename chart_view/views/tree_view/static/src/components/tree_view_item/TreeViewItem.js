/** @odoo-module **/
const { Component } = owl;

export default class TreeViewItem extends Component { }

TreeViewItem.components = { TreeViewItem }
TreeViewItem.defaultProps = {}
TreeViewItem.props = {
    item: Object,
    onClickNode: Function,
}
TreeViewItem.template = "tree_view.TreeViewItem"
