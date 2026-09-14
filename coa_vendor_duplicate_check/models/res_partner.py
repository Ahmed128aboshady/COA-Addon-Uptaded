# -*- coding: utf-8 -*-
import re

from odoo import _, api, models
from odoo.exceptions import ValidationError

# Values that ir.config_parameter may store for a boolean setting.
_TRUE_VALUES = ("1", "true", "True", "TRUE", "yes")

# How many trailing digits of a phone number are compared. This absorbs
# country-code / leading-zero variations (e.g. +20 100 123 4567 == 0100 123 4567).
_PHONE_SIGNIFICANT_DIGITS = 9


class ResPartner(models.Model):
    _inherit = "res.partner"

    # ------------------------------------------------------------------
    # Configuration
    # ------------------------------------------------------------------
    @api.model
    def _vdc_config(self):
        get = self.env["ir.config_parameter"].sudo().get_param
        return {
            "mode": get("coa_vendor_duplicate_check.mode", "block"),
            "check_email": get("coa_vendor_duplicate_check.check_email", "True") in _TRUE_VALUES,
            "check_phone": get("coa_vendor_duplicate_check.check_phone", "True") in _TRUE_VALUES,
            "scope": get("coa_vendor_duplicate_check.scope", "vendor"),
        }

    # ------------------------------------------------------------------
    # Normalisation helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _vdc_normalize_email(value):
        if not value:
            return False
        return value.strip().lower() or False

    @staticmethod
    def _vdc_normalize_phone(value):
        """Return a comparable key for a phone number.

        Removes every non-digit character, drops leading trunk zeros, then keeps
        the last significant digits so different formats of the same number match.
        """
        if not value:
            return False
        digits = re.sub(r"\D", "", value)
        if not digits:
            return False
        trimmed = digits.lstrip("0") or digits
        if len(trimmed) >= _PHONE_SIGNIFICANT_DIGITS:
            return trimmed[-_PHONE_SIGNIFICANT_DIGITS:]
        return trimmed

    def _vdc_ids_to_exclude(self):
        """Return (record_id, commercial_id) as ints/False, safe in domains.

        Works for saved records (constraint) and NewId records (onchange).
        """
        origin = self._origin if self._origin else self
        res_id = origin.id if isinstance(origin.id, int) else False
        commercial = origin.commercial_partner_id
        commercial_id = commercial.id if isinstance(commercial.id, int) else False
        return res_id, commercial_id

    # ------------------------------------------------------------------
    # Detection
    # ------------------------------------------------------------------
    def _vdc_find_duplicates(self, config=None):
        """Return {field_name: matched_partners} for the current record."""
        self.ensure_one()
        config = config or self._vdc_config()

        check_email = config["check_email"] and bool(self.email)
        check_phone = config["check_phone"] and bool(self.phone)
        if not (check_email or check_phone):
            return {}

        res_id, commercial_id = self._vdc_ids_to_exclude()
        domain = []
        if res_id:
            domain.append(("id", "!=", res_id))
        if commercial_id:
            # Do not flag the vendor's own child contacts / parent company.
            domain.append(("commercial_partner_id", "!=", commercial_id))
        if config["scope"] == "vendor":
            domain.append(("supplier_rank", ">", 0))

        field_domain = []
        if check_email:
            field_domain.append(("email", "!=", False))
        if check_phone:
            field_domain.append(("phone", "!=", False))
        if len(field_domain) == 2:
            domain += ["|"] + field_domain
        else:
            domain += field_domain

        candidates = self.env["res.partner"].search(domain)
        result = {}

        if check_email:
            key = self._vdc_normalize_email(self.email)
            matches = candidates.filtered(
                lambda p: self._vdc_normalize_email(p.email) == key
            )
            if matches:
                result["email"] = matches

        if check_phone:
            key = self._vdc_normalize_phone(self.phone)
            matches = candidates.filtered(
                lambda p: self._vdc_normalize_phone(p.phone) == key
            )
            if matches:
                result["phone"] = matches

        return result

    # ------------------------------------------------------------------
    # Messages (Arabic)
    # ------------------------------------------------------------------
    def _vdc_build_message(self, duplicates):
        self.ensure_one()
        labels = {"email": _("البريد الإلكتروني"), "phone": _("رقم الهاتف / الجوال")}
        values = {"email": self.email or "", "phone": self.phone or ""}
        lines = []
        for field_name, partners in duplicates.items():
            names = "، ".join(partners.mapped("display_name")[:5])
            extra = ""
            if len(partners) > 5:
                extra = _(" و%(n)s غيرهم", n=len(partners) - 5)
            lines.append(_(
                "%(label)s «%(value)s» مُسجّل مسبقًا لدى: %(names)s%(extra)s",
                label=labels[field_name],
                value=values[field_name],
                names=names,
                extra=extra,
            ))
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Guards
    # ------------------------------------------------------------------
    @api.constrains("email", "phone")
    def _vdc_check_duplicates(self):
        config = self._vdc_config()
        if config["mode"] != "block":
            return
        for partner in self:
            duplicates = partner._vdc_find_duplicates(config)
            if duplicates:
                raise ValidationError(
                    _("تعذّر الحفظ لوجود تكرار في بيانات المورد:\n\n%(details)s",
                      details=partner._vdc_build_message(duplicates))
                )

    @api.onchange("email", "phone")
    def _vdc_onchange_warn(self):
        config = self._vdc_config()
        duplicates = self._vdc_find_duplicates(config)
        if duplicates:
            return {
                "warning": {
                    "title": _("تنبيه: احتمال تكرار بيانات"),
                    "message": self._vdc_build_message(duplicates),
                }
            }
