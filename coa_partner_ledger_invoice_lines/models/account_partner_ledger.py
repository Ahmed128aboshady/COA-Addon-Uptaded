# -*- coding: utf-8 -*-

from odoo import models, api
from odoo.tools import SQL
import logging

_logger = logging.getLogger(__name__)


class PartnerLedgerCustomHandler(models.AbstractModel):
    """
    Extension of Partner Ledger Report Handler to display invoice lines
    as expandable sub-lines under each invoice/bill entry.
    """
    _inherit = 'account.partner.ledger.report.handler'

    # ============================================================
    # SQL QUERY EXTENSIONS
    # ============================================================

    def _get_additional_column_aml_values(self):
        """
        Add move_id and move_type to the SQL query for invoice lines lookup.

        These additional columns allow us to:
        - Identify the move (invoice) associated with each line
        - Check the move type to determine if it has invoice lines
        - Access invoice_line_ids efficiently
        """
        parent_result = super()._get_additional_column_aml_values()

        # Build the additional columns SQL
        additional_sql = "account_move_line.move_id AS move_id, account_move.move_type AS move_type,"

        # Append to parent result if it exists
        if parent_result and str(parent_result).strip():
            return SQL("%s %s", parent_result, SQL(additional_sql))
        else:
            return SQL(additional_sql)

    # ============================================================
    # MOVE LINE RENDERING
    # ============================================================

    def _get_report_line_move_line(
        self, options, aml_query_result, partner_line_id, init_bal_by_col_group, level_shift=0
    ):
        """
        Override to make invoice/bill lines unfoldable.

        This method checks if the move line belongs to an invoice/bill that has
        invoice_line_ids. If yes, it marks the line as unfoldable and sets the
        custom expand function.

        Args:
            options: Report options
            aml_query_result: SQL query result dictionary
            partner_line_id: Parent partner line ID
            init_bal_by_col_group: Initial balance by column group
            level_shift: Level adjustment for prefix groups

        Returns:
            dict: Line dictionary with unfoldable properties if applicable
        """
        # Get the base line from parent
        line_dict = super()._get_report_line_move_line(
            options, aml_query_result, partner_line_id, init_bal_by_col_group, level_shift
        )

        # Check if this move line has invoice lines to display
        move_id = aml_query_result.get('move_id')
        move_type = aml_query_result.get('move_type')

        # Supported move types: invoices and bills (including refunds)
        supported_types = ('out_invoice', 'out_refund', 'in_invoice', 'in_refund')

        if move_id and move_type in supported_types:
            try:
                # Check if the move has invoice lines
                move = self.env['account.move'].browse(move_id)
                if move.exists() and move.invoice_line_ids:
                    # Filter to get only product lines (exclude sections, notes)
                    product_lines = move.invoice_line_ids.filtered(
                        lambda l: l.display_type == 'product'
                    )

                    if product_lines:
                        # Make the line unfoldable
                        line_dict['unfoldable'] = True
                        line_dict['unfolded'] = line_dict['id'] in options.get('unfolded_lines', [])
                        line_dict['expand_function'] = '_report_expand_unfoldable_line_move_line_invoice_lines'

                        _logger.debug(
                            f"[Partner Ledger Invoice Lines] Made move line {move_id} unfoldable "
                            f"with {len(product_lines)} product lines"
                        )
            except Exception as e:
                _logger.error(
                    f"[Partner Ledger Invoice Lines] Error checking invoice lines for move {move_id}: {e}"
                )

        return line_dict

    # ============================================================
    # EXPAND FUNCTION FOR INVOICE LINES
    # ============================================================

    def _report_expand_unfoldable_line_move_line_invoice_lines(
        self, line_dict_id, groupby, options, progress, offset, unfold_all_batch_data=None
    ):
        """
        Custom expand function to display invoice lines as sub-lines.

        This function is called when the user clicks the expand icon on an invoice line.
        It retrieves all invoice_line_ids from the move and creates sub-lines for each product.

        Args:
            line_dict_id: The line ID to expand (format: account.report~X|res.partner~Y|account.move.line~Z)
            groupby: Groupby field (not used here)
            options: Report options
            progress: Progress for load_more (not used here as we load all lines at once)
            offset: Offset for pagination (not used here)
            unfold_all_batch_data: Batch data for unfold_all (not implemented yet)

        Returns:
            dict: Dictionary with 'lines', 'offset_increment', 'has_more', 'progress'
        """
        _logger.info(f"[Partner Ledger Invoice Lines] Expanding line: {line_dict_id}")

        # Parse the line_id to extract the move line ID
        report = self.env['account.report'].browse(options['report_id'])

        try:
            # Get the model and record ID from the line_id
            model, aml_id = report._get_model_info_from_id(line_dict_id)

            if model != 'account.move.line':
                _logger.warning(
                    f"[Partner Ledger Invoice Lines] Unexpected model in line_id: {model}"
                )
                return {
                    'lines': [],
                    'offset_increment': 0,
                    'has_more': False,
                    'progress': progress
                }

            if not aml_id:
                _logger.warning(
                    f"[Partner Ledger Invoice Lines] Could not extract aml_id from line_id: {line_dict_id}"
                )
                return {
                    'lines': [],
                    'offset_increment': 0,
                    'has_more': False,
                    'progress': progress
                }

            # Get the parent level from the line_id structure
            # Level calculation: account.report (0) | res.partner (1) | account.move.line (3)
            # So invoice lines will be level 4
            parent_level = 3

            # Check if there are prefix groups in the line_id (affects level)
            parsed_line_id = report._parse_line_id(line_dict_id)
            prefix_groups_count = sum(
                1 for markup, dummy1, dummy2 in parsed_line_id
                if isinstance(markup, dict) and 'groupby_prefix_group' in markup
            )
            level_shift = prefix_groups_count * 2
            parent_level += level_shift

            # Create the invoice line sub-lines
            lines = self._create_invoice_line_sublines(
                options, aml_id, line_dict_id, parent_level
            )

            _logger.info(
                f"[Partner Ledger Invoice Lines] Created {len(lines)} sub-lines for aml_id {aml_id}"
            )

            return {
                'lines': lines,
                'offset_increment': len(lines),
                'has_more': False,
                'progress': progress
            }

        except Exception as e:
            _logger.error(
                f"[Partner Ledger Invoice Lines] Error expanding line {line_dict_id}: {e}",
                exc_info=True
            )
            return {
                'lines': [],
                'offset_increment': 0,
                'has_more': False,
                'progress': progress
            }

    # ============================================================
    # SUB-LINES CREATION
    # ============================================================

    def _create_invoice_line_sublines(self, options, aml_id, parent_line_id, parent_level):
        """
        Create sub-lines for invoice line items.

        This method:
        1. Retrieves the account.move.line record
        2. Gets the associated move and its invoice_line_ids
        3. Filters to only product lines
        4. Creates a sub-line dictionary for each invoice line
        5. Returns the list of sub-lines

        Args:
            options: Report options
            aml_id: Account move line ID
            parent_line_id: Parent line ID (the invoice line)
            parent_level: Parent line level (for proper indentation)

        Returns:
            list: List of sub-line dictionaries
        """
        sub_lines = []
        report = self.env['account.report'].browse(options['report_id'])

        # Get the account move line
        aml = self.env['account.move.line'].browse(aml_id)
        if not aml.exists():
            _logger.warning(
                f"[Partner Ledger Invoice Lines] Account move line {aml_id} does not exist"
            )
            return sub_lines

        # Get the move
        move = aml.move_id
        if not move:
            _logger.warning(
                f"[Partner Ledger Invoice Lines] Account move line {aml_id} has no move_id"
            )
            return sub_lines

        # Get invoice lines (only products, exclude sections and notes)
        invoice_lines = move.invoice_line_ids.filtered(
            lambda l: l.display_type == 'product'
        )

        if not invoice_lines:
            _logger.debug(
                f"[Partner Ledger Invoice Lines] Move {move.id} ({move.name}) has no product invoice lines"
            )
            return sub_lines

        _logger.debug(
            f"[Partner Ledger Invoice Lines] Processing {len(invoice_lines)} invoice lines "
            f"for move {move.name}"
        )

        # Create a sub-line for each invoice line
        for invoice_line in invoice_lines:
            try:
                # Build columns
                columns = self._build_invoice_line_columns(
                    options, invoice_line, aml, report
                )

                # Build line_id for the sub-line
                # We use the invoice_line.id as the record ID
                # markup='invoice_line' helps identify this as an invoice line sub-line
                subline_id = report._get_generic_line_id(
                    'account.move.line',
                    invoice_line.id,
                    parent_line_id=parent_line_id,
                    markup='invoice_line'
                )

                # Format the line name
                name = self._format_invoice_line_name(invoice_line)

                # Build the sub-line dictionary
                sub_line = {
                    'id': subline_id,
                    'parent_id': parent_line_id,
                    'name': name,
                    'columns': columns,
                    'level': parent_level + 1,
                    'unfoldable': False,
                    'unfolded': False,
                    'caret_options': False,  # No caret (not clickable)
                    'class': 'o_account_reports_invoice_line_subline',  # CSS class for styling
                }

                sub_lines.append(sub_line)

            except Exception as e:
                _logger.error(
                    f"[Partner Ledger Invoice Lines] Error creating sub-line for invoice line "
                    f"{invoice_line.id}: {e}",
                    exc_info=True
                )

        return sub_lines

    # ============================================================
    # HELPER METHODS
    # ============================================================

    def _build_invoice_line_columns(self, options, invoice_line, aml, report):
        """
        Build column dictionaries for an invoice line.

        This method creates the column values for each invoice line sub-line.
        The amounts are distributed into Debit/Credit/Balance columns based on
        the original move line's direction.

        Args:
            options: Report options
            invoice_line: Invoice line record (account.move.line)
            aml: Parent account move line (the receivable/payable line)
            report: Report recordset

        Returns:
            list: List of column dictionaries
        """
        columns = []

        # Determine the sign based on the parent move line
        # If parent has debit, invoice line amounts go to debit
        # If parent has credit, invoice line amounts go to credit
        is_debit = aml.debit > 0

        for column in options['columns']:
            col_expr_label = column['expression_label']
            value = None
            currency = False

            # Distribute amounts based on column type
            if col_expr_label == 'debit':
                value = invoice_line.price_subtotal if is_debit else 0
            elif col_expr_label == 'credit':
                value = invoice_line.price_subtotal if not is_debit else 0
            elif col_expr_label == 'balance':
                # Balance: positive if debit, negative if credit
                sign = 1 if is_debit else -1
                value = invoice_line.price_subtotal * sign
            elif col_expr_label == 'amount_currency':
                # Show amount_currency only if line currency differs from company currency
                if invoice_line.currency_id and invoice_line.currency_id != self.env.company.currency_id:
                    value = invoice_line.price_subtotal
                    currency = invoice_line.currency_id
                else:
                    value = ''  # Empty if same currency
            elif col_expr_label in ('amount', 'debit', 'credit'):
                # 'amount' is typically an alias for balance in some reports
                if col_expr_label == 'amount':
                    sign = 1 if is_debit else -1
                    value = invoice_line.price_subtotal * sign

            # Build the column dictionary using the report's method
            if value == '':
                # Empty string for amount_currency when not applicable
                columns.append(report._build_column_dict('', None))
            elif value is not None:
                columns.append(
                    report._build_column_dict(value, column, options=options, currency=currency)
                )
            else:
                # Empty column for other expression labels (date, journal, etc.)
                columns.append(report._build_column_dict(None, None))

        return columns

    def _format_invoice_line_name(self, invoice_line):
        """
        Format the display name for an invoice line.

        Creates a nicely formatted string showing:
        - Product code (if available)
        - Product name or line description
        - Quantity and unit price

        Format: "  ↳ [CODE] Product Name | Qty: X.XX × Price: Y.YY"

        Args:
            invoice_line: Invoice line record (account.move.line)

        Returns:
            str: Formatted line name
        """
        # Start with an indentation symbol
        name_parts = ["  ↳ "]

        # Add product code if available
        if invoice_line.product_id and invoice_line.product_id.default_code:
            name_parts.append(f"[{invoice_line.product_id.default_code}] ")

        # Add product name or line description
        product_name = invoice_line.product_id.name if invoice_line.product_id else invoice_line.name
        if product_name:
            name_parts.append(product_name)
        else:
            name_parts.append("(No description)")

        # Add quantity and price details
        if invoice_line.quantity and invoice_line.price_unit:
            name_parts.append(f" | Qty: {invoice_line.quantity:.2f} × {invoice_line.price_unit:.2f}")
        elif invoice_line.quantity:
            name_parts.append(f" | Qty: {invoice_line.quantity:.2f}")

        return ''.join(name_parts)
