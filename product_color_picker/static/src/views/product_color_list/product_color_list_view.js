/** @odoo-module **/

import { registry } from "@web/core/registry";
import { listView } from "@web/views/list/list_view";
import { ProductColorListRenderer } from "./product_color_list_renderer";

export const productColorListView = {
    ...listView,
    Renderer: ProductColorListRenderer,
};

registry.category("views").add("product_color_list", productColorListView);
