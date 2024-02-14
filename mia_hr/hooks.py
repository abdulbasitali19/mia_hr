from . import __version__ as app_version

app_name = "mia_hr"
app_title = "MIA HR"
app_publisher = "abdul basit"
app_description = "hr module customization"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "mia.hr@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mia_hr/css/mia_hr.css"
# app_include_js = "/assets/mia_hr/js/mia_hr.js"

# include js, css files in header of web template
# web_include_css = "/assets/mia_hr/css/mia_hr.css"
# web_include_js = "/assets/mia_hr/js/mia_hr.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "mia_hr/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Purchase Order" : "public/js/purchase_order.js",
	"Material Request" : "public/js/material_request.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "mia_hr.install.before_install"
# after_install = "mia_hr.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "mia_hr.uninstall.before_uninstall"
# after_uninstall = "mia_hr.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mia_hr.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events


doc_events = {
    "Material Request":{
		"before_save": "mia_hr.overrides.material_request.check"
	},
	"Purchase Order":{
		"validate" : "mia_hr.overrides.purchase_order.updated_only_by_owner",
		"before_save" : "mia_hr.overrides.purchase_order.setting_first_approver"
	}


}
# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"mia_hr.tasks.all"
#	],
#	"daily": [
#		"mia_hr.tasks.daily"
#	],
#	"hourly": [
#		"mia_hr.tasks.hourly"
#	],
#	"weekly": [
#		"mia_hr.tasks.weekly"
#	]
#	"monthly": [
#		"mia_hr.tasks.monthly"
#	]
# }

# Testing
# -------

# before_tests = "mia_hr.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "mia_hr.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "mia_hr.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Request Events
# ----------------
# before_request = ["mia_hr.utils.before_request"]
# after_request = ["mia_hr.utils.after_request"]

# Job Events
# ----------
# before_job = ["mia_hr.utils.before_job"]
# after_job = ["mia_hr.utils.after_job"]

# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"mia_hr.auth.validate"
# ]

