import re

with open("frontend/src/config/navigation.js", "r", encoding="utf-8") as f:
    content = f.read()

nav_item_addition = """  admin_center: {
    id: 'admin_center',
    label: 'Admin Center',
    icon: Activity,
    path: '/admin-center',
    adminOnly: true,
  },
"""

# Insert into NAV_ITEMS
content = content.replace("export const NAV_ITEMS = {", "export const NAV_ITEMS = {\n" + nav_item_addition)

# Insert into DEFAULT_ADMIN_ORDER
admin_order_orig = """export const DEFAULT_ADMIN_ORDER = [
  'channels',"""
admin_order_new = """export const DEFAULT_ADMIN_ORDER = [
  'channels',
  'admin_center',"""
content = content.replace(admin_order_orig, admin_order_new)

with open("frontend/src/config/navigation.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Patched navigation.js!")
