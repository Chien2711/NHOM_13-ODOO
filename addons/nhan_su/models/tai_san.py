from odoo import models, fields

class TaiSan(models.Model):
    _name = 'qlns.tai.san'
    _description = 'Quản lý Tài sản Nhân viên'

    name = fields.Char(string="Tên tài sản", required=True)
    ma_tai_san = fields.Char(string="Mã tài sản")
    ngay_cap = fields.Date(string="Ngày cấp", default=fields.Date.context_today)
    trang_thai = fields.Selection([
        ('dang_dung', 'Đang sử dụng'),
        ('thu_hoi', 'Đã thu hồi'),
        ('hong', 'Báo hỏng')
    ], string="Trạng thái", default='dang_dung')
    
    # Móc nối (Relate) tài sản này thuộc về nhân viên nào
    nhan_vien_id = fields.Many2one('nhan_vien', string="Người giữ")