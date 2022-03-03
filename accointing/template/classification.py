from enum import Enum


class DepositClassification(str, Enum):
    ADD_FUNDS = "add funds"
    AIRDROP = "airdrop"
    BOUNTY = "bounty"
    GAMBLING_INCOME = "gambling_income"
    GIFT_RECEIVED = "gift_received"
    HARD_FORK = "hard_fork"
    IGNORED = "ignored"
    INCOME = "income"
    LENDING_INCOME = "lending_income"
    LIQUIDITY_POOL = "liquidity_pool"
    MARGIN_GAIN = "margin_gain"
    MASTER_NODE = "master_node"
    MINED = "mined"
    STAKED = "staked"


class WithdrawClassification(str, Enum):
    REMOVE_FUNDS = "remove funds"
    PAYMENT_FEE = "payment fee"
    GAMBLING_USED = "gambling_used"
    GIFT_SENT = "gift_sent"
    IGNORED = "ignored"
    INTEREST_PAID = "interest_paid"
    LENDING = "lending"
    LOST = "lost"
    MARGIN_FEE = "margin_fee"
    MARGIN_LOSS = "margin_loss"
    PAYMENT = "payment"
