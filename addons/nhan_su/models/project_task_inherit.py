from odoo import models, fields

class ProjectTaskInherit(models.Model):
    _inherit = 'project.task' 
    # Kế thừa bảng công việc của Odoo

    # Thêm trường để lưu nhân viên của bạn vào Task
    nhan_vien_phu_trach_id = fields.Many2one('nhan_vien', string="Nhân viên phụ trách (Custom)")