/** @odoo-module **/
import { Model } from "@web/views/helpers/model";
import { KeepLast } from "@web/core/utils/concurrency";

export default class OWLTreeViewModel extends Model {
    setup(params, { orm }) {
        this.modelName = params.resModel;
        this.orm = orm;
        this.keepLast = new KeepLast();
        this.archOptions = params.archOptions;
        this.tableOptions = params.tableOptions;
        this.tableFields = params.tableFields;
    };

    _transformData(originData, arr_index) {
        return originData.map((item, index) => ({
            id: item.id,
            name: item[this.archOptions.display],
            count: item[this.archOptions.count],
            isOpen: false,
            isSelect: false,
            child_id: item[this.archOptions.child],
            index: [...arr_index, index],
            child: []
        }))
    }

    async load(searchParams) {
        const response = await this.keepLast.add(
          this.orm.searchRead(this.modelName, [[this.archOptions.parent, '=', false]]),
        );
        this.data = this._transformData(response, [])
        this.notify();
    }

    async getChildNodeData(child_id, arr_index) {
        const response = await this.keepLast.add(
          this.orm.searchRead(this.modelName, [['id', 'in', child_id]])
        );
        const data = this._transformData(response, arr_index)
        return data
    };

    async getDataTable(arr_filter) {
        if(this.tableFields.length > 0) {
            const domain = arr_filter ? [[this.tableOptions.relation_field, 'in', arr_filter]] : []
            const table_response = await this.keepLast.add(
              this.orm.searchRead(this.tableOptions.name, domain, this.tableFields),
            );
            return table_response;
        } else {
            return []
        }
    }
}

OWLTreeViewModel.services = ["orm"];