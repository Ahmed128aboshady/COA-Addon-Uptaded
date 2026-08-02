/** @odoo-module **/
'use strict';

/**
 * Customer Portal Order — إدارة نموذج طلب الأوردر
 */

function initPortalOrder() {

    const tbody  = document.getElementById('order_lines_body');
    const addBtn = document.getElementById('add_line_btn');
    const form   = document.getElementById('portal_order_form');

    if (!tbody || !addBtn) return;   // مش في صفحة النموذج

    // ── مساعدات ─────────────────────────────────────────────────────────────────

    function updateRowNumbers() {
        tbody.querySelectorAll('.order-line-row').forEach((row, i) => {
            row.querySelector('.row-num').textContent = i + 1;
        });
    }

    function initRow(row) {
        const searchInput  = row.querySelector('.product-search-input');
        const productIdIn  = row.querySelector('.product-id-input');
        const productThumb = row.querySelector('.product-thumb');
        const dropdown     = row.querySelector('.product-dropdown');
        const removeBtn    = row.querySelector('.remove-line-btn');

        // إعادة تعيين القيم
        searchInput.value          = '';
        productIdIn.value          = '';
        productThumb.src           = '/web/static/img/placeholder.png';
        dropdown.style.display     = 'none';
        dropdown.innerHTML         = '';

        // ── بحث بـ debounce ──
        let timer;
        searchInput.addEventListener('input', function () {
            const term = this.value.trim();
            productIdIn.value = '';
            clearTimeout(timer);
            if (term.length < 2) {
                dropdown.style.display = 'none';
                return;
            }
            timer = setTimeout(() => searchProducts(term, row), 320);
        });

        // إخفاء الـ dropdown لما يضغط برا
        document.addEventListener('click', function (e) {
            if (!row.contains(e.target)) dropdown.style.display = 'none';
        });

        // ── حذف السطر ──
        removeBtn.addEventListener('click', function () {
            const rows = tbody.querySelectorAll('.order-line-row');
            if (rows.length > 1) {
                row.remove();
                updateRowNumbers();
            } else {
                searchInput.value  = '';
                productIdIn.value  = '';
                productThumb.src   = '/web/static/img/placeholder.png';
                row.querySelector('input[name="qty[]"]').value = 1;
            }
        });
    }

    // ── البحث عن المنتجات ────────────────────────────────────────────────────────

    function searchProducts(term, row) {
        const dropdown = row.querySelector('.product-dropdown');

        dropdown.innerHTML     = '<div class="list-group-item text-muted text-center py-2"><i class="fa fa-spinner fa-spin me-1"/>جاري البحث...</div>';
        dropdown.style.display = 'block';

        fetch('/my/order/product/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                jsonrpc: '2.0',
                method:  'call',
                id:      1,
                params:  { term },
            }),
        })
        .then(r => r.json())
        .then(data => {
            const products = data.result || [];
            dropdown.innerHTML = '';

            if (products.length === 0) {
                dropdown.innerHTML = '<div class="list-group-item text-muted text-center py-2">لا توجد نتائج</div>';
                return;
            }

            products.forEach(p => renderProductItem(p, row, dropdown));
        })
        .catch(() => {
            dropdown.innerHTML = '<div class="list-group-item text-danger text-center py-2"><i class="fa fa-exclamation-triangle me-1"/>حدث خطأ، حاول مرة ثانية</div>';
        });
    }

    function renderProductItem(product, row, dropdown) {
        const item       = document.createElement('a');
        item.href        = '#';
        item.className   = 'list-group-item list-group-item-action d-flex align-items-center gap-2 py-2 px-3';

        item.innerHTML = `
            <img src="${product.image_url}"
                 style="width:38px;height:38px;object-fit:cover;border-radius:6px;flex-shrink:0;border:1px solid #dee2e6;"
                 onerror="this.src='/web/static/img/placeholder.png'"/>
            <div class="flex-grow-1 min-width-0">
                <div class="fw-semibold text-truncate" style="font-size:.875rem;">${product.name}</div>
                <div class="d-flex gap-2 mt-1 flex-wrap">
                    ${product.code ? `<span class="badge bg-secondary" style="font-size:.7rem;">${product.code}</span>` : ''}
                    <span class="badge" style="background:#714B67;font-size:.7rem;">${product.price.toFixed(2)} / ${product.uom}</span>
                </div>
            </div>
        `;

        item.addEventListener('click', function (e) {
            e.preventDefault();
            selectProduct(product, row);
        });

        dropdown.appendChild(item);
    }

    function selectProduct(product, row) {
        row.querySelector('.product-search-input').value = product.name;
        row.querySelector('.product-id-input').value     = product.id;

        const thumb   = row.querySelector('.product-thumb');
        thumb.src     = product.image_url;
        thumb.onerror = () => { thumb.src = '/web/static/img/placeholder.png'; };

        row.querySelector('.product-dropdown').style.display = 'none';
    }

    // ── إضافة سطر جديد ────────────────────────────────────────────────────────────

    addBtn.addEventListener('click', function () {
        const template = tbody.querySelector('.order-line-row');
        const newRow   = template.cloneNode(true);
        tbody.appendChild(newRow);
        initRow(newRow);
        updateRowNumbers();
        newRow.querySelector('.product-search-input').focus();
    });

    // ── التحقق قبل الإرسال ────────────────────────────────────────────────────────

    if (form) {
        form.addEventListener('submit', function (e) {
            const selected = Array.from(
                form.querySelectorAll('.product-id-input')
            ).filter(i => i.value && parseInt(i.value) > 0);

            if (selected.length === 0) {
                e.preventDefault();
                let alertBox = form.querySelector('.js-form-error');
                if (!alertBox) {
                    alertBox = document.createElement('div');
                    alertBox.className = 'alert alert-danger js-form-error d-flex align-items-center gap-2 mb-3';
                    alertBox.innerHTML = '<i class="fa fa-exclamation-triangle fa-lg"/><span>يرجى اختيار منتج واحد على الأقل.</span>';
                    form.prepend(alertBox);
                }
                alertBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
                return;
            }

            const submitBtn = document.getElementById('submit_btn');
            if (submitBtn) {
                submitBtn.disabled   = true;
                submitBtn.innerHTML  = '<i class="fa fa-spinner fa-spin me-1"/>جاري الإرسال...';
            }
        });
    }

    // ── تهيئة الصف الأول ──────────────────────────────────────────────────────────

    const firstRow = tbody.querySelector('.order-line-row');
    if (firstRow) initRow(firstRow);
}

// ── تشغيل بعد تحميل الصفحة بغض النظر عن readyState ─────────────────────────────

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPortalOrder);
} else {
    initPortalOrder();
}
