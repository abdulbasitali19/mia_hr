# Copyright (c) 2024, Abdul Basit Ali and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import today, getdate


class LeaveApplicationDocument(Document):
    def validate(self):
        self.calculate_eligibility()

    def calculate_eligibility(self):
        year_starting_date = getdate("01-01-2024")
        request_from_date = getdate(self.request_from_date)
        request_to_date = getdate(self.request_to_date)
        date_of_join = getdate(self.date_of_join)

        if date_of_join >= year_starting_date:
            year_starting_date = self.date_of_join  

        if self.eligible_til_date and not None:
            self.total_eligibility = (request_from_date - year_starting_date).days * 0.057
            self.total_request_days = (request_to_date - request_from_date).days
            self.total_paid_leaves = int(self.eligible_til_date) + self.total_eligibility
            self.total_unpaid_leaves = round(self.total_request_days - self.total_paid_leaves, 2)
        else:
            if has_completed_one_year(self.date_of_join):
                self.total_eligibility = (request_from_date - year_starting_date).days * 0.057
                self.total_request_days = (request_from_date - request_to_date).days
                self.total_paid_leaves = self.total_eligibility
                self.total_unpaid_leaves = self.total_request_days - self.total_paid_leaves
            else:
                frappe.throw("You haven't completed one year in the company")


def has_completed_one_year(joining_date_str):
    current_date_time = today()
    time_difference = getdate(current_date_time) - getdate(joining_date_str)
    return time_difference.days >= 365
