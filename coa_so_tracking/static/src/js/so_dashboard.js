/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

// ─── Date helpers ─────────────────────────────────────────────────────────────
function _fmt(d) {
    return [
        d.getFullYear(),
        String(d.getMonth() + 1).padStart(2, "0"),
        String(d.getDate()).padStart(2, "0"),
    ].join("-");
}
function _firstOfMonth() {
    const d = new Date();
    return _fmt(new Date(d.getFullYear(), d.getMonth(), 1));
}
function _today() { return _fmt(new Date()); }

// ─── Component ────────────────────────────────────────────────────────────────
export class CoaSoTrackingDashboard extends Component {
    static template = "coa_so_tracking.Dashboard";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");

        this.filters = useState({
            dateFrom: _firstOfMonth(),
            dateTo:   _today(),
            state:    "all",
        });

        this.state = useState({
            loading:     false,
            data:        [],
            expandedSOs: {},   // { [soId]: boolean }
            error:       null,
        });

        onWillStart(() => this.loadData());
    }

    // ── Data loading ──────────────────────────────────────────────────────────
    async loadData() {
        this.state.loading     = true;
        this.state.error       = null;
        this.state.expandedSOs = {};
        try {
            const data = await this.orm.call(
                "sale.order",
                "get_so_tracking_data",
                [this.filters.dateFrom, this.filters.dateTo, this.filters.state]
            );
            this.state.data = data;
        } catch (e) {
            const msg =
                (e && e.data && e.data.message) ||
                (e && e.message) ||
                "حدث خطأ أثناء تحميل البيانات";
            this.state.error = msg;
            this.state.data  = [];
        } finally {
            this.state.loading = false;
        }
    }

    async applyFilters() { await this.loadData(); }

    // ── Expand / collapse ─────────────────────────────────────────────────────
    toggleSO(soId) {
        this.state.expandedSOs[soId] = !this.state.expandedSOs[soId];
    }
    isExpanded(soId) { return !!this.state.expandedSOs[soId]; }

    // ── Formatting ────────────────────────────────────────────────────────────
    fmtQty(v) {
        const n = v || 0;
        // Show up to 2 decimals, strip trailing zeros
        return Number(n.toFixed(2)).toLocaleString("en-US", {
            minimumFractionDigits: 0,
            maximumFractionDigits: 2,
        });
    }

    pct(done, total) {
        if (!total) return 0;
        return Math.min(Math.round((done / total) * 100), 100);
    }

    stateLabel(s) {
        const map = {
            sale: "مؤكد", done: "مغلق",
            cancel: "ملغي", draft: "مسودة", sent: "مرسل",
        };
        return map[s] || s;
    }

    stateBadgeClass(s) {
        const map = {
            sale: "coa_badge_sale", done: "coa_badge_done",
            cancel: "coa_badge_cancel", draft: "coa_badge_draft",
            sent: "coa_badge_sent",
        };
        return map[s] || "";
    }

    // ── Excel export ──────────────────────────────────────────────────────────
    async exportExcel() {
        this.state.loading = true;
        this.state.error   = null;
        try {
            const result = await this.orm.call(
                "sale.order",
                "export_so_tracking_excel",
                [this.filters.dateFrom, this.filters.dateTo, this.filters.state]
            );
            // Decode base64 → Blob → download
            const byteChars = atob(result.file_data);
            const bytes = new Uint8Array(byteChars.length);
            for (let i = 0; i < byteChars.length; i++) {
                bytes[i] = byteChars.charCodeAt(i);
            }
            const blob = new Blob([bytes], {
                type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            });
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href     = url;
            a.download = result.filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        } catch (e) {
            const msg =
                (e && e.data && e.data.message) ||
                (e && e.message) ||
                "فشل في تصدير Excel — يرجى المحاولة مجدداً";
            this.state.error = msg;
        } finally {
            this.state.loading = false;
        }
    }
}

registry.category("actions").add("coa_so_tracking_dashboard", CoaSoTrackingDashboard);
