-- Migration: Add VIEW_ONLY role to users table
-- Date: 2026-03-05

-- Note: This is a schema update for the role enum
-- SQLAlchemy will handle this automatically when models are updated
-- This file is for reference only

-- The UserRole enum now includes:
-- - ADMIN: Full system access
-- - LANH_DAO: Leadership (view all, approve/reject)
-- - CAN_BO: Officer (manage categories, create records)
-- - USER: Regular user (create own unit records, view own data)
-- - VIEW_ONLY: View-only access (no create/edit/delete permissions)

-- No SQL commands needed, SQLAlchemy will handle enum updates
