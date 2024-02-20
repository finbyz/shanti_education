from . import __version__ as app_version

app_name = "shanti_education"
app_title = "SHANTI EDUCATION"
app_publisher = "FINBYZ TECH PVT LTD"
app_description = "EDUCATION"
app_email = "info@finbyz.com"
app_license = "MIT"

# Includes in <head>
# ------------------

fixtures = [
       {
         "dt": "Role", 
         "filters":[["name", "in", ['Timeline Disable']]]
      },
]

# include js, css files in header of desk.html
# app_include_css = "/assets/shanti_education/css/shanti_education.css"
# app_include_js = "/assets/shanti_education/js/shanti_education.js"

# include js, css files in header of web template
# web_include_css = "/assets/shanti_education/css/shanti_education.css"
# web_include_js = "/assets/shanti_education/js/shanti_education.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "shanti_education/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}
doctype_js = {
    "Lead" : "public/js/lead.js",
    "Issue": "public/js/issue.js",
    "Purchase Invoice": "public/js/purchase_invoice.js",
    "Stock Entry": "public/js/stock_entry.js"
	}
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

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "shanti_education.utils.jinja_methods",
#	"filters": "shanti_education.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "shanti_education.install.before_install"
# after_install = "shanti_education.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "shanti_education.uninstall.before_uninstall"
# after_uninstall = "shanti_education.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "shanti_education.notifications.get_notification_config"

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

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }
doc_events = {
	"Lead": {
		"validate": "shanti_education.shanti_education.doc_event.lead.validate"
	},
  "Material Request":{
      "before_validate" : "shanti_education.shanti_education.doc_event.material_request.before_validate"
  },
  "Purchase Order" :{
      "before_validate" : "shanti_education.shanti_education.doc_event.purchase_order.before_validate"
  },
  ("Payment Entry","Purchase Invoice","Material Request","Purchase Receipt", "Purchase Order","Journal Entry") :{
      "before_validate": "shanti_education.shanti_education.doc_event.workflow_state_change.before_validate",
  }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"shanti_education.tasks.all"
#	],
#	"daily": [
#		"shanti_education.tasks.daily"
#	],
#	"hourly": [
#		"shanti_education.tasks.hourly"
#	],
#	"weekly": [
#		"shanti_education.tasks.weekly"
#	],
#	"monthly": [
#		"shanti_education.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "shanti_education.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "shanti_education.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "shanti_education.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["shanti_education.utils.before_request"]
# after_request = ["shanti_education.utils.after_request"]

# Job Events
# ----------
# before_job = ["shanti_education.utils.before_job"]
# after_job = ["shanti_education.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"shanti_education.auth.validate"
# ]
