# SQL Injection Notes — PortSwigger Labs

## What is SQL Injection?
Injecting malicious SQL into input fields to manipulate database queries.

## Lab 1 — WHERE Clause Injection
- Added ' to URL parameter
- Used OR '1'='1 to return all rows
- Bypassed category filter

## Lab 2 — Login Bypass
- Username: administrator'--
- -- comments out the password check
- Successfully logged in without password

## Lab 3 — UNION Attack
- Used UNION SELECT to retrieve data from other tables
- Must match number of columns in original query

## Impact
- Authentication bypass
- Data extraction
- Admin access without credentials