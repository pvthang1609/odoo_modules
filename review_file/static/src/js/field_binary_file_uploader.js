/** @odoo-module alias=web.FieldMany2ManyBinaryMultiFilesInherit**/

    import {FieldMany2ManyBinaryMultiFiles} from 'web.relational_fields';

    FieldMany2ManyBinaryMultiFiles.include({
         events: {
                'click .o_attach': '_onAttach',
                'click .o_attachment_delete': '_onDelete',
                'change .o_input_file': '_onFileChanged',
                'click .o_view_file': '_onFileViewed',
         },
         _onFileViewed: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();

            var fileID = $(ev.currentTarget).data('id');
            var fileName = $(ev.currentTarget).data('name');

            this.do_action({
                name: `Review file tài liệu - ${fileName}`,
                view_mode: 'iframe',
                views: [[false, 'iframe']],
                res_model: 'ir.attachment',
                type: 'ir.actions.act_window',
                target: 'new',
                context: {
                    'file_id': fileID
                }
            })
        },
    })