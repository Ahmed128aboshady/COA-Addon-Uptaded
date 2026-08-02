import { Chatter } from "@mail/chatter/web_portal/chatter";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { onMounted, useState } from "@odoo/owl";

patch(Chatter.prototype, {
  setup() {
    super.setup();
    
    // 1. استخدام this.env.services لتجنب انهيار النظام (Crash) إذا كانت الخدمة غير متوفرة
    this.orm = this.env.services.orm || null;
    this.userService = this.env.services.user || null;
    
    this.access = useState({hide_log_notes: false, hide_send_mail: false, hide_schedule_activity: false});
    
    onMounted(async () => {
      // 2. إذا كنا في واجهة (مثل البورتال) لا تحتوي على خدمات المستخدم أو قاعدة البيانات، يتم إيقاف التنفيذ هنا بأمان
      if (!this.userService || !this.orm) {
          return;
      }

      var self = this;
      let model = this.props.threadModel;
      
      // 3. استخدام this.userService بدلاً من this.user
      let cid = this.userService.activeCompany?.id || this.userService.company?.id; 
      let userId = this.userService.userId;

      if (cid && model && userId) {
        await this.orm.call("access.management", "get_chatter_hide_details", [userId, cid, model])
          .then(function (result) {
            Object.assign(self.access, result);
          });
      }
    });
  },
});