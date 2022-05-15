/** @odoo-module **/
import { useService, useEffect } from "@web/core/utils/hooks";

const { Component, useState } = owl;

export class Notification extends Component {
    setup() {
        this.orm = useService('orm')
        this.actionService = useService("action");
        this.state = useState({
            count: 0,
            isOpen: false,
            tab: "unread",
            notifications: []
        })
        useEffect(
            () => {
                if (this.state.isOpen) {
                    this.getNotification(this.state.tab)
                }
            },
            () => [this.state.tab, this.state.isOpen]
        )
        this._onClickCaptureGlobal = this._onClickCaptureGlobal.bind(this);
    }

    willStart() {
        const legacyEnv = Component.env;
        legacyEnv.services.bus_service.onNotification(this,this.on_notification);
        this.getCountNotification()
        this.getNotification()
    }

    mounted() {
        document.addEventListener('click', this._onClickCaptureGlobal, true);
    }

    willUnmount() {
        document.removeEventListener('click', this._onClickCaptureGlobal, true);
    }

    _onClickCaptureGlobal(ev) {
        if (!this.el || this.el.contains(ev.target)) {
            return;
        }
        this.state.isOpen = false
    }

    getFormNow(dateString) {
        return moment.utc(dateString, "YYYY-MM-DD HH:mm:ss").fromNow()
    }

    async getCountNotification() {
        const count = await this.orm.call('vns.notification', 'compute_count_unread', [{}])
        this.state.count = count
    }

    async getNotification(type = 'unread') {
        const domain = type === 'unread' ? [['is_read','=',false]] : []
        const res = await this.orm.searchRead('vns.notification', domain)
        this.state.notifications = res
    }

    async on_notification(notifications) {
        for (let i = 0; i < notifications.length; i++) {
            if(notifications[i].type === 'create') {
                this.getNotification(this.state.tab)
                this.getCountNotification()
            }
        }
    }

    handleClickDropdownToggle() {
        this.state.isOpen = !this.state.isOpen
    }

    handleClickChangeTab(e) {
        const tab = e.target.getAttribute('data-tab-id')
        this.state.tab = tab
    }

    handleMarkAsRead(e) {
        e.stopPropagation();
        const notificationId = parseInt(e.target.getAttribute('data-notification-id'))
        this.orm.write('vns.notification', [notificationId], { is_read: true }).then(() => {
            this.getNotification(this.state.tab)
            this.getCountNotification()
        });
    }

    async handleMarkAsReadAll() {
         const search_res = await this.orm.searchRead('vns.notification', [['is_read','=',false]], ['id'])
         if (search_res.length > 0) {
             const notification_ids = search_res.map(n => n.id)
             const write_res = await this.orm.write('vns.notification', notification_ids, { is_read: true })
             if (write_res) {
                this.getNotification(this.state.tab)
                this.getCountNotification()
             }
         } else {
            this.actionService.doAction({
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'warning',
                    'title': "Hành động không được thực thi.",
                    'message': "Không còn thông báo chưa đọc nào.",
                }
            })
         }
    }

    _handleDirectLink(link,target) {
        return this.actionService.doAction({
            type: "ir.actions.act_url",
            url: link,
            target
        })
    }

    handlerClickNotification(link, target, id, isRead) {
        if (link) {
            this._handleDirectLink(link, target).then(() => {
                if (!isRead) {
                    this.orm.write('vns.notification', [id], { is_read: true }).then(() => {
                        this.getNotification(this.state.tab)
                        this.getCountNotification()
                    });
                }
            })
        }
    }

    handleDeleteNotification(e) {
        e.stopPropagation();
        const notificationId = parseInt(e.target.getAttribute('data-notification-id'))
        this.orm.unlink('vns.notification', [notificationId]).then(() => {
            this.getNotification(this.state.tab)
            this.getCountNotification()
        });
    }
}

Notification.template = "vns.Notification";