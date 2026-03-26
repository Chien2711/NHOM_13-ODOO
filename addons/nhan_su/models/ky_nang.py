from odoo import models, fields

class KyNang(models.Model):
    _name = 'qlns.ky.nang'
    _description = 'Đánh giá Kỹ năng Nhân viên'

    name = fields.Char(string="Tên kỹ năng", required=True)
    muc_do = fields.Selection([
        ('1', '⭐ (Mới học)'),
        ('2', '⭐⭐ (Cơ bản)'),
        ('3', '⭐⭐⭐ (Khá)'),
        ('4', '⭐⭐⭐⭐ (Tốt)'),
        ('5', '⭐⭐⭐⭐⭐ (Chuyên gia)')
    ], string="Đánh giá mức độ", default='3')
    
    # Móc nối kỹ năng này với nhân viên nào
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên")