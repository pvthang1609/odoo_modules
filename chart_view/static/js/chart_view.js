odoo.define("chart_view.ChartView", function (require) {
    "use strict";
    const AbstractController = require('web.AbstractController');
    const AbstractModel = require('web.AbstractModel');
    const AbstractRenderer = require('web.AbstractRenderer');
    const AbstractView = require('web.AbstractView');
    const viewRegistry = require('web.view_registry');
    const SearchPanel = require('web.searchPanel');
    const ControlPanel = require('web.ControlPanel');

    const ChartController = AbstractController.extend({})
    const ChartRenderer = AbstractRenderer.extend({
        className: "",
        on_attach_callback: function () {
            this.isInDOM = true;
            this._renderChart();
        },
        _render: function() {
            this.$el.append(
                $('<canvas id="myChart" width="400" height="400">')
            )
            return $.when();
        },
        _renderChart: function () {
            const ctx = document.getElementById('myChart').getContext('2d');
            const myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
                    datasets: [{
                        label: '# of Votes',
                        data: [12, 19, 3, 5, 2, 3],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(153, 102, 255, 0.2)',
                            'rgba(255, 159, 64, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)',
                            'rgba(153, 102, 255, 1)',
                            'rgba(255, 159, 64, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        },
    })
    const ChartModel = AbstractModel.extend({})

    const ChartView = AbstractView.extend({
        config: {
            Model: ChartModel,
            Controller: ChartController,
            Renderer: ChartRenderer,
            ControlPanel: ControlPanel,
            SearchPanel: SearchPanel
        },
        viewType: 'chart'
    })

    viewRegistry.add('chart', ChartView)

    return ChartView

    })