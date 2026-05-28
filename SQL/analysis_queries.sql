-- ═══════════════════════════════════════════════
-- UAE REMITTANCE ANALYTICS — SQL ANALYSIS
-- Exchange House Business Intelligence Queries
-- Analyst: Aiswarya NA | 2024
-- ═══════════════════════════════════════════════


-- ───────────────────────────────────────────────
-- QUERY 1: Total Transactions and Volume Overview
-- Purpose: Give management a quick summary of
-- how many transactions happened and total money moved
-- ───────────────────────────────────────────────

SELECT
    status,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_aed), 2) AS total_volume_aed,
    ROUND(AVG(amount_aed), 2) AS avg_transaction_aed,
    ROUND(SUM(fee_aed), 2) AS total_revenue_aed
FROM transactions
GROUP BY status
ORDER BY total_transactions DESC;


-- ───────────────────────────────────────────────
-- QUERY 2: Revenue and Volume by Corridor
-- Purpose: Which countries make us the most money?
-- This helps management decide where to focus marketing
-- ───────────────────────────────────────────────

SELECT
    corridor,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_aed), 2) AS total_volume_aed,
    ROUND(SUM(fee_aed), 2) AS total_revenue_aed,
    ROUND(AVG(amount_aed), 2) AS avg_transaction_aed,
    ROUND(SUM(fee_aed) * 100.0 / SUM(SUM(fee_aed)) OVER(), 2) AS revenue_share_pct
FROM transactions
WHERE status = 'SUCCESS'
GROUP BY corridor
ORDER BY total_revenue_aed DESC;


-- ───────────────────────────────────────────────
-- QUERY 3: Monthly Transaction Trend
-- Purpose: Is the business growing month by month?
-- Helps spot seasonal patterns
-- ───────────────────────────────────────────────

SELECT
    strftime('%Y-%m', date) AS month,
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS successful,
    SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) AS failed,
    ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN amount_aed ELSE 0 END), 2) AS volume_aed,
    ROUND(SUM(CASE WHEN status = 'SUCCESS' THEN fee_aed ELSE 0 END), 2) AS revenue_aed
FROM transactions
GROUP BY month
ORDER BY month;


-- ───────────────────────────────────────────────
-- QUERY 4: Agent Performance Report
-- Purpose: Which agents are causing the most failures?
-- High failure rate = customer dissatisfaction + lost revenue
-- ───────────────────────────────────────────────

SELECT
    agent_id,
    agent_name,
    COUNT(*) AS total_transactions,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) AS successful,
    SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) AS failed,
    ROUND(SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) * 100.0
        / COUNT(*), 2) AS failure_rate_pct,
    ROUND(SUM(fee_aed), 2) AS total_revenue_generated
FROM transactions
GROUP BY agent_id, agent_name
ORDER BY failure_rate_pct DESC;


-- ───────────────────────────────────────────────
-- QUERY 5: Customer Repeat Rate
-- Purpose: How many customers come back more than once?
-- Repeat customers = loyalty = stable revenue
-- ───────────────────────────────────────────────

SELECT
    customer_type,
    COUNT(*) AS number_of_customers,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM (
    SELECT
        customer_id,
        CASE
            WHEN COUNT(*) >= 5 THEN 'Loyal (5+ transactions)'
            WHEN COUNT(*) >= 2 THEN 'Repeat (2-4 transactions)'
            ELSE 'One-time customer'
        END AS customer_type
    FROM transactions
    WHERE status = 'SUCCESS'
    GROUP BY customer_id
) customer_summary
GROUP BY customer_type
ORDER BY number_of_customers DESC;


-- ───────────────────────────────────────────────
-- QUERY 6: Payment Method Analysis
-- Purpose: How do customers prefer to pay?
-- Helps operations team plan cash handling
-- ───────────────────────────────────────────────

SELECT
    payment_method,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_aed), 2) AS total_volume_aed,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS usage_pct
FROM transactions
WHERE status = 'SUCCESS'
GROUP BY payment_method
ORDER BY total_transactions DESC;