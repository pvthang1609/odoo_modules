from odoo import models
import io
import base64
import datetime


class SaleOrderXlsx(models.AbstractModel):
    _name = 'report.sale.report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def set_column(self, sheet, data):
        for item in data:
            s = item['s']
            e = item['e']
            h = item['h']
            sheet.set_column(s, e, h)

    def set_row(self, sheet, data):
        for item in data:
            p = item['p']  # POSITION
            h = item['h']
            sheet.set_row(p, h)

    def render_address(self, workbook, sheet, position):
        x = position['x']
        y = position['y']
        c_name_company = "CÔNG TY CỔ PHẦN VẬT TƯ VÀ THIẾT BỊ CÔNG NGHIỆP DIMO VIỆT NAM"
        c_address = "Địa chỉ: Số 9-B14, ngõ 15 đường Hàm Nghi, phường Cầu Diễn, quận Nam Từ Liêm, thành phố Hà Nội, Việt Nam"
        c_phone = "ĐT: 0243.992.5886"
        c_tax = "MST: 0105430056"
        c_website = "Website: http://dimovietnam.com/"

        # STYLE
        s_general = workbook.add_format({'font_size': 13, 'bold': True, 'text_wrap': True})
        s_header = workbook.add_format({'font_size': 13, 'bold': True, 'align': 'center', 'text_wrap': True})

        # RENDER
        sheet.merge_range(x, y, x + 1, y + 3, c_name_company, s_header)
        sheet.merge_range(x + 2, y, x + 3, y + 3, c_address, s_header)
        sheet.merge_range(x + 4, y, x + 4, y + 3, c_phone, s_general)
        sheet.merge_range(x + 5, y, x + 5, y + 3, c_tax, s_general)
        sheet.merge_range(x + 6, y, x + 6, y + 3, c_website, s_general)

    def render_logo(self, sheet, position):
        x = position['x']
        y = position['y']
        logo_company = io.BytesIO(base64.b64decode(self.env.user.company_id.logo))

        # SETUP
        sheet.merge_range(x, y, x + 6, y + 2, None)

        # RENDER
        sheet.insert_image(x, y, "logo.png", {'image_data': logo_company})

    def render_heading(self, workbook, sheet, position, title):
        x = position['x']
        y = position['y']

        # STYLE
        s_general = workbook.add_format({'font_size': 20, 'bold': True, 'align': 'center'})

        # RENDER
        sheet.merge_range(x, y, x, y + 6, title, s_general)

    def render_date(self, workbook, sheet, position):
        x = position['x']
        y = position['y']
        d = datetime.datetime.now()
        date_now = "Hà Nội, ngày %s tháng %s năm %s" % (d.day, d.month, d.year)

        # STYLE
        s_general = workbook.add_format({'font_size': 13, 'italic': True, 'align': 'right'})

        # RENDER
        sheet.merge_range(x, y, x, y + 6, date_now, s_general)

    def render_info(self, workbook, sheet, position):
        x = position['x']
        y = position['y']

        # STYLE
        s_title = workbook.add_format({'font_size': 13, 'bold': True, 'align': 'center'})
        s_info = workbook.add_format({'font_size': 13, 'text_wrap': True})

        # RENDER
        sheet.merge_range(x, y, x, y + 6, "NỘI DUNG VIẾT HÓA ĐƠN", s_title)
        # INFO_SALE
        sheet.merge_range(x + 1, y, x + 1, y + 2, "Đơn vị bán: Công ty CP VT&TB Công nghiệp Dimo VN", s_info)
        sheet.merge_range(x + 2, y, x + 2, y + 2, "MST: 0105430056", s_info)
        sheet.merge_range(x + 3, y, x + 4, y + 2,
                          "Đ/c: Số 9-B14, ngõ 15 đường Hàm Nghi, phường Cầu Diễn, quận Nam Từ Liêm, thành phố Hà Nội, Việt Nam",
                          s_info)
        sheet.merge_range(x + 5, y, x + 5, y + 2, "ĐT: 0243.992.5886", s_info)
        sheet.merge_range(x + 6, y, x + 6, y + 2, "Số Hợp đồng/ PO:", s_info)
        # INFO_PURCHASE
        sheet.merge_range(x + 1, y + 3, x + 1, y + 6, "Đ.vị mua hàng: Công ty Cổ phần Vật liệu Xây dựng Việt Nam",
                          s_info)
        sheet.merge_range(x + 2, y + 3, x + 2, y + 6, "MST: 3100405421", s_info)
        sheet.merge_range(x + 3, y + 3, x + 4, y + 6,
                          "Địa chỉ: Thôn Xuân Hạ, xã Văn Hóa, huyện Tuyên Hóa, Quảng Bình",
                          s_info)
        sheet.merge_range(x + 5, y + 3, x + 5, y + 6, "Thông tin người liên hệ trên hóa đơn:", s_info)
        sheet.merge_range(x + 6, y + 3, x + 6, y + 6,
                          "Họ và tên:                                             Số điện thoại:", s_info)
        sheet.merge_range(x + 7, y + 3, x + 7, y + 6, "E-mail:", s_info)

    def render_records(self, workbook, sheet, position, records):
        x = position['x']
        y = position['y']
        data_headers = [{'c': 'STT'},
                        {'c': 'Thông tin về sản phẩm (Tên hàng hóa và Model)'},
                        {'c': 'Số lượng'},
                        {'c': 'Đơn vị tính'},
                        {'c': 'Đơn giá'},
                        {'c': 'Thành tiền'}]

        # STYLE
        s_title = workbook.add_format({'font_size': 13, 'bold': True})
        s_header = workbook.add_format({'font_size': 12, 'bold': True, 'align': 'center'})
        s_record_id = workbook.add_format({'align': 'center'})

        # RENDER
        sheet.merge_range(x, y, x + 1, y + 6, "1. Thông tin về hàng hóa:", s_title)
        # HEADER
        for i in range(len(data_headers)):
            sheet.write(x + 2, y + 1 + i, data_headers[i]['c'], s_header)
        # RECORD
        for i in range(len(records)):
            partner = records[i]['partner_id']['name']
            total = records[i]['amount_total']
            sheet.write(x + 3 + i, y + 1, i + 1, s_record_id)
            sheet.write(x + 3 + i, y + 2, partner)
            sheet.write(x + 3 + i, y + 6, total)

    def generate_xlsx_report(self, workbook, data, records):
        sheet = workbook.add_worksheet('De_nghi_xuat_hoa_don')
        width_cols = [{'s': 0, 'e': 0, 'h': 2},
                      {'s': 1, 'e': 1, 'h': 3},
                      {'s': 2, 'e': 2, 'h': 9},
                      {'s': 3, 'e': 3, 'h': 47},
                      {'s': 4, 'e': 7, 'h': 16}]
        height_rows = [{'p': 0, 'h': 12}, {'p': 8, 'h': 35}]

        # SETUP
        sheet.set_default_row(20.3)
        self.set_row(sheet, height_rows)
        self.set_column(sheet, width_cols)

        # RENDER
        self.render_logo(sheet, {'x': 1, 'y': 1})
        self.render_address(workbook, sheet, {'x': 1, 'y': 4})
        self.render_heading(workbook, sheet, {'x': 8, 'y': 1}, "ĐỀ NGHỊ XUẤT HÓA ĐƠN")
        self.render_date(workbook, sheet, {'x': 9, 'y': 1})
        self.render_info(workbook, sheet, {'x': 10, 'y': 1})
        self.render_records(workbook, sheet, {'x': 18, 'y': 1}, records)
