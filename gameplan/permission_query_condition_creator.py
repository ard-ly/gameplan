# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version
import frappe
from frappe import _
from frappe.utils import getdate, cstr


def get_permission_query_conditions(user, doctype):
    if doctype == "GP User Profile":
        return get_userprofile_perm(user, doctype)
    elif doctype == "GP Team":
        return get_team_perm(user, doctype)
    elif doctype == "GP Project":
        return get_project_perm(user, doctype)
    elif doctype == "GP Task":
        return get_task_perm(user, doctype)
    elif doctype == "GP Discussion":
        return get_discussion_perm(user, doctype)
    elif doctype == "GP Discussion":
        return get_discussion_perm(user, doctype)



def get_userprofile_perm(user, doctype):
    owned_docs = frappe.get_all(doctype,filters={"owner":frappe.session.user})

    # Get documents shared with the user
    shared_docs = frappe.get_all("DocShare",
                             filters={"share_doctype": doctype},
                             or_filters=[{"user": frappe.session.user}, {"user": ""}],
                             fields=["share_name"])

    userprofiles = frappe.get_all(doctype,
                                    filters={"user": frappe.session.user},
                                    fields=["name"])

    allowed_docs_list = []
    for owned_doc in owned_docs:
        allowed_docs_list.append(str(owned_doc.name))

    for shared_doc in shared_docs:
        allowed_docs_list.append(str(shared_doc.share_name))

    for userprofile in userprofiles:
        allowed_docs_list.append(str(userprofile.name))


    if frappe.session.user == "Administrator":
        return

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "`tab{doctype}`.name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple), doctype= doctype)
   



def get_team_perm(user, doctype):
    owned_docs = frappe.get_all(doctype,filters={"owner":frappe.session.user})

    # Get documents shared with the user
    shared_docs = frappe.get_all("DocShare",
                             filters={"share_doctype": doctype},
                             or_filters=[{"user": frappe.session.user}, {"user": ""}],
                             fields=["share_name"])

    members = frappe.get_all("GP Member",
                                    filters={"parenttype": doctype,
                                             "user": frappe.session.user},
                                    fields=["parent"])

    allowed_docs_list = []
    for owned_doc in owned_docs:
        allowed_docs_list.append(owned_doc.name)

    for shared_doc in shared_docs:
        allowed_docs_list.append(shared_doc.share_name)

    for member in members:
        allowed_docs_list.append(member.parent)


    if frappe.session.user == "Administrator":
        return

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple))



def get_project_perm(user, doctype):
    owned_docs = frappe.get_all(doctype,filters={"owner":frappe.session.user})

    # Get documents shared with the user
    shared_docs = frappe.get_all("DocShare",
                             filters={"share_doctype": doctype},
                             or_filters=[{"user": frappe.session.user}, {"user": ""}],
                             fields=["share_name"])

    members = frappe.get_all("GP Member",
                                    filters={"parenttype": doctype,
                                             "user": frappe.session.user},
                                    fields=["parent"])

    allowed_docs_list = []
    for owned_doc in owned_docs:
        allowed_docs_list.append(owned_doc.name)

    for shared_doc in shared_docs:
        allowed_docs_list.append(shared_doc.share_name)

    for member in members:
        allowed_docs_list.append(member.parent)


    if frappe.session.user == "Administrator":
        return

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "`tab{doctype}`.name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple), doctype= doctype)
   
                        


def get_task_perm(user, doctype):
    owned_docs = frappe.get_all(doctype,filters={"owner":frappe.session.user})

    # Get documents shared with the user
    shared_docs = frappe.get_all("DocShare",
                             filters={"share_doctype": doctype},
                             or_filters=[{"user": frappe.session.user}, {"user": ""}],
                             fields=["share_name"])

    members = frappe.get_all("GP Task",
                                    filters={"assigned_to": frappe.session.user},
                                    fields=["name"])

    allowed_docs_list = []
    for owned_doc in owned_docs:
        allowed_docs_list.append(str(owned_doc.name))

    for shared_doc in shared_docs:
        allowed_docs_list.append(str(shared_doc.share_name))

    for member in members:
        allowed_docs_list.append(str(member.name))


    if frappe.session.user == "Administrator":
        return

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "`tab{doctype}`.name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple), doctype= doctype)
   



def get_discussion_perm(user, doctype):
    owned_docs = frappe.get_all(doctype,filters={"owner":frappe.session.user})

    # Get documents shared with the user
    shared_docs = frappe.get_all("DocShare",
                             filters={"share_doctype": doctype},
                             or_filters=[{"user": frappe.session.user}, {"user": ""}],
                             fields=["share_name"])

    allowed_teams = frappe.db.sql_list("select parent from `tabGP Member` where parenttype='GP Team' and user='{0}'".format(frappe.session.user))
    allowed_projects = frappe.db.sql_list("select parent from `tabGP Member` where parenttype='GP Project' and user='{0}'".format(frappe.session.user))
    
    discussions = frappe.get_all(
        doctype,
        filters={
            "team": ["in", allowed_teams],
            "project": ["in", allowed_projects]
        },
        fields=["name"]
    )


    allowed_docs_list = []
    for owned_doc in owned_docs:
        allowed_docs_list.append(str(owned_doc.name))

    for shared_doc in shared_docs:
        allowed_docs_list.append(str(shared_doc.share_name))

    for discussion in discussions:
        allowed_docs_list.append(str(discussion.name))


    if frappe.session.user == "Administrator":
        return

    allowed_docs_tuple = tuple(allowed_docs_list)
    return "`tab{doctype}`.name in ('{allowed_list}')".format(allowed_list="','".join(allowed_docs_tuple), doctype= doctype)
   

