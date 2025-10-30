

#开票操作
OPERATION_LOG_RECEIPT_ADD = {
    "type": "receipt:add",
    "desc": "申请开票",
}

OPERATION_LOG_RECEIPT_EDIT = {
    "type": "receipt:edit",
    "desc": "编辑开票",
}


OPERATION_LOG__RECEIPT_DO = {
    "type": "receipt:do",
    "desc": "完成开票",
}
OPERATION_LOG__RECEIPT_REJECT = {
    "type": "receipt:reject",
    "desc": "拒绝开票",
}

#要优惠操作
OPERATION_LOG_DISCOUNT_ADD = {
    "type": "discount:add",
    "desc": "申请优惠",
}

OPERATION_LOG_DISCOUNT_communicated = {
    "type": "discount:communicated",
    "desc": "已沟通优惠",
}

OPERATION_LOG_DISCOUNT_edit = {
    "type": "discount:edit",
    "desc": "优惠编辑",
}

OPERATION_LOG_DISCOUNT_DO = {
    "type": "discount:do",
    "desc": "完成优惠",
}

OPERATION_LOG_DISCOUNT_REJECT = {
    "type": "discount:reject",
    "desc": "拒绝优惠",
}

OPERATION_LOG_DISCOUNT_ABANDONS = {
    "type": "discount:ABANDONS",
    "desc": "房东放弃优惠",
}

OPERATION_LOG_DISCOUNT_PROCESS = {
    "type": "discount:reject",
    "desc": "提交books",
}

OPERATION_LOG_DISCOUNT_DELETE = {
    "type": "discount:delete",
    "desc": "删除优惠",
}

OPERATION_LOG_DISCOUNT_MOVE = {
    "type": "discount:move",
    "desc": "移动优惠",
}

#数据调整操作
OPERATION_LOG_SPECIAL_APPLY_ADD = {
    "type": "special_apply:add",
    "desc": "申请数据调整",
}
OPERATION_LOG_SPECIAL_APPLY_DO = {
    "type": "special_apply:do",
    "desc": "完成数据调整",
}

OPERATION_LOG_SPECIAL_EDIT = {
    "type": "special_apply:edit",
    "desc": "编辑数据调整",
}

OPERATION_LOG_SPECIAL_DELETE  = {
    "type": "special_apply:delete",
    "desc": "编辑数据调整",
}

OPERATION_LOG_SPECIAL_MOVE  = {
    "type": "special_apply:move",
    "desc": "移动数据调整",
}


OPERATION_LOG_SPECIAL_APPLY_REJECT = {
    "type": "special_apply:reject",
    "desc": "拒绝数据调整",
}

#账号注销
OPERATION_LOG_ACCOUNT_DELETION_ADD = {
    "type": "account_deletion:add",
    "desc": "申请账号注销",
}
OPERATION_LOG_ACCOUNT_DELETION_DO = {
    "type": "account_deletion:do",
    "desc": "完成账号注销",
}
OPERATION_LOG_ACCOUNT_DELETION_REJECT = {
    "type": "account_deletion:reject",
    "desc": "拒绝账号注销",
}


#vip费用退款
OPERATION_LOG_VIP_REFUND_ADD = {
    "type": "vip_refund:add",
    "desc": "申请vip费用退款",
}
OPERATION_LOG_VIP_REFUND_DO = {
    "type": "vip_refund:do",
    "desc": "完成vip费用退款",
}
OPERATION_LOG_VIP_REFUND_REJECT = {
    "type": "vip_refund:reject",
    "desc": "拒绝vip费用退款",
}

OPERATION_LOG_VIP_REFUND_DELETE = {
    "type": "vip_refund:delete",
    "desc": "删除vip费用退款",
}

OPERATION_LOG_VIP_REFUND_EDIT = {
    "type": "vip_refund:edit",
    "desc": "编辑vip费用退款",
}



#申请店主更换
OPERATION_LOG_SHOP_OWNER_CHANGE_ADD = {
    "type": "shop_owner_change:add",
    "desc": "申请店主更换",
}


#编辑店主更换
OPERATION_LOG_SHOP_OWNER_CHANGE_EDIT = {
    "type": "shop_owner_change:edit",
    "desc": "编辑店主更换",
}

OPERATION_SHOP_OWNER_CHANGE_DELETE = {
    "type": "shop_owner_change:delete",
    "desc": "删除店主更换",
}




#合作推广
OPERATION_LOG_COOP_EX_ADD = {
    "type": "coop_ex:add",
    "desc": "添加合作推广",
}
OPERATION_LOG_COOP_EX_DO = {
    "type": "coop_ex:do",
    "desc": "编辑合作推广",
}

#售前进度
OPERATION_LOG_PRESALES_PROGRESS_DO = {
    "type": "presales_progress:do",
    "desc": "更新售前进度",
}

OPERATION_LOG_CLAIM_PRESALES = {
    "type": "presales_progress:claim",
    "desc": "认领",
}

OPERATION_LOG_PRESALES_PROGRESS_UPDATE = {
    "type": "presales_progress:edit",
    "desc": "编辑",
}


#添加客户运营人员
OPERATION_LOG_OPERATING_SUB_COMPANY_ADD = {
    "type": "operating_sub_company:add",
    "desc": "添加客户运营人员",
}

#编辑客户运营人员
OPERATION_LOG_OPERATING_SUB_COMPANY_EDIT = {
    "type": "operating_sub_company:edit",
    "desc": "编辑客户运营人员",
}

#删除客户运营人员
OPERATION_LOG_OPERATING_SUB_COMPANY_DEL = {
    "type": "operating_sub_company:del",
    "desc": "删除客户运营人员",
}


#账号操作
OPERATION_LOG_ACCOUNT_ADD = {
    "type": "account:add",
    "desc": "添加账号",
}
OPERATION_LOG_ACCOUNT_DELETE = {
    "type": "account:delete",
    "desc": "删除账号",
}
OPERATION_LOG_ACCOUNT_SETROLE = {
    "type": "account:setrole",
    "desc": "设置角色",
}
OPERATION_LOG_ACCOUNT_MODIFY_PASSWORD = {
    "type": "account:modifypassword",
    "desc": "修改密码",
}


#账号操作
OPERATION_LOG_ADD_API = {
    "type": "api:add",
    "desc": "创建接口",
}

#更新奖励金
OPERATION_LOG_CODE_MODIFY_UPDATE = {
    "type": "code_modify:update",
    "desc": "更新邀请码",
}

#删除校色
OPERATION_LOG_ROLE_DEL = {
    "type": "ROLE:DEL",
    "desc": "删除校色",
}

#初始化订单操作
OPERATION_LOG_INITIAL_ORDER_SEND = {
    "type": "initial_order:send",
    "desc": "初始化订单操作",
}
