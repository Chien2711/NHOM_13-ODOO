import odoo
import logging

# Cấu hình để kết nối DB
config_path = 'odoo.conf'
odoo.tools.config.parse_config(['-c', config_path])
db_name = 'hoangchien'

registry = odoo.registry(db_name)
with registry.cursor() as cr:
    env = odoo.api.Environment(cr, odoo.SUPERUSER_ID, {})
    # Tìm tất cả user KHÔNG PHẢI là portal (người dùng nội bộ)
    admins = env['res.users'].search([('share', '=', False)])
    print("\n--- DANH SÁCH TÀI KHOẢN ADMIN TRONG HỆ THỐNG ---")
    for user in admins:
        print(f"Login (Tên đăng nhập): {user.login} | Tên: {user.name}")
    print("------------------------------------------------\n")
