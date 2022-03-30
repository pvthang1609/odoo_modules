odoo.define("inherit.ActionMenus", function (require) {
  "use strict";
  const ActionMenus = require("web.ActionMenus");

  ActionMenus.prototype._setActionItems = async function (props) {
    // Callback based actions
    const callbackActions = (props.items.other || []).map((action) =>
      Object.assign({ key: `action-${action.description}` }, action)
    );
    // Action based actions
    const actionActions = props.items.action || [];
    const relateActions = props.items.relate || [];
    const formattedActions = [...actionActions, ...relateActions].map(
      (action) => {
        return { action, description: action.name, key: action.id, icon: action.icon };
      }
    );
    // ActionMenus action registry components
    const registryActions = [];
    const rpc = this.rpc.bind(this);
    for (const { Component, getProps } of this.constructor.registry.values()) {
      const itemProps = await getProps(props, this.env, rpc);
      if (itemProps) {
        registryActions.push({
          Component,
          key: `registry-action-${registryActionId++}`,
          props: itemProps,
        });
      }
    }

    return [...callbackActions, ...formattedActions, ...registryActions];
  };
});
