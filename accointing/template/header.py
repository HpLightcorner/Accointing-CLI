import cattrs

HEADER = [
    "transactionType",
    "date",
    "inBuyAmount",
    "inBuyAsset",
    "outSellAmount",
    "outSellAsset",
    "feeAmount (optional)",
    "feeAsset (optional)",
    "classification (optional)",
    "operationId (optional)",
    "comments (optional)"
]


OVERRIDE = {
    "transaction_type": cattrs.gen.override(rename="transactionType"),
    "timestamp": cattrs.gen.override(rename="date"),
    "in_buy_amount": cattrs.gen.override(rename="inBuyAmount"),
    "in_buy_asset": cattrs.gen.override(rename="inBuyAsset"),
    "out_sell_amount": cattrs.gen.override(rename="outSellAmount"),
    "out_sell_asset": cattrs.gen.override(rename="outSellAsset"),
    "fee_amount": cattrs.gen.override(rename="feeAmount (optional)"),
    "fee_asset": cattrs.gen.override(rename="feeAsset (optional)"),
    "classification": cattrs.gen.override(rename="classification (optional)"),
    "operation_id": cattrs.gen.override(rename="operationId (optional)"),
    "comments": cattrs.gen.override(rename="comments (optional)"),
}
