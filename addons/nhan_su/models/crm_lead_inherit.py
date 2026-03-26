from odoo import models, fields, api

# ==========================================
# 1. KẾT NỐI BẢNG DỰ ÁN (PROJECT TASK)
# ==========================================
class ProjectTaskInherit(models.Model):
    _inherit = 'project.task'

    # Tạo thêm trường này để bảng Dự án biết đường nhận nhân viên từ QLNS bắn sang
    nhan_vien_qlns_id = fields.Many2one('nhan_vien', string="Người phụ trách (Từ QLNS)")

# ==========================================
# 2. KẾT NỐI BẢNG CRM LEAD
# ==========================================
class CrmLeadInherit(models.Model):
    _inherit = 'crm.lead'

    x_yeu_cau_khach_hang = fields.Text(string="Yêu cầu của khách hàng")
    x_san_pham_goi_y = fields.Char(string="Sản phẩm gợi ý (AI)", readonly=True)
    nhan_vien_qlns_id = fields.Many2one('nhan_vien', string="Nhân viên phụ trách (Từ QLNS)")

    def action_ai_goi_y_va_tao_viec(self):
        for rec in self:
            yeu_cau = (rec.x_yeu_cau_khach_hang or "").lower()
            if not yeu_cau:
                return {'type': 'ir.actions.client','tag': 'display_notification','params': {'title': 'Nhắc nhở', 'message': 'Bạn chưa nhập yêu cầu khách hàng!', 'type': 'warning'}}

            # ==========================================
            # NÂNG CẤP LOGIC AI: TỪ KHÓA TRỌNG SỐ (NLP Heuristic)
            # ==========================================
            # 1. Khai báo bộ từ khóa đào tạo AI cho 3 mảng nghiệp vụ
            bo_tu_khoa = {
                'tech': ['kho', 'mã vạch', 'nhập', 'xuất', 'tồn', 'vận chuyển', 'logistics', 'bảo trì'],
                'sales': ['bán hàng', 'pos', 'thu ngân', 'tạp hóa', 'hóa đơn', 'doanh thu', 'máy tính tiền'],
                'support': ['chăm sóc', 'cskh', 'khiếu nại', 'hotline', 'hỗ trợ', 'tổng đài', 'khách hàng cũ']
            }

            # 2. Bảng điểm xuất phát là 0
            diem_so = {'tech': 0, 'sales': 0, 'support': 0}

            # 3. Phân tích câu nói của khách: Trúng từ nào cộng điểm mảng đó
            for mang, danh_sach_tu in bo_tu_khoa.items():
                for tu in danh_sach_tu:
                    if tu in yeu_cau:
                        diem_so[mang] += 1

            # 4. Tìm mảng có điểm số cao nhất để quyết định
            tu_khoa_chuyen_mon = max(diem_so, key=diem_so.get)

            # Nếu khách nhập chung chung (tất cả đều 0 điểm)
            if diem_so[tu_khoa_chuyen_mon] == 0:
                san_pham = "Giải pháp ERP Tổng thể"
                tu_khoa_chuyen_mon = 'sales' # Mặc định đẩy cho bộ phận kinh doanh tư vấn trước
            elif tu_khoa_chuyen_mon == 'tech':
                san_pham = "Phần mềm Quản lý Kho & Vận hành"
            elif tu_khoa_chuyen_mon == 'support':
                san_pham = "Phần mềm Chăm sóc Khách hàng (CRM)"
            else:
                san_pham = "Phần mềm Bán hàng POS"

            rec.x_san_pham_goi_y = san_pham

            # ==========================================
            # KẾT NỐI QLNS & DỰ ÁN
            # ==========================================
            # Tìm nhân viên theo chuyên môn vừa phân tích được
            nhan_vien_phu_hop = self.env['nhan_vien'].search([('x_chuyen_mon', '=', tu_khoa_chuyen_mon)], limit=1)
            
            if not nhan_vien_phu_hop:
                nhan_vien_phu_hop = self.env['nhan_vien'].search([], limit=1)

            # Gán nhân viên QLNS vào trường trên CRM
            if nhan_vien_phu_hop:
                rec.nhan_vien_qlns_id = nhan_vien_phu_hop.id

            du_an = self.env['project.project'].search([('name', 'ilike', 'Triển khai')], limit=1)
            if not du_an:
                du_an = self.env['project.project'].search([], limit=1)

            if du_an:
                # Tạo Task bên Dự án
                self.env['project.task'].create({
                    'name': f"[AI Giao Việc] {san_pham} cho {rec.name}",
                    'project_id': du_an.id,
                    'description': f"Sản phẩm: {san_pham}\nChuyên môn cần: {tu_khoa_chuyen_mon}\nYêu cầu khách: {rec.x_yeu_cau_khach_hang}\n\n(Phân tích bằng AI Scoring System)",
                    
                    # QUAN TRỌNG: Gán đúng vào trường mới của bảng Task
                    'nhan_vien_qlns_id': nhan_vien_phu_hop.id if nhan_vien_phu_hop else False,
                })
                
                thong_bao = f"AI đã phân tích từ khóa và giao việc cho: {nhan_vien_phu_hop.ho_va_ten if nhan_vien_phu_hop else 'NV mặc định'}."
                loai_thong_bao = 'success'
            else:
                thong_bao = "Phân công NV thành công nhưng không tìm thấy dự án nào để tạo việc!"
                loai_thong_bao = 'warning'

            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {'title': 'AI NLP Scoring', 'message': thong_bao, 'type': loai_thong_bao}
            }