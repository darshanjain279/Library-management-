# Copyright (c) 2022, Darshan Jain and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus


class LibraryTransaction(Document):
    #D. Starting counter of number of issued.
    def before_submit(self):
        article = frappe.get_doc("Article", self.article)
        if self.type == "Issue":
            self.validate_issue()
            self.validate_maximum_limit()
            # set the article status to be Issued
            #D. Removing the previous changing of status to issued at once since now there are a higher number of articles.
            """article = frappe.get_doc("Article", self.article)
            article.status = "Issued"
            article.save()"""
            article.number += 1
            article.available -= 1
            if article.number == article.quantity:
                article.status = "Issued"
                frappe.throw("Article is not available currently")
            article.save()

        elif self.type == "Return":
            #D. I have switched off the validate return since There are more items of each article and it need not be in issued state like a single piece, to be returned.
            #self.validate_return()
            # set the article status to be Available
            article.status = "Available"
            article.number -= 1
            article.available += 1
            article.save()
#        """ if self.returned == "1":
 #          article.number -= 1
  #          article.available += 1
   #         article.save() """
    #    """elif self.type == "Return":
     #       #D. I have switched off the validate return since There are more items of each article and it need not be in issued state like a single piece, to be returned.
      #      #self.validate_return()
       #     # set the article status to be Available
        #    article.status = "Available"
         #   article.number -= 1
          #  article.available += 1
           # article.save()"""
           

    def validate_issue(self):
        self.validate_membership()
        article = frappe.get_doc("Article", self.article)
        # article cannot be issued if it is already issued
        if article.status == "Issued":
            frappe.throw("Article is already issued by other members")
    
        """def validate_return(self):
        article = frappe.get_doc("Article", self.article)
        # article cannot be returned if it is not issued first
        if article.status == "Available":
            frappe.throw("Article cannot be returned without being issued first")"""

    def validate_maximum_limit(self):
        max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
        count = frappe.db.count(
            "Library Transaction",
            {"library_member": self.library_member, "type": "Issue", "docstatus": DocStatus.submitted()},
        )
        if count >= max_articles:
            frappe.throw("Maximum limit reached for issuing articles")

    def validate_membership(self):
        # check if a valid membership exist for this library member
        valid_membership = frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "docstatus": DocStatus.submitted(),
                "from_date": ("<", self.date),
                "to_date": (">", self.date),
            },
        )
        if not valid_membership:
            frappe.throw("The member does not have a valid membership")
            
    """def calculate_availability(self):
        #This calcultes both available and the number of issued.
        article = frappe.get_doc("Article", self.article)
        article.available = article.quantity - article.number""" 
        #if self.returned.
    def check_returned(self):
        if self.returned == "Yes":
            article.number -= 2
            article.available += 2
