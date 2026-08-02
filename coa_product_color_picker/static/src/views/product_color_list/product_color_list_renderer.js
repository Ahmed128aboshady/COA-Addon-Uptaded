/** @odoo-module **/

import { ListRenderer } from "@web/views/list/list_renderer";

export class ProductColorListRenderer extends ListRenderer {
    static template = "web.ListRenderer";

    getRowClass(record) {
        const classNames = super.getRowClass(record);
        const colorIndex = record.data.color;
        if (colorIndex) {
            return `${classNames} o_product_list_color_${colorIndex}`;
        }
        return classNames;
    }
}
