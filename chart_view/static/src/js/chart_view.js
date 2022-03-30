odoo.define("chart_view.ChartView", function (require) {
  "use strict";
  const AbstractController = require("web.AbstractController");
  const AbstractModel = require("web.AbstractModel");
  const AbstractRenderer = require("web.AbstractRenderer");
  const AbstractView = require("web.AbstractView");
  const viewRegistry = require("web.view_registry");
  const SearchPanel = require("web.searchPanel");
  const ControlPanel = require("web.ControlPanel");

  const ChartController = AbstractController.extend({});
  const ChartRenderer = AbstractRenderer.extend({
    className: "",
    on_attach_callback: function () {
      this.isInDOM = true;
      console.log(this.arch);
      this._renderChart();
    },
    _render: function () {
      const cBar = $(
        '<div class="canvas_bg"><canvas id="chart-bar"></canvas></div>'
      );
      const dBar = $(
        '<div class="canvas_bg_doughnut"><canvas id="chart-doughnut"></canvas></div>'
      );
      this.$el.addClass("chart_container").append(cBar, dBar);
      return $.when();
    },
    _transformDataOrder: function (
      source_data,
      byValue,
      statisticalUnit,
      label
    ) {
      let labels = [];
      let backgroundColor = [];
      let data = [];
      let color_index = 0;

      source_data.forEach((element) => {
        const COLORS = [
          "#FFD93D",
          "#6BCB77",
          "#533E85",
          "#FF6B6B",
          "#D82148",
          "#FFB2A6",
          "#4D96FF",
          "#00C897",
        ];
        const user_index = labels.indexOf(element[byValue]);
        if (user_index < 0) {
          labels.push(element[byValue]);
          data.push(element[statisticalUnit]);
          backgroundColor.push(COLORS[color_index]);
          color_index++;
        } else {
          data[user_index] += element[statisticalUnit];
        }
      });
      let dataReturn = {
        labels,
        datasets: [
          {
            backgroundColor,
            borderColor: "#fff",
            data,
          },
        ],
      };
      if (label) {
        dataReturn.datasets[0].label = label;
      }
      return dataReturn;
    },
    _renderChart: function () {
      const orders_config_bar = {
        type: "bar",
        data: this._transformDataOrder(
          this.state.orders,
          "state",
          "amount_total"
        ),
        options: {
          plugins: {
            legend: {
              display: false,
            },
            title: {
              display: true,
              text: "Thống kê giá trị đơn hàng theo trạng thái đơn hàng",
            },
          },
        },
      };
      const orders_config_doughnut = {
        type: "doughnut",
        data: this._transformDataOrder(
          this.state.orders,
          "user_name",
          "amount_total",
          "Tổng giá trị đơn hàng"
        ),
        options: {
          plugins: {
            legend: {
              position: "bottom",
            },
            title: {
              display: true,
              text: "Thống kê giá trị đơn hàng theo người dùng",
            },
          },
        },
      };
      const chartBar = new Chart(
        document.getElementById("chart-bar"),
        orders_config_bar
      );
      const chartDoughnut = new Chart(
        document.getElementById("chart-doughnut"),
        orders_config_doughnut
      );
    },
  });
  const ChartModel = AbstractModel.extend({
    get: function () {
      return { orders: this.orders };
    },
    load: function (params) {
      this.displayOrders = true;
      return this._load(params);
    },
    _load: function (params) {
      this.domain = params.domain || this.domain || [];
      if (this.displayOrders) {
        var self = this;
        return this._rpc({
          model: "sale.order",
          method: "search_read",
          fields: ["id", "create_uid", "state", "tax_totals_json", "user_id"],
          domain: this.domain,
        }).then(function (result) {
          self.orders = self._transformData(result);
        });
      }
      this.orders = [];
      return $.when();
    },
    _transformData: function (data) {
      return data.map((item) => {
        const { create_uid, user_id, tax_totals_json, ...rest } = item;
        const create_name = create_uid[1];
        const user_name = user_id[1];
        const amount_total = JSON.parse(tax_totals_json).amount_total;
        return { ...rest, create_name, user_name, amount_total };
      });
    },
  });

  const ChartView = AbstractView.extend({
    config: {
      Model: ChartModel,
      Controller: ChartController,
      Renderer: ChartRenderer,
      ControlPanel: ControlPanel,
      SearchPanel: SearchPanel,
    },
    viewType: "chart",
    init: function () {
      this._super.apply(this, arguments);
      // this.loadParams.displayContacts = this.arch.attrs.display_contacts;
    },
  });

  viewRegistry.add("chart", ChartView);

  return ChartView;
});
